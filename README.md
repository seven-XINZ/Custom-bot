# Custom-bot

一个**可以直接跑的** Python 异步多平台聊天机器人框架：内核 + 协议适配器 + 插件系统 + 定时任务 + Web 控制台。

最初只是一份只有 3 个适配器骨架的仓库（依赖的 `core` 包并不存在，代码无法导入）。现在已补齐内核与全部运行所需组件，`pip install -r requirements.txt` 后即可启动。

## 特性

- **异步内核**：消息总线、并发上限、优雅退出、组件级故障隔离（某个适配器起不来不影响其他组件）。
- **三种适配器**：QQ（OneBot v11 反向 WebSocket）、HTTP Webhook、通用反向 WebSocket。均兼容 `websockets` 12～15。
- **插件系统**：模块级 `setup(ctx)` + 命令装饰器，支持别名、管理员限定、超时、热重载、启停；`on_message` 监听器可处理非命令消息。
- **定时任务**：自实现 5 段 cron（支持 `*/n`、`a-b`、`a,b`、`a-b/n`，日/周同时受限按 Vixie cron 的 OR 规则）与 interval 两种触发方式；任务脚本同步/异步皆可。
- **Web 控制台**：单页状态面板 + WebSocket 实时推送；插件启停/重载、任务手动触发、日志查看；可选 Basic Auth。
- **零外部存储依赖**：JSON 文件数据库（每表一个文件、原子写入、表级锁），日志按大小轮转。

## 目录结构

```
Custom-bot/                 # 项目根（运行目录）
├── main.py                 # 入口：参数解析、日志初始化、内核启动
├── requirements.txt
├── config/
│   └── config.yaml         # 全部运行配置
├── core/
│   ├── kernel.py           # 内核：装配、消息分发、回复、状态汇总
│   ├── adapters.py         # BaseAdapter 抽象基类
│   ├── message.py          # InternalMessage / Attachment
│   ├── handlers.py         # 命令注册、插件运行时、分发
│   ├── scheduler.py        # cron 解析 + 定时任务
│   ├── database.py         # JSON 数据库
│   ├── webui.py            # aiohttp 控制台
│   ├── config.py           # 配置加载与校验
│   └── utils.py            # 日志与文本工具
├── Adapter/
│   ├── qq_adapter.py       # OneBot v11 反向 WS
│   ├── http_adapter.py     # HTTP webhook 出入站
│   └── reverse_ws_adapter.py# 通用反向 WS
├── plugins/
│   └── official/basic.py   # 基础命令插件（11 条命令）
├── scripts/
│   └── example_task.py     # 示例定时任务
└── data/                   # 运行时生成：db/ 与 logs/
```

## 快速开始

```bash
cd Custom-bot
python3 -m venv .venv && source .venv/bin/activate   # 可选
pip install -r requirements.txt

python3 main.py --check-config   # 先校验配置
python3 main.py                  # 启动
```

默认监听：

| 服务 | 地址 |
| --- | --- |
| QQ 反向 WS | `ws://0.0.0.0:8765/onebot/v11/event` |
| Web 控制台 | `http://0.0.0.0:9090/` |

启动后浏览器打开控制台即可看到适配器、插件、任务与最近消息；在 QQ 里发 `/help` 验证链路。

### 接入 QQ（NapCat / LLOneBot）

1. 在 QQ 客户端里新建**反向 WebSocket**连接：
   - URL：`ws://<机器人服务器 IP>:8765/onebot/v11/event`
   - Token：与 `config.yaml` 里 `adapters.qqbot_reverse_ws.config.access_token` 保持一致（未配置则留空）
2. 客户端连上后日志出现 `QQ 客户端已连接`，给机器人发 `/ping`，收到 `pong` 即通。
3. 把你自己的 QQ 号填进 `kernel.admins`（可先用 `/id` 查看），否则管理员命令不可用。

## 内置命令

| 命令 | 别名 | 说明 |
| --- | --- | --- |
| `help` | 帮助、菜单 | 命令列表；`help <命令>` 查看用法 |
| `ping` | — | 连通性测试，返回耗时 |
| `version` | 版本 | 框架/插件版本与运行时长 |
| `status` | 状态 | 内核与适配器运行状态 |
| `plugins` | 插件 | 已加载插件、命令数与调用次数 |
| `id` | — | 当前用户/群 ID、是否管理员 |
| `echo` | — | 原样回显（默认隐藏） |
| `reload` | 重载 | 热重载插件（管理员） |
| `enable` | 启用 | 启用插件（管理员） |
| `disable` | 停用 | 停用插件（管理员） |
| `broadcast` | 广播 | 给所有管理员发私聊（管理员） |

> `enable/disable/reload` 在插件被停用后仍可用：内核为这三条管理动作保留了兜底实现，避免「停用后只能改配置文件」的死角。

前缀由 `kernel.command_prefixes` 决定（默认 `/`、`!`）；也支持不带前缀直接发命令名（整句精确匹配，避免误触发）。

## 写一个插件

在 `plugins/` 下新建 `.py`，按下面契约实现即可被自动发现（当前扫描 `plugins/official`）：

```python
NAME = "天气预报"
VERSION = "1.0.0"
DESCRIPTION = "查询城市天气"
AUTHOR = "you"

async def setup(ctx):
    @ctx.command(
        "weather", aliases=["天气"],
        description="查询天气", usage="weather <城市>",
    )
    async def weather(c):
        city = c.args[0] if c.args else "成都"
        # c.reply("...") 可直接发多条；return 字符串则自动作为一条回复
        return f"{city}：晴，25℃（示例数据）"
```

