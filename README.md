# Custom-bot

基于 Python 异步实现的多平台聊天机器人**框架骨架（开发中）**。

## 当前状态

本仓库目前只包含**协议适配器层**与配置文件；框架内核（`core` 消息总线/会话/处理器调度）、插件目录与程序入口尚未随仓库提供，因此当前代码**不能直接运行**，属于早期结构预留。

## 已包含的适配器

| 适配器 | 文件 | 说明 |
| --- | --- | --- |
| QQ 反向 WebSocket | `Adapter/qq_adapter.py` | 基于 OneBot v11 标准的反向 WS 服务端，等待 QQ 机器人客户端连接 |
| HTTP Webhook | `Adapter/http_adapter.py` | 接收外部 HTTP Webhook 请求，也可作为 HTTP 客户端外发 |
| 通用反向 WebSocket | `Adapter/reverse_ws_adapter.py` | 通用反向 WS 服务端，等待外部客户端接入 |

## 配置

配置文件位于 `Custom-bot/config/config.yaml`，主要分段：

- `kernel`：日志级别、全局管理员 ID、框架版本
- `webui`：Web 管理界面监听地址、端口与状态推送间隔
- `database`：数据库提供方（预留 TinyDB）与存储路径
- `adapters`：各适配器的启用开关、监听地址/端口与协议路径
- `handlers`：基础命令处理器与插件配置
- `scheduled_tasks`：定时任务预留配置

## 目录结构

```
Custom-bot/
├── Adapter/
│   ├── __init__.py
│   ├── http_adapter.py
│   ├── qq_adapter.py
│   └── reverse_ws_adapter.py
└── config/
    └── config.yaml
```

## 后续待补

- `core` 内核：内部消息模型、适配器装配、处理器与插件调度
- 程序入口与依赖清单（`requirements.txt`）
- 基础命令插件与示例定时任务

## 说明

适配器依赖 `aiohttp`、`websockets`；仓库未锁定依赖版本，接入内核后再补充 `requirements.txt`。
