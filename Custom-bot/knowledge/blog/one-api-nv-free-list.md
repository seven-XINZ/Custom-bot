# One-API + nv-free-list 英伟达免费模型自动同步部署教程

> 标题：One-API + nv-free-list 英伟达免费模型自动同步部署教程
> 分类：AI大模型
> 标签：api、docker、ai
> 原文：https://www.xinz.fun/archives/one-api-nv-free-list

> **导读**：这篇是「One-API + nv-free-list 英伟达免费模型自动同步部署教程」的实操教程。下文按「方案概述」「一、部署 nv-free-list」「二、部署 One-API」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾AI大模型的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 方案概述
2. 一、部署 nv-free-list
3. 二、部署 One-API
4. 三、部署自动同步脚本
5. 四、调用示例
6. 五、常见问题
7. 六、常用运维命令
8. 结语

> 文档版本：V1.0
> 适用环境：Debian / Ubuntu，Docker + Docker Compose
> 纯容器部署，不含反向代理配置
> 脱敏说明：文中密钥、账号均为占位符，部署前请替换为你自己的真实值

## 方案概述

NVIDIA 官方提供了大量免费可调用的大模型，但模型列表会动态上下架，人工维护 One-API 渠道模型非常麻烦。本方案由两个容器服务加一个本地同步脚本组成：

1. **nv-free-list**：定时拉取 NVIDIA 官方模型清单，过滤免费模型后通过 HTTP 接口输出模型 ID 列表。
2. **One-API**：模型聚合转发面板，提供统一的 OpenAI 兼容接口、密钥与额度管控。
3. **同步脚本**：读取 nv-free-list 的模型清单，自动更新 One-API 对应渠道的模型列表，配合定时任务无人值守运行。

### 端口规划

| 服务 | 端口 | 说明 |
| ---- | ---- | ---- |
| nv-free-list | 8000 | 内部清单接口，仅本机调用 |
| One-API | 3003 | 面板访问与对外接口 |

### 前置依赖

1. 服务器已安装 Docker 与 Docker Compose。
2. 已获取 NVIDIA API Key（`nvapi-` 开头）。
3. 服务器防火墙放行 3003 端口。
4. 已安装 Python3、pip3（用于运行同步脚本）。

### 所需镜像清单

| 服务 | 镜像名称 | 说明 |
| ---- | ---- | ---- |
| One-API | `justsong/one-api:latest` | 模型聚合转发面板 |
| nv-free-list | `python:3.11-slim` | 运行清单抓取服务（源码挂载进容器） |

---

## 一、部署 nv-free-list

部署目录：`/vol1/1000/docker/1panel/apps/nv-free-list`

功能：定时抓取英伟达模型清单，对外提供接口 `http://127.0.0.1:8000/api/models_free`。

### 1. 创建目录

```bash
mkdir -p /vol1/1000/docker/1panel/apps/nv-free-list
cd /vol1/1000/docker/1panel/apps/nv-free-list
```

### 2. 主程序 main.py

```python
from fastapi import FastAPI
import httpx
import asyncio
import logging

# ========= 配置区 =========
NVIDIA_API_KEY = "替换为你的 NVIDIA nvapi-xxxx 密钥"
REFRESH_INTERVAL = 43200  # 单位秒，12 小时刷新一次模型列表
LIST_URL = "https://integrate.api.nvidia.com/v1/models"
# ==========================

app = FastAPI(title="nv-free-list")
model_cache = []
lock = asyncio.Lock()

logging.basicConfig(level=logging.INFO)

async def fetch_models():
    """从 NVIDIA 官方拉取模型列表，过滤免费模型"""
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(LIST_URL, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            all_models = data.get("data", [])
            free_models = []
            for m in all_models:
                # 这里根据 NVIDIA 返回字段过滤免费模型，按需调整判断逻辑
                if m.get("id"):
                    free_models.append(m["id"])
            return free_models
    except Exception as e:
        logging.error(f"拉取模型失败：{str(e)}")
        return []

async def refresh_task():
    global model_cache
    while True:
        logging.info("开始刷新 NVIDIA 模型列表")
        new_list = await fetch_models()
        async with lock:
            model_cache = new_list
        logging.info(f"刷新完成，模型数量：{len(model_cache)}")
        await asyncio.sleep(REFRESH_INTERVAL)

@app.on_event("startup")
async def startup():
    asyncio.create_task(refresh_task())

@app.get("/api/models_free")
async def get_free_models():
    async with lock:
        return {"models": model_cache}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
```

