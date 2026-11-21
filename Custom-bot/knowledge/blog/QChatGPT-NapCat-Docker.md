# QChatGPT＋NapCat-Docker 部署运行

> 标题：QChatGPT＋NapCat-Docker 部署运行
> 分类：机器人Bot
> 标签：docker、Linux、群晖、ubuntu
> 原文：https://www.xinz.fun/archives/QChatGPT＋NapCat-Docker

> **导读**：这篇是「QChatGPT＋NapCat-Docker 部署运行」的实操教程。下文按「特别感谢」「Docker部署(仅推荐在Linux上使用)」「[**注意**](https://qchatgpt.rockchin.top/posts/deploy/qchatgpt/docker.html#%E6%B3%A8%E6%84%8F)」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾机器人Bot的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 特别感谢
2. Docker部署(仅推荐在Linux上使用)
3. [**注意**](https://qchatgpt.rockchin.top/posts/deploy/qchatgpt/docker.html#%E6%B3%A8%E6%84%8F)
4. [**OneBot 11 协议**](https://qchatgpt.rockchin.top/posts/deploy/platforms/aiocqhttp/#onebot-11-%E5%8D%8F%E8%AE%AE)**反向wsNapCat**
5. NapCat-Docker
6. 配置
7. 启动容器
8. 反向 WS
9. 固化路径，方便下次直接快速登录
10. 登录
11. Tips
12. 反向ws对接
13. 以及其余 1 个小节

## 特别感谢

**感谢雪佬开发和维护（雪佬也在群内，如果有相关的建议和问题也可以来问问），Napcat项目地址：**

[**https://github.com/NapNeko/NapCatQQ**](https://github.com/NapNeko/NapCatQQ)

**感谢大佬开发和维护（大佬也在Lazy的交流群:[群:619154800]**

**，如果有相关的建议和问题也可以来问问），Napcat项目地址：**

[项目主页 | QChatGPT (rockchin.top)](https://qchatgpt.rockchin.top/)

使用文字转语音自用推荐:[TTS适配海豚Ai TTS-Online](https://www.ttson.cn/?source=falPMO)

## Docker部署(仅推荐在Linux上使用)

---

请您确保您**确实**需要 Docker 部署，您**必须**具有以下能力：

- 了解 `Docker` 和 `Docker Compose` 的使用
- 了解容器间网络通信配置方式
- 了解容器文件挂载机制
- 了解容器调试操作
- 动手能力强、资料查找能力强

若您不完全具有以上能力，请勿使用 Docker 部署，由于误操作导致的配置不正确，我们将不会解答您的问题并不负任何责任。
**不建议**您在除 Linux 之外的系统上使用 Docker 进行部署。

**注**

请先确保 Docker 和 Docker Compose 已安装

以下是推荐的`docker-compose.yaml`模板，您可以根据自己的需求进行修改。

```yaml
version: "3"

services:
  qchatgpt:
    image: rockchin/qchatgpt:latest  # 使用最新的 QChatGPT 镜像
    volumes:
      - ./data:/app/data  # 将主机的 ./data 目录挂载到容器的 /app/data 目录
      - ./plugins:/app/plugins  # 将主机的 ./plugins 目录挂载到容器的 /app/plugins 目录
    restart: on-failure  # 当容器非正常退出时自动重启

    # 根据具体环境配置网络
    # 使用 host 网络模式时，容器将共享主机的网络栈
    # 这意味着容器内的服务将直接使用主机的 IP 地址
    # 例如，如果容器内的应用监听在 8080 端口，您可以通过主机的 8080 端口访问该应用
    # 请注意，使用 host 模式时，容器的端口映射将无效
    # 可以通过取消注释以下行来启用 host 网络模式：
    # network_mode: host
```

### 说明

- `image`: 指定要使用的 Docker 镜像，这里使用的是 `rockchin/qchatgpt:latest`。
- `volumes`:

  - `./data:/app/data`: 将当前目录下的 `data` 文件夹挂载到容器的 `/app/data` 目录中，以便容器可以访问主机上的数据。
  - `./plugins:/app/plugins`: 将当前目录下的 `plugins` 文件夹挂载到容器的 `/app/plugins` 目录中，以便容器可以访问主机上的插件。
- `restart`: 设置容器的重启策略为 `on-failure`，即当容器因错误退出时会自动重启。
- `network_mode: host`:

  - 该配置允许容器使用主机的网络堆栈。
  - 在这种模式下，容器内的应用将使用主机的 IP 地址和端口进行通信。
  - 例如，如果容器内的应用监听在 8080 端口，您可以通过访问主机的 8080 端口直接与之交互。
  - 注意：使用 `host` 模式时，容器内部的端口映射（如 `ports`）将无效，所以不需要在 `ports` 中进行额外配置。

### 使用方法

- 如果您需要启用 `host` 网络模式，请取消注释 `network_mode: host` 行。
- 保存修改后的 `docker-compose.yml` 文件，并使用以下命令启动服务：
- 这将根据您的配置启动 `qchatgpt` 服务！

```bash
docker-compose up -d
```

无报错即为启动成功，请查看`部署消息平台`部分以配置消息平台框架。

## [**注意**](https://qchatgpt.rockchin.top/posts/deploy/qchatgpt/docker.html#%E6%B3%A8%E6%84%8F)

- 安装的插件都会保存在`plugins`(映射到本目录`plugins`)，安装插件时可能会自动安装相应的依赖，此时若`重新创建`容器，已安装的插件将被加载，但所需的增量依赖并未安装，会导致引入问题。您可以删除插件目录后重启，再次安装插件，以便程序可以自动安装插件所需依赖。

## [**OneBot 11 协议**](https://qchatgpt.rockchin.top/posts/deploy/platforms/aiocqhttp/#onebot-11-%E5%8D%8F%E8%AE%AE)**反向wsNapCat**

OneBot 是用于接入多种消息平台的标准化协议，详细介绍：[**https://onebot.dev/open in new window**](https://onebot.dev/)

以下消息框架可以通过 OneBot 11 协议接入，需选择使用`aiocqhttp`作为适配器，修改`data/platform.json`配置文件，在`platform-adapters`字段中添加以下内容（如果已经有aiocqhttp的适配器，可以直接将其enable改为true）：

下面为**NapCat配置说明**

```json
{
    "adapter": "aiocqhttp",
    "enable": true,
    "host": "192.168.3.8",
    "port": 8080,
    "access-token": ""
}
```

![data/platform.json](https://cos.thelazy.cn/pictures/202405292250017.jpeg)

data/platform.json

当前可用的OneBot 11标准消息平台继续向下看完

## NapCat-Docker

## 配置

容器通过环境变量来配置，环境变量名称可以查看 [entrypoint](https://github.com/NapNeko/NapCat-Docker/blob/main/entrypoint.sh)👈

具体参数可参考[官方文档](https://napneko.github.io/zh-CN/guide/getting-started)

## 启动容器

## 反向 WS

```bash
docker run -d \
-e ACCOUNT=<机器人qq> \
-e WSR_ENABLE=true \
-e WS_URLS='["ws://192.168.3.8:5140/onebot"]' \
--name napcat \
--restart=always \
mlikiowa/napcat-docker:latest
```

```bash
# docker compose 反向 WS
version: "3"
services:
    napcat:
        environment:
            - ACCOUNT=<机器人qq>
            - WSR_ENABLE=true
            - WS_URLS=["ws://192.168.3.8:5140/onebot"]
        container_name: napcat
        network_mode: bridge
        ports:
           - 6099:6099
        restart: always
        image: mlikiowa/napcat-docker:latest
```

## 固化路径，方便下次直接快速登录

QQ 文档路径：~/.config/QQ

NapCat 配置文件路径: /usr/src/app/napcat/config

注意：如果是重新创建的容器，需要固定 Mac 地址

## 登录

```bash
docker logs napcat
```

## Tips

- 若 Docker 镜像拉取失败，可以使用 [Docker 镜像加速服务](https://github.com/dqzboy/Docker-Proxy)

## 反向ws对接

QChatGPT端口为8080 修改下方图中代码 示例:["ws://192.168.3.8:8080/ws"]

![配图](/upload/image-jtop.png)

## vnc可视化配置

转到此篇文章:[【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件-鑫仔博客 (xinz.fun)](https://www.xinz.fun/archives/1723791651891)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
