# Custom-bot

一个**可以直接跑的** Python 异步多平台聊天机器人框架：内核 + 协议适配器 + 插件系统 + 定时任务 + Web 控制台。

最初只是一份只有 3 个适配器骨架的仓库（依赖的 `core` 包并不存在，代码无法导入）。现在已补齐内核与全部运行所需组件，`pip install -r requirements.txt` 后即可启动。

## 特性

- **异步内核**：消息总线、并发上限、优雅退出、组件级故障隔离（某个适配器起不来不影响其他组件）。
- **AI 心智**：可接任意 OpenAI 兼容模型；有人格、有长期记忆、会从对话里学习、能定期自省，还能生成插件/代码提案交管理员审批。
- **本地知识库**：没有模型或模型不可用时，先用本地文档/手工知识作答；本地没命中还能联网搜索并缓存结果，断网后继续用缓存回答。
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
│   ├── mind.py             # 心智：人格、对话、记忆、自省、提案审批
│   ├── llm.py              # OpenAI 兼容模型客户端
│   ├── memory.py           # 长期记忆（事实 + 对话片段）
│   ├── knowledge.py        # 本地知识库 + 联网搜索/网页抓取
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
│   ├── official/basic.py   # 基础命令插件（11 条命令）
│   ├── official/ai.py      # AI 心智插件（对话/记忆/自省/提案）
│   └── official/kb.py      # 知识库插件（问答/录入/导入/联网）
├── knowledge/              # 本地知识文档（.md/.txt，启动自动索引）
├── scripts/
│   ├── example_task.py     # 示例定时任务
│   └── mind_tick.py        # 定时自省任务
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
| `ask` | 问知识库、qa | 问知识库：本地优先，没有则联网（无模型也能用） |
| `kb` | 知识库 | 知识库管理：统计/搜索/添加/导入/删除/重建索引/联网 |

> `enable/disable/reload` 在插件被停用后仍可用：内核为这三条管理动作保留了兜底实现，避免「停用后只能改配置文件」的死角。

前缀由 `kernel.command_prefixes` 决定（默认 `/`、`!`）；也支持不带前缀直接发命令名（整句精确匹配，避免误触发）。

## AI 心智

内核里有一个可接任意 OpenAI 兼容模型的「心智」：人格 + 长期记忆 + 自动学习 + 自省 + 插件/代码提案。

### 接通模型

```yaml
brain:
  base_url: "https://api.openai.com/v1"
  model: "gpt-4o-mini"
  api_key: ""                       # 也可以留空，用环境变量
  api_key_env: "CUSTOM_BOT_LLM_KEY"
```

```bash
export CUSTOM_BOT_LLM_KEY="sk-..."
```

常见服务：OpenAI `https://api.openai.com/v1`；DeepSeek `https://api.deepseek.com/v1`；火山方舟 `https://ark.cn-beijing.volces.com/api/v3`（model 填推理接入点 ID）；本地 vLLM / Ollama 网关填对应地址即可。改完重启，发 `/brain` 看到「就绪」即通。

### 对话与学习

- 私聊默认自动接话；群聊需要 @ 机器人或叫名字（`mind.trigger_names`，默认「小栖」）。
- 每个用户有回复冷却（`cooldown_seconds`）和独立上下文（`history_turns`）。
- 后台会从对话里提取稳定事实（口味、身份、习惯、约定），按 `learn_cooldown_seconds` 限频；寒暄和一次性请求不会入库。
- 记忆按相关度注入系统提示，事实表满了自动淘汰最旧的。
- 每天有调用上限 `max_llm_calls_per_day`，超了直接拒答，不会无上限烧 token。

### 人格

`persona` 段定义名字、自述、性格、口吻与边界；运行时也能改：

```text
/persona
/persona set style 更简短一点，别超过两句话
/persona reset
```

覆盖值写入 `data/db/persona.json`，重启保留。

### 自省

- `/reflect` 立即回顾最近对话与运行状态，输出一段自我评价，存进 `mind_journal`。
- `/journal` 查看历史自省。
- 定时自省默认每 6 小时运行一次（`scheduled_tasks.mind_reflection`），不需要就设为 `false`。
- `mind.proactive: true` 会把自省私聊给管理员，默认每天最多一次。

### 让它写插件 / 改代码

```text
/propose 做一个骰子插件，命令 /roll 2d6
/propose --target 基础命令 在 ping 回复里加一句“我在”
/proposals
/approve p-20261121-132311-7a50
/reject  p-20261121-132311-7a50
/rollback 基础命令
```

安全边界：

1. 提案先写到 `data/proposals/<id>/`（含 `meta.json`、`plugin.py`、改旧插件时的 `diff.txt`），不动线上代码；
2. 应用前做语法编译 + AST 校验：必须有模块级 `NAME`、`setup(ctx)`，禁止 `subprocess`、`eval/exec`、`os.system` 等；
3. 改现有插件先备份到 `data/backups/<插件名>/`，加载失败自动还原；`/rollback` 回到最近备份；
4. 新插件安装到 `plugins/generated/`（已加入 `.gitignore`），下次启动会被自动发现；
5. `mind.auto_apply: true` 可跳过人工审批直接应用，不建议长期开启。