### 3. 依赖文件 requirements.txt

```txt
fastapi
uvicorn
httpx
```

### 4. 编排文件 docker-compose.yml

```yaml
version: "3.8"
services:
  nv-free-list:
    image: python:3.11-slim
    container_name: nv-free-list
    working_dir: /app
    ports:
      - "8000:8000"
    volumes:
      - ./main.py:/app/main.py
      - ./requirements.txt:/app/requirements.txt
    environment:
      - TZ=Asia/Shanghai
    restart: unless-stopped
    command: >
      sh -c "pip install --no-cache-dir -r requirements.txt &&
             python main.py"
```

### 5. 启动服务

```bash
cd /vol1/1000/docker/1panel/apps/nv-free-list
docker-compose up -d

# 查看日志
docker logs -f nv-free-list
```

### 6. 接口验证

```bash
curl http://127.0.0.1:8000/api/models_free
```

正常返回格式：

```json
{"models": ["模型ID1", "模型ID2"]}
```

### 7. 打包导出（迁移或备份用）

```bash
cd /vol1/1000/docker/1panel/apps/nv-free-list
tar -zcvf nv-free-list.tar.gz main.py requirements.txt docker-compose.yml
```

---

## 二、部署 One-API

部署目录：`/vol1/1000/docker/1panel/apps/one-api`，端口 3003。

### 1. 创建目录

```bash
mkdir -p /vol1/1000/docker/1panel/apps/one-api
cd /vol1/1000/docker/1panel/apps/one-api
```

### 2. 编排文件 docker-compose.yml

```yaml
version: "3.8"
services:
  one-api:
    image: justsong/one-api:latest
    container_name: one-api
    network_mode: bridge
    ports:
      - "3003:3000"
    environment:
      - TZ=Asia/Shanghai
      - SESSION_SECRET=替换为你自己的随机密钥
      - DNS_NAMESERVER=223.5.5.5,119.29.29.29
    volumes:
      - ./data:/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-fs", "http://127.0.0.1:3000/api/status"]
      interval: 60s
      timeout: 10s
      retries: 3
```

### 3. 启动容器

```bash
docker-compose up -d

# 查看容器状态
docker ps | grep one-api

# 查看日志（排查启动报错）
docker logs -f one-api
```

### 4. 初始化面板

浏览器访问：`http://服务器IP:3003`

- 默认初始账号：`root`，默认密码：`123456`
- 登录后请第一时间修改密码，并新建自己的管理员账号。

### 5. 添加英伟达渠道

渠道参数：

- 渠道类型：OpenAI 兼容（Type 50）
- 上游地址：`https://integrate.api.nvidia.com/v1`
- 官方密钥：`nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxx`（替换为你自己的 NVIDIA Key）
- 模型来源：由 nv-free-list 服务自动拉取

操作步骤：

1. 登录 One-API 后台。
2. 渠道 → 添加渠道 → 选择「OpenAI 兼容」。
3. 填入上游地址与 NVIDIA 密钥。
4. 模型栏先随便填写，后续交给同步脚本自动维护。

---

## 三、部署自动同步脚本

脚本目录：`/vol1/1000/docker/1panel/apps/one-api/sync`

### 1. 创建目录

```bash
mkdir -p /vol1/1000/docker/1panel/apps/one-api/sync
cd /vol1/1000/docker/1panel/apps/one-api/sync
```

### 2. 同步脚本 sync_nv_models.py

