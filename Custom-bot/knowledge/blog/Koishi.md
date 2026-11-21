# docker安装Koishi

> 标题：docker安装Koishi
> 分类：机器人Bot
> 标签：无
> 原文：https://www.xinz.fun/archives/Koishi

> **导读**：这篇是「docker安装Koishi」的实操教程。下文按「在容器中使用」「**启动容器**[****](https://koishi.chat/zh-CN/manual/starter/docker.html#%E5%90%AF%E5%8A%A8%E5%AE%B9%E5%99%A8)」「自用版」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾机器人Bot的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 在容器中使用
2. **启动容器**[****](https://koishi.chat/zh-CN/manual/starter/docker.html#%E5%90%AF%E5%8A%A8%E5%AE%B9%E5%99%A8)
3. 自用版
4. **安装插件**[****](https://koishi.chat/zh-CN/manual/starter/docker.html#%E5%AE%89%E8%A3%85%E6%8F%92%E4%BB%B6)
5. 安装完成后连接机器人ws
6. 反向ws使用
7. 机器人初始配置按需配置

## 在容器中使用

Docker 等容器化软件是以服务生产环境而开发的应用平台，在使用此类软件部署之时，我们相信你已经掌握了运维一台服务器所必须的知识，同时也理解了容器化的概念与相关软件的基础操作。如若不然，在除路由器或 NAS 等特殊环境外，请 选择其他安装方式。

Koishi 提供了 Docker 镜像，方便你在容器中运行 Koishi。你需要首先安装 Docker 来运行容器

## **启动容器**[****](https://koishi.chat/zh-CN/manual/starter/docker.html#%E5%90%AF%E5%8A%A8%E5%AE%B9%E5%99%A8)

使用以下命令启动容器：

```bash
docker run -p 5140:5140 koishijs/koishi
```

许多插件依赖 [**koishi-plugin-puppeteer**](https://www.npmjs.com/package/koishi-plugin-puppeteer) 来进行图片渲染，故默认镜像中包含 Chromium。如果你认为镜像过大，不需要预装 Chromium，我们也提供了轻量版本：

```bash
docker run -p 5140:5140 koishijs/koishi:latest-lite
```

## 自用版

如果您希望以特定的容器名称（如 `koishi`）运行 Docker 容器，并确保它在崩溃或停止后能够自动重启，您可以使用以下命令

```bash
docker run -d \
  --name koishi \
  --restart unless-stopped \
  -p 5140:5140 \
  -v /opt/1panel/apps/koishi:/koishi \
  -e TZ=Asia/Shanghai \
  koishijs/koishi:latest

#命令解释
#docker run: 用于创建并运行一个新的容器。
#-d: 以分离模式（后台模式）运行容器。
#--name koishi: 指定容器的名称为 koishi。
#--restart unless-stopped: 设置重启策略为“除非手动停止”，这意味着如果#容器崩溃或 Docker 服务重启，容器会自动重启。
#-p 5140:5140: 将主机的 5140 端口映射到容器的 5140 端口。
#-v /some/place:/koishi: 将主机的 /some/place 目录挂载到容器内的 /koishi 目录。
#-e TZ=Asia/Shanghai: 设置环境变量 TZ 为 Asia/Shanghai，以指定时区。
#koishijs/koishi: 指定要使用的 Docker 镜像。
```

启动后将会绑定 Koishi 控制台到 5140 端口。

如果你需要持久化，请使用 `-v /some/place:/koishi` 来映射 Koishi 的文件。

如果需要更正时区，请使用 `-e TZ=Asia/Shanghai` 来设置时区。

Koishi 本体及其插件都可以控制台完成更新。在持久化文件过后更新容器仅会更新 Chromium 和 Node.js 等的版本。

## **安装插件**[****](https://koishi.chat/zh-CN/manual/starter/docker.html#%E5%AE%89%E8%A3%85%E6%8F%92%E4%BB%B6)

在容器运行时，可以通过在浏览器中访问 `http://宿主机地址:5140` 在控制台中安装和启用插件。若无法访问请检查你的防火墙配置是否正确。

## 安装完成后连接机器人ws

## 反向ws使用

先配置好Koishi的ws链接插件

插件市场搜索

```
adapter-onebot
```

安装如下图中插件

**![配图](/upload/image-xhhs.png)**

然后根据图片操作

进入插件配置

![配图](/upload/image-htco.png)

先配置机器人qq然后点击上方启动

![配图](/upload/image-zaba.png)

根据教程安装docker容器ncqq

ncqq教程:[Docker安装Napcat反向ws-鑫仔博客 (xinz.fun)](https://www.xinz.fun/archives/Napcat)

操作完成后打开webui添加反向ws

```
ws://ip:5140/onebot
```

即可连接

## 机器人初始配置按需配置

### 监听设置 @`黑白名单`

安装插件

```
keyword-blocker
```

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