要点：

- 处理函数收到 `CommandContext`：`c.args`（按空格切分）、`c.raw_args`、`c.message`、`c.user_id`、`c.is_admin`、`c.config`（插件配置）、`c.db`。
- 返回 `str` 自动回复一条；返回 `list[str]` 自动分段发送；返回 `None` 表示自行用 `c.reply()` 处理。
- `admin_only=True` 的命令只有管理员可用；`timeout` 可覆盖全局超时（秒）。
- 需要在每条消息上做副作用（如计数、关键词回复）时用 `@ctx.on_message` 注册监听器。
- 修改后管理员发 `reload <插件名>` 热重载；启用/停用状态会写入 `data/db/plugins.json`，重启后保持。

## 定时任务

`config.yaml` 的 `scheduled_tasks` 每项支持：

```yaml
scheduled_tasks:
  daily_report:
    enabled: true
    name: "每日报表"
    script_path: "daily_report.py"        # 相对 scripts/ 目录
    schedule: { trigger: "cron", cron: "0 9 * * 1-5" }   # 工作日 9 点
    timeout_seconds: 300

  heartbeat:
    enabled: false
    script_path: "example_task.py"
    schedule: { trigger: "interval", minutes: 30 }        # 或 seconds/hours/days
```

脚本放在 `scripts/`，实现 `async def run(kernel)` 或 `def main(kernel)`，返回值会记入任务结果：

```python
async def run(kernel):
    count = await kernel.db.update("runtime", "count", lambda x: (x or 0) + 1, default=0)
    return f"第 {count} 次执行"
```

cron 五段为 `分 时 日 月 周`，周字段 0/7 均为周日；也接受 `schedule: { cron: "*/10 * * * *" }` 整串写法。

## Web 控制台与 API

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/` | 状态面板（暗色单页，WebSocket 自动刷新） |
| GET | `/api/status` | 完整状态 JSON |
| GET | `/api/plugins` | 插件列表 |
| POST | `/api/plugins/{name}/toggle` | `{"enabled": true/false}` |
| POST | `/api/plugins/{name}/reload` | 热重载 |
| GET | `/api/tasks` | 定时任务列表 |
| POST | `/api/tasks/{id}/run` | 立即执行一次 |
| GET | `/api/logs?lines=200` | 日志尾部 |
| GET | `/ws/status` | 状态推送 WebSocket |

需要登录保护时填写 `webui.auth.username/password`（两项都为空则不校验）。生产环境建议放在 Nginx/Caddy 后并启用 HTTPS。

## 配置说明（常用项）

| 键 | 默认 | 说明 |
| --- | --- | --- |
| `kernel.admins` | 示例值 | 管理员用户 ID 列表；`"*"` 表示所有人（仅调试） |
| `kernel.command_prefixes` | `["/", "!"]` | 命令前缀；含空串表示允许无前缀 |
| `kernel.max_concurrent` | `16` | 同时处理消息上限 |
| `kernel.plugin_timeout` | `15` | 单条命令默认超时（秒） |
| `database.path` | `data/db` | JSON 表目录（相对项目根） |
| `logging.*` | 见配置文件 | 日志级别、目录、轮转大小与备份数 |
| `adapters.*.class` | — | 适配器类路径，如 `Adapter.qq_adapter.QQAdapter` |

## HTTP / 通用 WS 适配器

- **HTTP Webhook**：`POST /webhook`，body 为 JSON（`{"user_id": "...", "content": "/ping"}`）或纯文本；带 `access_token` 时需 `X-Token: <token>` 或 `Authorization: Bearer <token>`。收到即返回 `202`，处理结果通过 `callback_url` 或请求头 `X-Callback-URL` POST 回去。`GET /health` 为健康检查。
- **通用反向 WS**：客户端连 `ws://host:8766/ws`，发 `{"type":"message","user_id":"u1","content":"/ping","msg_id":"m1"}`，收 `{"type":"reply","content":"...","reply_to":"m1"}`；支持 `{"type":"ping"}` → `{"type":"pong"}`。
- **QQ 适配器**额外支持：消息段数组（text/image/record/video/file）、CQ 码字符串、notice/request 事件、任意 OneBot API 透传（插件返回时在 `metadata` 里放 `onebot_action` / `onebot_params`）。

## 常见问题

- **`ImportError: cannot import name 'WebSocketServerProtocol'`**：`websockets` 15 移除了旧 API。本项目已兼容（优先用 `websockets.asyncio.server`，缺失时回退旧模块），无需降级。
- **QQ 连不上 / 401**：检查路径必须完全一致（默认 `/onebot/v11/event`）、Token 一致、端口未被占用。
- **命令没反应**：确认前缀、插件是否被停用（`/plugins` 查看）、发送者是否在 `kernel.admins`。
- **端口冲突**：QQ 8765 / WebUI 9090 / HTTP 8088 / 通用 WS 8766，改 `config.yaml` 对应 `port` 即可。
- **数据在哪**：`data/db/*.json`、`data/logs/custom-bot.log`（均在 `Custom-bot/` 下，已加入 `.gitignore`）。

## 许可

MIT。欢迎 issue / PR。

## 致谢

原始适配器骨架与配置结构由 Xinz / ahhhahh 提供；内核、插件系统、调度与 WebUI 在其基础上补全。