```python
import requests
import logging

# ========= 配置区（自行修改） =========
ONE_API_URL = "http://127.0.0.1:3003"
ONE_API_USER = "替换为你的 One-API 管理员账号"
ONE_API_PASS = "替换为你的 One-API 管理员密码"
LIST_URL = "http://127.0.0.1:8000/api/models_free"
CHANNEL_ID = 1
LOG_FILE = "./sync.log"
# ======================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def login():
    """登录 One-API 获取会话 Cookie"""
    resp = requests.post(
        f"{ONE_API_URL}/api/user/login",
        json={"username": ONE_API_USER, "password": ONE_API_PASS},
        timeout=30,
    )
    if resp.status_code != 200 or not resp.json().get("success"):
        raise Exception("One-API 登录失败")
    return resp.cookies

def get_channel(cookies):
    """读取渠道信息"""
    resp = requests.get(
        f"{ONE_API_URL}/api/channel/{CHANNEL_ID}",
        cookies=cookies,
        timeout=30,
    )
    if resp.status_code != 200 or not resp.json().get("success"):
        raise Exception("获取渠道信息失败")
    return resp.json()["data"]

def update_channel(cookies, channel_data, model_list):
    """更新渠道模型列表"""
    channel_data["models"] = ",".join(model_list)
    resp = requests.put(
        f"{ONE_API_URL}/api/channel/{CHANNEL_ID}",
        json=channel_data,
        cookies=cookies,
        timeout=30,
    )
    if resp.status_code != 200 or not resp.json().get("success"):
        raise Exception("更新渠道模型失败")
    return True

def main():
    try:
        logging.info("===== 开始同步 NVIDIA 模型列表 =====")
        r = requests.get(LIST_URL, timeout=30)
        r.raise_for_status()
        new_models = r.json()["models"]
        logging.info(f"远端模型数量：{len(new_models)}")

        ck = login()
        ch = get_channel(ck)
        old_models = ch["models"].split(",") if ch.get("models") else []
        logging.info(f"渠道原有模型数量：{len(old_models)}")

        if sorted(old_models) == sorted(new_models):
            logging.info("模型列表无变化，无需更新")
            return

        update_channel(ck, ch, new_models)
        logging.info(f"更新完成，新模型数量：{len(new_models)}")
    except Exception as e:
        logging.error(f"同步异常：{str(e)}")

if __name__ == "__main__":
    main()
```

### 3. 安装依赖

```bash
pip3 install requests
```

### 4. 手动测试

```bash
python3 sync_nv_models.py
cat sync.log
```

### 5. 配置定时任务

```bash
crontab -e
```

写入以下内容，每天 00:30、12:30 自动同步模型：

```bash
30 00,12 * * * /usr/bin/python3 /vol1/1000/docker/1panel/apps/one-api/sync/sync_nv_models.py >> /vol1/1000/docker/1panel/apps/one-api/sync/cron.log 2>&1
```

---

## 四、调用示例

接口地址：`http://服务器IP:3003/v1`

> 访问令牌在 One-API 后台自行新建，形如 `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx`。

curl 测试命令：

```bash
curl http://服务器IP:3003/v1/chat/completions \
  -H "Authorization: Bearer sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nvidia/nemotron-3.5-bolt-e4b",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

接口完全兼容 OpenAI 格式，所有支持 OpenAI 的客户端都可以直接接入。

---

## 五、常见问题

1. **拉取模型为空**：检查 NVIDIA Key 是否正确、是否有权限访问模型列表接口。
2. **同步脚本报错**：确认 `CHANNEL_ID` 与后台渠道 ID 一致。
3. **请求超时**：已在容器内配置国内 DNS，仍需检查服务器出站网络是否正常。
4. **对接上游返回 404**：渠道上游地址必须带 `/v1` 后缀，即 `https://integrate.api.nvidia.com/v1`。

## 六、常用运维命令

```bash
# 重启服务
docker restart one-api
docker restart nv-free-list

# 停止服务
docker stop one-api
docker stop nv-free-list

# 更新 One-API 镜像
cd /vol1/1000/docker/1panel/apps/one-api
docker pull justsong/one-api:latest
docker-compose up -d
```

## 结语

这套方案一次部署后即可长期自动运行：官方上架新模型会自动进入 One-API 渠道，官方下架的模型会自动剔除，全程无需人工干预。后续各类 AI 应用、机器人、知识库与多模态项目，都可以统一接入这个接口池。
