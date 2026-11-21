"""Web 管理界面。

一个 aiohttp 应用，提供：
  GET  /                  单页控制台（状态 / 适配器 / 插件 / 任务 / 日志）
  GET  /api/status        内核与适配器状态
  GET  /api/plugins       插件列表
  POST /api/plugins/{name}/toggle   启用 / 停用
  POST /api/plugins/{name}/reload   热重载
  GET  /api/tasks         定时任务列表
  POST /api/tasks/{id}/run          立即执行
  GET  /api/logs?lines=120          日志尾部
  GET  /ws/status         WebSocket 状态推送

认证是可选的：`webui.auth.username` / `password` 都为空时不做校验（默认只建议本机或反代后使用）。
"""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional

from aiohttp import WSMsgType, web

from .utils import fmt_time, truncate

logger = logging.getLogger("内核.WebUI")

SEC_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    "Content-Security-Policy": "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' ws: wss:",
}


class WebUI:
    def __init__(self, kernel):
        self.kernel = kernel
        self.host: str = str(kernel.config.get("webui.host", "0.0.0.0"))
        self.port: int = int(kernel.config.get("webui.port", 9090))
        self.interval: int = max(1, min(30, int(kernel.config.get("webui.stats_interval", 5))))
        self.title: str = str(kernel.config.get("webui.title", "Custom-bot 控制台"))
        self.username: str = str(kernel.config.get("webui.auth.username", "") or "")
        self.password: str = str(kernel.config.get("webui.auth.password", "") or "")
        self._app: Optional[web.Application] = None
        self._runner: Optional[web.AppRunner] = None
        self._site: Optional[web.TCPSite] = None
        self._ws_clients: set[web.WebSocketResponse] = set()
        self._push_task: Optional[asyncio.Task] = None
        self.enabled = bool(kernel.config.get("webui.enabled", True))

    # ------------------------------------------------------------------ 启动
    def build_app(self) -> web.Application:
        app = web.Application()
        app.router.add_get("/", self.handle_index)
        app.router.add_get("/api/status", self.handle_status)
        app.router.add_get("/api/plugins", self.handle_plugins)
        app.router.add_post("/api/plugins/{name}/toggle", self.handle_plugin_toggle)
        app.router.add_post("/api/plugins/{name}/reload", self.handle_plugin_reload)
        app.router.add_get("/api/tasks", self.handle_tasks)
        app.router.add_post("/api/tasks/{task_id}/run", self.handle_task_run)
        app.router.add_get("/api/logs", self.handle_logs)
        app.router.add_get("/ws/status", self.handle_ws)
        app.middlewares.append(self._middleware)
        return app

    async def start(self) -> None:
        if not self.enabled:
            logger.info("WebUI 已在配置中关闭")
            return
        self._app = self.build_app()
        self._runner = web.AppRunner(self._app, access_log=logger)
        await self._runner.setup()
        self._site = web.TCPSite(self._runner, self.host, self.port)
        await self._site.start()
        logger.info("WebUI 已启动: http://%s:%d", self.host, self.port)
        self._push_task = asyncio.create_task(self._push_loop(), name="WebUI 状态推送")

    async def stop(self) -> None:
        if self._push_task:
            self._push_task.cancel()
            try:
                await self._push_task
            except (asyncio.CancelledError, Exception):  # noqa: BLE001
                pass
            self._push_task = None
        for ws in list(self._ws_clients):
            try:
                await ws.close()
            except Exception:  # noqa: BLE001
                pass
        self._ws_clients.clear()
        if self._site:
            await self._site.stop()
            self._site = None
        if self._runner:
            await self._runner.cleanup()
            self._runner = None
        logger.info("WebUI 已停止")

    def is_running(self) -> bool:
        return bool(self._site is not None)

    # ------------------------------------------------------------------ 中间件
    @web.middleware
    async def _middleware(self, request: web.Request, handler):
        if not self._authorized(request):
            return web.Response(
                status=401,
                text="需要登录",
                headers={"WWW-Authenticate": 'Basic realm="Custom-bot"', **SEC_HEADERS},
            )
        try:
            response = await handler(request)
        except web.HTTPException as exc:
            response = exc
        except Exception as exc:  # noqa: BLE001
            logger.exception("WebUI 处理 %s 出错: %s", request.path, exc)
            response = web.json_response({"ok": False, "error": str(exc)}, status=500)
        for key, value in SEC_HEADERS.items():
            response.headers.setdefault(key, value)
        return response

    def _authorized(self, request: web.Request) -> bool:
        if not self.username and not self.password:
            return True
        header = request.headers.get("Authorization", "")
        if not header.startswith("Basic "):
            return False
        try:
            raw = base64.b64decode(header[6:]).decode("utf-8", "replace")
            user, _, pwd = raw.partition(":")
        except Exception:  # noqa: BLE001
            return False
        return user == self.username and pwd == self.password

    # ------------------------------------------------------------------ 页面
    async def handle_index(self, request: web.Request) -> web.Response:
        return web.Response(text=INDEX_HTML.replace("{{TITLE}}", self.title),
                            content_type="text/html", charset="utf-8")

    async def handle_status(self, request: web.Request) -> web.Response:
        return web.json_response({"ok": True, **self.kernel.status()})

    async def handle_plugins(self, request: web.Request) -> web.Response:
        return web.json_response({"ok": True, "plugins": self.kernel.handlers.list_plugins()})

    async def handle_plugin_toggle(self, request: web.Request) -> web.Response:
        name = request.match_info["name"]
        body: Dict[str, Any] = {}
        if request.can_read_body:
            try:
                body = await request.json()
            except json.JSONDecodeError:
                body = {}
        enabled = body.get("enabled")
        if enabled is None:
            runtime = self.kernel.handlers.plugins.get(name)
            enabled = not (runtime and runtime.enabled)
        try:
            state = await self.kernel.handlers.set_enabled(name, bool(enabled))
        except KeyError as exc:
            return web.json_response({"ok": False, "error": str(exc)}, status=404)
        return web.json_response({"ok": True, "name": name, "enabled": state})

    async def handle_plugin_reload(self, request: web.Request) -> web.Response:
        name = request.match_info["name"]
        try:
            runtime = await self.kernel.handlers.reload_plugin(name)
        except KeyError as exc:
            return web.json_response({"ok": False, "error": str(exc)}, status=404)
        except Exception as exc:  # noqa: BLE001
            return web.json_response({"ok": False, "error": str(exc)}, status=500)
        return web.json_response({"ok": True, "plugin": runtime.to_dict()})

    async def handle_tasks(self, request: web.Request) -> web.Response:
        return web.json_response({"ok": True, "tasks": self.kernel.scheduler.list()})

    async def handle_task_run(self, request: web.Request) -> web.Response:
        task_id = request.match_info["task_id"]
        task = self.kernel.scheduler.tasks.get(task_id)
        if not task:
            return web.json_response({"ok": False, "error": "任务不存在"}, status=404)
        result = await self.kernel.scheduler.run_task(task)
        return web.json_response({"ok": bool(result.get("ok")), **result})

    async def handle_logs(self, request: web.Request) -> web.Response:
        try:
            lines = max(1, min(1000, int(request.query.get("lines", 120))))
        except ValueError:
            lines = 120
        log_dir = Path(str(self.kernel.config.get("logging.dir", "data/logs")))
        log_file = log_dir / str(self.kernel.config.get("logging.file", "custom-bot.log"))
        if not log_file.is_file():
            return web.json_response({"ok": True, "lines": []})
        try:
            content = await asyncio.to_thread(log_file.read_text, "utf-8", "replace")
        except OSError as exc:
            return web.json_response({"ok": False, "error": str(exc)}, status=500)
        tail = content.splitlines()[-lines:]
        return web.json_response({"ok": True, "lines": tail})

    # ------------------------------------------------------------------ WebSocket
    async def handle_ws(self, request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse(heartbeat=30)
        await ws.prepare(request)
        self._ws_clients.add(ws)
        try:
            await ws.send_json({"type": "status", "data": self.kernel.status()})
            async for msg in ws:
                if msg.type == WSMsgType.TEXT and msg.data == "ping":
                    await ws.send_json({"type": "pong", "ts": time.time()})
                elif msg.type == WSMsgType.ERROR:
                    break
        finally:
            self._ws_clients.discard(ws)
        return ws

    async def _push_loop(self) -> None:
        while True:
            await asyncio.sleep(self.interval)
            if not self._ws_clients:
                continue
            payload = {"type": "status", "data": self.kernel.status()}
            for ws in list(self._ws_clients):
                try:
                    await ws.send_json(payload)
                except Exception:  # noqa: BLE001
                    self._ws_clients.discard(ws)


INDEX_HTML = """<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{TITLE}}</title>
<style>
:root{--bg:#0b0d10;--card:#15191f;--line:#252b34;--fg:#e6e9ef;--dim:#8b95a5;--accent:#5eead4;--bad:#f87171}
*{box-sizing:border-box}
body{margin:0;background:radial-gradient(1200px 600px at 20% -10%,#1b2430,transparent),var(--bg);
color:var(--fg);font:15px/1.6 -apple-system,"Segoe UI","Noto Sans SC",sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:22px;margin:0 0 4px}
.sub{color:var(--dim);font-size:13px;margin-bottom:22px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}
.card h2{font-size:13px;color:var(--dim);font-weight:600;margin:0 0 10px;letter-spacing:.04em}
.big{font-size:26px;font-weight:600}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th,td{text-align:left;padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:middle}
th{color:var(--dim);font-weight:500}
.tag{display:inline-block;padding:1px 7px;border-radius:999px;font-size:12px;border:1px solid var(--line)}
.ok{color:var(--accent);border-color:rgba(94,234,212,.4)}
.no{color:var(--bad);border-color:rgba(248,113,113,.4)}
button{background:#1e242c;color:var(--fg);border:1px solid var(--line);border-radius:8px;
padding:4px 9px;font-size:12px;cursor:pointer}
button:hover{border-color:var(--accent);color:var(--accent)}
pre{background:#0e1116;border:1px solid var(--line);border-radius:10px;padding:12px;
max-height:320px;overflow:auto;font-size:12px;line-height:1.55;color:#b9c2d0;margin:0}
.sec{margin-top:22px}
</style></head><body><div class="wrap">
<h1>{{TITLE}}</h1>
<div class="sub" id="sub">连接中…</div>
<div class="grid">
  <div class="card"><h2>运行时长</h2><div class="big" id="uptime">—</div></div>
  <div class="card"><h2>适配器</h2><div class="big" id="adapters">—</div></div>
  <div class="card"><h2>插件</h2><div class="big" id="plugins">—</div></div>
  <div class="card"><h2>已处理消息</h2><div class="big" id="messages">—</div></div>
  <div class="card"><h2>AI 心智</h2><div class="big" id="mind">—</div>
    <div class="sub" id="mind-sub" style="margin:4px 0 0"></div></div>
  <div class="card"><h2>知识库</h2><div class="big" id="kb">—</div>
    <div class="sub" id="kb-sub" style="margin:4px 0 0"></div></div>
</div>

<div class="sec card"><h2>适配器</h2><table id="adapter-table">
<thead><tr><th>ID</th><th>协议</th><th>状态</th><th>收发</th><th>最后错误</th></tr></thead><tbody></tbody></table></div>

<div class="sec card"><h2>插件</h2><table id="plugin-table">
<thead><tr><th>名称</th><th>版本</th><th>命令</th><th>调用</th><th>状态</th><th></th></tr></thead><tbody></tbody></table></div>

<div class="sec card"><h2>定时任务</h2><table id="task-table">
<thead><tr><th>名称</th><th>触发</th><th>下次</th><th>次数</th><th>结果</th><th></th></tr></thead><tbody></tbody></table></div>

<div class="sec card"><h2>日志</h2><pre id="logs">加载中…</pre></div>

<script>
const $=s=>document.querySelector(s);
async function j(u,opt){const r=await fetch(u,opt);return r.json()}
function esc(s){return String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function paint(d){
  $('#sub').textContent=`内核 ${d.kernel.version} · ${d.adapter_summary.running}/${d.adapter_summary.total} 适配器运行中 · ${d.plugin_summary.enabled}/${d.plugin_summary.total} 插件启用`;
  $('#uptime').textContent=d.kernel.uptime;
  $('#adapters').textContent=d.adapter_summary.running+' / '+d.adapter_summary.total;
  $('#plugins').textContent=d.plugin_summary.enabled+' / '+d.plugin_summary.total;
  $('#messages').textContent=d.messages_handled;
  if(d.knowledge){
    $('#kb').textContent=d.knowledge.enabled?(d.knowledge.entries+' 条'):'停用';
    $('#kb').style.color=d.knowledge.enabled?'var(--accent)':'var(--dim)';
    $('#kb-sub').textContent=(d.knowledge.providers||[]).join(' / ')||'未配置联网';
  }
  if(d.mind){
    $('#mind').textContent=d.mind.ready?'就绪':'未接通';
    $('#mind').style.color=d.mind.ready?'var(--accent)':'var(--dim)';
    $('#mind-sub').textContent=`${d.mind.persona||''} · ${d.mind.model||'无模型'} · 今日 ${d.mind.calls_today}/${d.mind.max_calls_per_day}`;
  }
  $('#adapter-table tbody').innerHTML=d.adapters.map(a=>`<tr><td>${esc(a.id)}</td><td>${esc(a.protocol)}</td>
    <td><span class="tag ${a.running?'ok':'no'}">${a.running?'运行':'停止'}</span></td>
    <td>${a.stats.received} / ${a.stats.sent}</td><td>${esc(a.last_error||'—')}</td></tr>`).join('');
}
async function loadPlugins(){
  const d=await j('/api/plugins');
  $('#plugin-table tbody').innerHTML=d.plugins.map(p=>`<tr><td>${esc(p.name)}</td><td>${esc(p.version||'—')}</td>
    <td>${esc(p.commands.join(', ')||'—')}</td><td>${p.calls}${p.errors?' / 错'+p.errors:''}</td>
    <td><span class="tag ${p.enabled?'ok':'no'}">${p.enabled?'启用':'停用'}</span></td>
    <td><button onclick="toggle('${esc(p.name)}',${!p.enabled})">${p.enabled?'停用':'启用'}</button>
    <button onclick="reload('${esc(p.name)}')">重载</button></td></tr>`).join('');
}
async function loadTasks(){
  const d=await j('/api/tasks');
  $('#task-table tbody').innerHTML=d.tasks.map(t=>`<tr><td>${esc(t.name)}</td><td>${esc(t.trigger)}</td>
    <td>${esc(t.next_run_at||'—')}</td><td>${t.runs}${t.failures?' / 错'+t.failures:''}</td>
    <td>${esc(t.last_error||t.last_result||'—')}</td>
    <td><button onclick="runTask('${esc(t.id)}')">执行</button></td></tr>`).join('');
}
async function loadLogs(){const d=await j('/api/logs?lines=120');$('#logs').textContent=(d.lines||[]).join('\\n')||'（暂无日志）'}
window.toggle=async(n,e)=>{await j('/api/plugins/'+encodeURIComponent(n)+'/toggle',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({enabled:e})});await loadPlugins()};
window.reload=async n=>{const r=await j('/api/plugins/'+encodeURIComponent(n)+'/reload',{method:'POST'});if(!r.ok)alert(r.error);await loadPlugins()};
window.runTask=async id=>{const r=await j('/api/tasks/'+encodeURIComponent(id)+'/run',{method:'POST'});if(!r.ok)alert(r.error||'失败');await loadTasks()};
function ws(){
  const proto=location.protocol==='https:'?'wss':'ws';
  const s=new WebSocket(`${proto}://${location.host}/ws/status`);
  s.onmessage=ev=>{const m=JSON.parse(ev.data);if(m.type==='status')paint(m.data)};
  s.onclose=()=>{ $('#sub').textContent='连接断开，5 秒后重连…'; setTimeout(ws,5000) };
}
(async()=>{paint(await j('/api/status'));await Promise.all([loadPlugins(),loadTasks(),loadLogs()]);ws();
 setInterval(loadLogs,8000);
})();
</script>
</div></body></html>"""