### 心智命令

| 命令 | 别名 | 说明 |
| --- | --- | --- |
| `chat` | 聊、问 | 显式对话（不依赖自动接话） |
| `brain` | 心智 | 模型、人格、调用量、记忆与提案状态 |
| `remember` | 记住 | 手动记一条：`/remember 口味 = 微辣` |
| `recall` | 回忆 | 按关键词检索记忆 |
| `forget` | 忘掉 | 删除一条记忆 |
| `persona` | 人格 | 查看/修改人格（管理员） |
| `reflect` | 自省 | 立即自省（管理员） |
| `journal` | 日记 | 查看自省记录（管理员） |
| `feedback` | 反馈 | 对回复风格提意见，写入长期记忆 |
| `propose` | 提案 | 生成插件/改写提案（管理员） |
| `proposals` | — | 列出提案（管理员） |
| `approve` | — | 应用提案（管理员） |
| `reject` | — | 放弃提案（管理员） |
| `rollback` | 回滚 | 还原插件备份（管理员） |

## 本地知识库（没有模型也能答）

模型没配 Key、服务商挂了、服务器出不去外网，机器人都还能靠本地知识库回答；本地没有的内容，可以临时联网查，查到后写进缓存。

### 知识从哪来

1. **文档目录**：把 `.md` / `.markdown` / `.txt` 放进 `knowledge/`，启动时按段落切片索引；改完文件用 `/kb reindex` 重建。
2. **手动录入**：`/kb add 标题 | 内容`（管理员）。
3. **网页导入**：`/kb import https://example.com/page`（管理员），抓正文入库。
4. **联网缓存**：`/ask` 本地没命中时会搜索，结果按 `cache_ttl_seconds` 缓存；同一问题下次直接本地命中。

### 怎么用

```text
/ask 服务器怎么部署          # 本地优先，没有就联网
/kb search Docker            # 只查本地
/kb add 部署约定 | 重启容器前先备份 data 目录
/kb import https://example.com/docs
/kb stats
/kb reindex
```

没有模型时，私聊或群里 @/叫名字（默认「小栖」）会自动用知识库兜底；有模型时自动接话仍归 AI 心智，不会抢答。`/ask` 不受这个限制，随时可用。

### 检索与联网

- 本地检索：标题、标签、正文加权，中文按二元组切分，并计算「主题词覆盖率」，避免只命中一个「Python」就硬答。
- 联网顺序：`bing`（直接抓 `cn.bing.com`，国内一般可用）→ `duckduckgo`（部分网络不可达）；有自建 SearXNG 可只配它。
- 联网结果只取标题、链接、摘要，不执行网页脚本；导入正文会去掉标签并限制大小。
- 网页内容属于外部不可信输入，仅作为资料展示；机器人不会据此执行命令或改代码。

```yaml
knowledge:
  enabled: true
  docs_dir: "knowledge"
  index_docs_on_start: true
  search:
    providers: ["bing", "duckduckgo"]   # 或 ["searxng"]
    searxng_url: ""                     # 例：http://127.0.0.1:8080
    timeout: 12
    max_results: 5
  web:
    cache_ttl_seconds: 86400
    max_page_bytes: 2097152
    allow_private_urls: false           # 默认禁止抓内网，防 SSRF
  offline:
    auto_answer: true                   # 无模型时自动兜底
    auto_web: true                      # 本地没命中且像问句时联网
    min_score: 3.0
    min_coverage: 0.6
    cooldown_seconds: 60
```

> `/kb add`、`/kb import`、`/kb delete`、`/kb reindex`、`/kb web` 需要管理员；普通用户可用 `/ask` 和 `/kb search`。Web 控制台的状态卡会显示知识库条数与联网引擎。

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

面板除了适配器、插件、任务与日志，还会显示 AI 心智是否就绪、模型、人格和今日调用量，以及知识库条数与联网引擎。

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
| `brain.*` | 见配置 | 模型地址、模型名、Key（也可用环境变量） |
| `persona.*` | 见配置 | 名字、性格、口吻、边界 |
| `mind.auto_reply` | `true` | 是否自动接话；群聊另需 @ 或叫名字 |
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
- **AI 不接话**：先 `/brain` 看是否「就绪」；未就绪检查 `brain.base_url/model/api_key`；群聊要 @ 或叫名字；同一用户 5 秒内只回一次。
- **提案应用失败**：看 `data/proposals/<id>/meta.json` 与日志；代码校验不过（缺 `NAME/setup` 或含禁用内容）会被拒绝，改完再 `/propose`。
- **端口冲突**：QQ 8765 / WebUI 9090 / HTTP 8088 / 通用 WS 8766，改 `config.yaml` 对应 `port` 即可。
- **数据在哪**：`data/db/*.json`、`data/logs/custom-bot.log`（均在 `Custom-bot/` 下，已加入 `.gitignore`）。

## 许可

MIT。欢迎 issue / PR。

## 致谢

原始适配器骨架与配置结构由 Xinz / ahhhahh 提供；内核、插件系统、调度与 WebUI 在其基础上补全。
