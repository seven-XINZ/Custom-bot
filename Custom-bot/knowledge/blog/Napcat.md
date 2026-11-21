# Docker安装Napcat反向ws

> 标题：Docker安装Napcat反向ws
> 分类：机器人Bot
> 标签：docker、Linux
> 原文：https://www.xinz.fun/archives/Napcat

> **导读**：这篇是「Docker安装Napcat反向ws」的实操教程。下文按「前言」「AI总结」「**自用命令可不能复制粘贴** 谢谢」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾机器人Bot的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 前言
2. AI总结
3. **自用命令可不能复制粘贴** 谢谢
4. 教程开始
5. 修改下列命令使用
6. **登陆基础配置介绍**[****](https://napneko.github.io/zh-CN/guide/config/basic#%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE%E4%BB%8B%E7%BB%8D)
7. 用** **WebUI** **配置****扫码****登陆 【浏览器】
8. 视频教程
9. 用文件配置 OneBot11 设置

## 前言

## AI总结

**全文摘要** 本文是一份关于如何使用Docker部署NapCat机器人的详细教程。它包括了如何修改Docker命令以适应个人需求，如何配置环境变量，以及如何通过WebUI和文件进行OneBot11设置。此外，还提供了如何进行NapCat的其他设置和官方文档链接。

**关键段落**

- **修改Docker命令**: 用户需要根据自己的需求修改Docker命令中的环境变量和端口映射，以确保容器能够正确运行。
- **参数解释**: 文章详细解释了Docker命令中每个参数的作用，如-d表示后台运行，-e用于设置环境变量等。
- **注意事项**: 提醒用户注意端口冲突和文件夹权限问题，确保环境变量和MAC地址的正确性。
- **WebUI配置**: 介绍了如何通过WebUI进行配置，包括如何访问WebUI，修改登录Token，以及如何通过公网或穿透进行远程配置。
- **OneBot11设置**: 说明了如何通过文件配置OneBot11，包括如何找到和修改配置文件，以及配置参数的具体含义。
- **NapCat其他设置**: 提供了NapCat的其他设置选项，如日志记录和日志等级。
- **官方文档和资源**: 文章最后提供了官方文档链接和相关资源，供用户进一步学习和参考。

## **自用命令可不能复制粘贴** 谢谢

```bash
docker run -d \
-e ACCOUNT="3863384238" \
-e NAPCAT_GID=0 \
-e NAPCAT_UID=0 \
-e MESSAGE_POST_FORMAT="string" \
-e WSR_ENABLE=true \
-e WS_URLS='["ws://172.17.0.1:5140/onebot","ws://172.17.0.1:9099/api/bot/qqws","ws://192.168.3.20:7000/onebot/v11/ws","ws://172.17.0.1:8080/ws"]' \
-p 6099:6099 \
-v /opt/1panel/apps/napcat/QQ:/app/.config/QQ \
-v /opt/1panel/apps/napcat/config:/app/napcat/config \
-v /opt/1panel/apps/napcat/logs:/app/napcat/logs \
--name napcat \
--mac-address=02:42:ac:11:00:99 \
mlikiowa/napcat-docker:latest
```

上面是自用命令需要根具你的需求自己配置**往下看仔细看**

## 教程开始

**--------------------------------------------------------------请认真阅读看完--------------------------------------------------------------**

**-- 注意仔细看 --- 请认真阅读看完----后期补充视频教程---------**

## 修改下列命令使用

```bash
docker run -d \
-e ACCOUNT="机器人qq" \
-e NAPCAT_GID=0 \
-e NAPCAT_UID=0 \
-e MESSAGE_POST_FORMAT="string" \
-e WSR_ENABLE=true \
-e WS_URLS='["ws://自己的ws ip加端口/api/bot/qqws"]' \ 
-p 6099:6099 \
-v /自己的目录只改这前面/QQ:/app/.config/QQ \
-v /自己的目录只改这前面/config:/app/napcat/config \
-v /自己的目录只改这前面/logs:/app/napcat/logs \
--name napcat \
--mac-address=02:42:ac:11:00:99 \
mlikiowa/napcat-docker:latest
```

### 参数解释

**--------------------------------------------------** **没有标注的地方可以默认不修改****-------------------------------------------------------**

- `-d`：以分离模式运行容器（即在后台运行）。
- `-e`：设置环境变量，这些变量将传递给容器内的应用程序。

  - `ACCOUNT`：设置账户信息。**填写自己的机器人QQ**
  - `NAPCAT_GID` 和 `NAPCAT_UID`：设置容器内的用户和组 ID。
  - `MESSAGE_POST_FORMAT`：设置消息的格式。
  - `WSR_ENABLE`：启用 WebSocket 连接。
  - `WS_URLS`：指定 WebSocket 服务器的 URL。**填写自己框架的ws地址 ws地址是自己框架的 请根据自己框架填写 默认不适用**
- `-p 6099:6099`：将主机的 6099 端口映射到容器的 6099 端口。
- `-v`：挂载卷，将主机的目录映射到容器内的指定路径。

  - `/opt/1panel/apps/napcat/QQ`：用于 QQ 配置。**/opt/1panel/apps/napcat将/****QQ****前面改为自己的路径**
  - `/opt/1panel/apps/napcat/config`：用于 Napcat 配置。**/opt/1panel/apps/napcat将/**config**前面改为自己的路径**
  - `/opt/1panel/apps/napcat/logs`：用于存放日志文件。**/opt/1panel/apps/napcat将/**logs**前面改为自己的路径**
- `--name napcat`：指定容器的名称。
- `--mac-address=02:42:ac:11:00:99`：为容器分配一个特定的 MAC 地址。 **如果要开多个自己改后面尾数** ~~--mac-address=02:42:ac:11:00:9~~**8** 9**7** 9**6** 都可以
- `mlikiowa/napcat-docker:latest`：要使用的 Docker 镜像。

### 注意事项

1. **端口冲突**：确保主机的 6099 端口没有被其他服务占用。如果已经被占用，您可以选择另一个可用的端口。
2. **文件夹权限**：确保您挂载的目录（如 `/opt/1panel/apps/napcat/QQ`、`/opt/1panel/apps/napcat/config` 和 `/opt/1panel/apps/napcat/logs`）具有适当的权限，以便容器能够读写这些目录。
3. **环境变量的正确性**：确保所有传递的环境变量（如 `ACCOUNT` 和 `WS_URLS`）都是正确的并符合您的需求。
4. **MAC 地址**：如果您指定了 MAC 地址，确保它是唯一的，并且不会与网络中的其他设备发生冲突。

### 直接在ssh登录

**复制命令到ssh**

```bash
docker logs napcat
```

## **登陆基础配置介绍**[****](https://napneko.github.io/zh-CN/guide/config/basic#%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE%E4%BB%8B%E7%BB%8D)

下文所指的 NapCat 的目录为 `${QQ 安装目录}/resource/app/app_launcher/napcat`，对于 `${QQ 安装目录}`，Linux 一般在 `/opt/QQ`；Windows 一般在 `<系统盘>:\Program Files\Tencent\QQNT`。

## 用** **WebUI** **配置****扫码****登陆 【浏览器】

仔细看

**--------------------------------------------------------------------------------------------------------------------------------------**仔细看

仔细看

1.如果你已经启动了 NapCat，并且有多于 1 个开放端口，则可以通过 WebUI 进行配置。

2.默认地址为 `0.0.0.0`，即监听所有地址。当配置了不可用的地址时 WebUI 将被禁用。

3.默认端口为 `6099`。当端口被设置为 `0` 时将禁用 WebUI。当端口被占用时，会自动对端口 +1，直到找到可用端口（最多尝试100次，失败则会禁用 WebUI），端口号会在启动日志中显示。

启动后可在启动日志中看到形如 `[WebUi] Login Token is xxxx` 的token信息，亦可打开 NapCat 的 `config` **目录下的我们**`挂载目录`就是文章一开始让大家创建的目录内就会生成一个`webui.json`的文件，我们可以在里面修改`token`，方便我们自己好记

![file](https://lmu5.com/wp-content/uploads/2024/08/20240815221647519077.webp)

![file](https://lmu5.com/wp-content/uploads/2024/08/20240815221704752844.webp)

仔细看

仔细看

仔细看

```json
{
    "host": "0.0.0.0", // WebUI 监听地址
    "port": 6099, // WebUI 端口
    "prefix": "", // WebUI 工作前缀，此项功能将在进阶配置中解释
    "token": "xxxx", //登录密钥，默认是自动生成的随机登录密码
    "loginRate": 3, //每分钟登录次数限制
}
```

**配置完成后，点击保存，重启即可生效。**

浏览器访问 `http://$host:$port$prefix/webui/login.html`，然后进行以下操作：

**改好后我们就可以利用**`公网`或者`穿透`，直接在外面就可以更改配置，记得端口噢！`尾巴要带webui才可`。比如：`http://192.168.10.197:6110/webui`,记得在地址后面加 **/webui** 接着输入你上面设定的token，或者他自带的token,就能访问了。
[![file](https://lmu5.com/wp-content/uploads/2024/08/20240815221904945964.webp "【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 114")](https://lmu5.com/wp-content/uploads/2024/08/20240815221904945964.webp)
[![file](https://lmu5.com/wp-content/uploads/2024/08/20240815222048157960.webp "【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 115")](https://lmu5.com/wp-content/uploads/2024/08/20240815222048157960.webp)

**配置完成后，点击保存，重启登陆后即可生效。**。

## 视频教程

实在不明白跟着视频走

## 用文件配置 OneBot11 设置

和上面一样，**配置完成后，点击保存，重启登陆后即可生效。**。

打开 NapCat 的 `config` 目录，找到名为 `onebot11_<你的QQ号>.json` 的文件，如 `onebot11_1234567.json`；如果没有此文件可以复制 `onebot11.json` 重命名为 `onebot11_<你的QQ号>.json`。

![file](https://lmu5.com/wp-content/uploads/2024/08/20240815222222217086.webp)

![file](https://lmu5.com/wp-content/uploads/2024/08/20240815222336604186.webp)

下面是配置内容参数解释：

```json
{
  "http": {
    // 是否启用http服务, true为启动，false为禁用
    "enable": false,
    // HTTP服务监听的 ip 地址，为空则监听所有地址
    "host": "",
    // http服务端口
    "port": 3000,
    // http上报密钥，可为空
    "secret": "",
    // 是否启用http心跳
    "enableHeart": false,
    // 是否启用http上报服务
    "enablePost": false,
    // http上报地址, 如["http://127.0.0.1:8080/onebot/v11/http"]
    "postUrls": []
  },
  "ws": {
    // 是否启用正向websocket服务
    "enable": false,
    // 正向websocket服务监听的 ip 地址，为空则监听所有地址
    "host": "",
    // 正向websocket服务端口
    // 当port与http服务port一致时，host也需与http服务host保持一致，否则可能会导致启动失败
    "port": 3001
  },
  "reverseWs": {
    // 是否启用反向websocket服务
    "enable": false,
    // 反向websocket对接的地址, 如["ws://127.0.0.1:8080/onebot/v11/ws"]
    "urls": []
  },
  "GroupLocalTime": {
    "Record": false,//是否开启本地群聊时间记录
    "RecordList": []//开启全部群 ["-1"]  单个群配置 ["11111"] 多个群 ["1","2","3"]
  },
  // 是否开启调试模式，开启后上报消息会携带一个raw字段，为原始消息内容
  "debug": false,
  // ws心跳间隔，单位毫秒
  "heartInterval": 30000,
  // 消息上报格式，array为消息组，string为cq码字符串
  "messagePostFormat": "array",
  // 是否将本地文件转换为URL，如果获取不到url则使用base64字段返回文件内容
  "enableLocalFile2Url": true,
  // 音乐签名URL，用于处理音乐相关请求
  "musicSignUrl": "",
  // 是否上报自己发送的消息
  "reportSelfMessage": false,
  // access_token，可以为空
  "token": ""
}
```

**请勿将注释内容写入配置文件，否则会导致配置文件解析失败**。

#### 配置 NapCat 其它设置（如果不懂干嘛，不用看啦）

启动登录 NapCat 后，打开 NapCat 的 `config` 目录，找到名为 `napcat_<你的QQ号>.json` 的文件，如 `napcat_1234567.json`。

配置内容参数解释：

```json
{
  // 是否开启文件日志
  "fileLog": true,
  // 是否开启控制台日志
  "consoleLog": true,
  // 日志等级, 可选值: debug, info, error
  "fileLogLevel": "debug",
  "consoleLogLevel": "info"
}
```

**请勿将注释内容写入配置文件，否则会导致配置文件解析失败。**

#### 官方文档:

[仓库地址](https://github.com/NapNeko/NapCatQQ) [官方文档](https://napneko.github.io/zh-CN/)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
