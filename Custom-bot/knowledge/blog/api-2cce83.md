# Lobe Chat - 目前最好的调用 ChatGPT API 的网页应用

> 标题：Lobe Chat - 目前最好的调用 ChatGPT API 的网页应用
> 分类：AI大模型
> 标签：api、Linux、nas
> 原文：https://www.xinz.fun/archives/api

> **导读**：这篇围绕「Lobe Chat - 目前最好的调用 ChatGPT API 的网页应用」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾AI大模型的读者。执行前建议先备份原配置，并在测试环境验证。

本文重在 Lobe Chat 的部署流程和基础使用方法，如果你需要低价的 API，可以试试这篇文章介绍的商家 gptapi.us：[1 折 GPT-4, GPTAPI.US - 低价高质量的第三方 ChatGPT API - - 他山测评 (tashcp.com)](https://www.nodeseek.com/jump?to=https%3A%2F%2Ftashcp.com%2F2024%2F01%2Fgptapi_us%2F)

| **指标** | **描述** |
| --- | --- |
| 适用系统 | Debian 系发行版，包括 Ubuntu, Armbian，其他发行版稍改命令一般也可 |
| 走通流程时间 | 5 分钟 |

![配图](https://ib.ahfei.blog/imagesbed/lobe-chat-show.webp)

Lobe Chat 目前支持很多模型的 API，OpenAI / Claude 3 / Gemini 甚至开源可自建的 Mistral / Ollama，还支持图像和语言，另有插件系统。

GitHub： [lobehub/lobe-chat: 🤯 an open-source, modern-design LLMs/AI chat framework. Supports Multi AI Providers( OpenAI / Claude 3 / Gemini / Perplexity / Bedrock / Azure / Mistral / Ollama ), Multi-Modals (Vision/TTS) and plugin system. One-click FREE deployment of your private ChatGPT chat application. (github.com)](https://www.nodeseek.com/jump?to=https%3A%2F%2Fgithub.com%2Flobehub%2Flobe-chat)

### 安装

**全复制并执行**，一键创建工作目录并开放端口

sh

```
010203myserve="lobechat"
sudo ufw allow 3210/tcp comment $myserve && sudo ufw reload
mkdir -p ~/myserve/$myserve && cd ~/myserve/$myserve
```

**根据注释自定义**，然后执行，一键创建 docker-compose.yml 文件

yml

```bash
01020304050607080910111213141516171819cat > docker-compose.yml << EOF
---
version: '3.8'

services:
  lobe-chat:
    image: lobehub/lobe-chat
    container_name: lobe-chat
    restart: always
    ports:
      - '3210:3210'
    environment:
      OPENAI_API_KEY: sk-xxx9969cFb16   # 填 API key
      # 如果你使用了我推荐的商家 gptapi.us，那这里就填这个。如果用 chatgpt 官网 api，删除下行
      OPENAI_PROXY_URL: https://api.gptapi.us/v1
      ACCESS_CODE: password   # 访问密码，还能是多个密码 code1,code2,code3
      CUSTOM_MODELS: +gpt-4,+claude-3-opus   # 自定义网页中显示的模型，不了解可删除此行
      # 如果你使用 gptapi.us，加上 claude-3-opus 就能在网页直接使用这个模型了
EOF
```

CUSTOM\_MODELS 使用 `+` 增加一个模型，使用 `-` 来隐藏一个模型，使用 `模型名=展示名` 来自定义模型的展示名，用英文逗号隔开。

---

拉取容器镜像

sh

```
01docker compose pull
```

启动容器（这时就可以访问网页了，网址是 `http://ip_addr_or_domain:3210`）

sh

```
01docker compose up -d
```

关闭容器

sh

```
01docker compose down
```

### 基本使用

![配图](https://ib.ahfei.blog/imagesbed/lobe-chat-webapp-24-03-39.png)

第一次打开网页，到左下角，进入【设置】-【通用设置】，可以填入密码。

另外，在【设置】-【语言模型】，可以自定义 chatgpt api key、代理地址和模型名称，也就是如果你使用别人搭建的 Lobe Chat，也可以填入自己的 API 使用。

【语言模型】里还能设置其他支持的模型。

---

实际使用时，我建议按照你常问的领域，创建“助手”，添加引导词，这样不用每次询问都输入一遍去引导模型。

在上图中的左侧栏，点击【新建助手】，然后点击右上角的三条杠，编辑助手信息。主要就两个：

- **角色设定**：（比如我询问 Linux 问题的助手）你是一个 Linux 专家，精通 Linux 的基本使用和运维，比如 ansible 的使用，以及相关的虚拟化如 docker，网络如 iptables 等的应用
- **名称**： Linux 专家

![image.png](https://ib.ahfei.blog/imagesbed/202403290058526-24-03-27.png)

image.png

聊天时，输入框上栏要注意的有这几个

1. 模型，选合适的模型
2. 闹钟样式的，点击它之后可以限制每次传递多少条对话。推荐 1 或 3，可以随时按需调整。

> ChatGPT 能根据上下文回答，本质是每次发送新的对话，其实是把之前的聊天记录都发送了一遍，如果不限制最大发送的聊天记录，那新对话的价格只会在上一次对话上增加，非常费钱，并且模型能接收的内容是有长度限制的，比如 GPT-4 的 8k，如果超过 8000 token，就会被截断。
>
> “只包含 1 条会话消息” 含义就是，每次只会放松输入框的给 ChatGPT，虽然聊天框中有前文，但 ChatGPT 不会收到，也就不会表现出根据上文回答。
> 3 条消息只会发送上一次你发的、它回答的和这次你发的，也就是能根据上一条回答。

3. 使用，就是这轮对话使用的 token，图片显示 49 就是因为我为助手设定了引导词，每次对话都会发送。

![image.png](https://ib.ahfei.blog/imagesbed/202403290106207-24-03-19.png)

image.png

4. 当一个问题问完，推荐使用这个按钮清空聊天，也就是删除本次话题的所有内容。下次循环，用新话题。这样对于网页加载是有帮助的，而且看着清爽。
5. 输入框中，换行用 Ctrl + Enter，支持 markdown

---

以上就是我平时使用会用到的，其他功能请自行探索把！

如果觉得文章对你有用，请随意赞赏

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
