# 【NTQQ】Docker版本NTQQ结合了LiteLoaderQQNT与LLonebot等插件

> 分类：机器人Bot
> 标签：api、docker、nas、群晖、ubuntu
> 原文：https://www.xinz.fun/archives/LiteLoaderQQNT-LLonebot

> **导读**：这篇围绕「【NTQQ】Docker版本NTQQ结合了LiteLoaderQQNT与LLonebot等插件」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾机器人Bot的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 前言
2. 准备
3. NTQQ相关

本文介绍了如何在服务器上搭建NTQQ机器人，通过官方NTQQ对接各框架，实现QQ登录的稳定运行。文章提到了需要准备一台服务器和相应的软件，并详细描述了通过SSH链接服务器、创建文件夹和配置文件、编辑配置文件地址端口、运行容器等步骤。同时，文章还介绍了VNC连接的使用和配置，以及使用watchtower进行NTQQ的更新。文章总结起来就是在服务器上搭建NTQQ机器人，实现QQ登录的稳定性和自动登录功能，同时提供了更新和维护的方法。

## 前言

**相信很多机器人玩家，都已经无路可去了，目前可以利用官方NTQQ来对接各框架（当然需要各框架支持）**
**首先感谢** `青柠` 博客地址：[倾城于你](https://qninq.cn/) 提供的一些思路。
**感谢 群内**`魂焱` 博客地址：[魂焱小站](https://www.hunyan6.cn/)提供部分技术的支持。
**感谢 群内**`莫斯科`的arm服务器提供。

**打包的docker在魂焱打包的基础上改了一些，让QQ就算闪退或者崩溃，不影响到容器本身，用**`supervisor`进行守护，使其配合自动登录功能，实现绝对的稳定，下面我们来进入正题

## 准备

使用文字转语音自用推荐:[TTS适配海豚Ai TTS-Online](https://www.ttson.cn/?source=falPMO)

1. **准备一台服务器，**`amd64/arm64`都可以，配置最好还是2核保底吧。
2. **准备一个**`VNC`软件。我会在群内准备一些手机上的和PC端的。这里直接用青柠提供的`1Remote`
3. **准备手机登陆机器人**`QQ号`，扫码

## NTQQ相关
### NTQQ一键脚本（适用于小白支持autMan/无界）

**复制以下代码，在服务器发送即可。按照提示步骤**`输入正确参数`，如果出现输错可以自行去文件夹内`修改`！（如果`脚本有问题`，欢迎加`Q群反馈`，找时间会优化。）搞好后就跳转下面的`VNC连接`接着连接操作

```
cd && curl -o "ntqq.sh" "https://raw.githubusercontent.com/baquanluomu/ntapiconfig/main/ntqq.sh" && chmod +x ntqq.sh && ./ntqq.sh
```

**示例图：**

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221624265832.webp " alt="20240625221624267000" />


### 手动搭建NTQQ（建议老手）

1. **SSH链接你的服务器，在**`root`目录下，没有的请`cd /root`，然后输入下面命令创建对应文件夹并创建配置文件，请注意将`记得换`文字换成机器人的`QQ号码`

   ```
   mkdir -p LLOneBot && cd LLOneBot && touch config_记得换.json
   ```

   **Copy**

   请把记得换更改为机器人QQ号码
2. **如果不确定是否成功，可以自行查看下目录或者**`ll`看查目录。正确后我们进行编辑配置文件，配置地址端口。（并不是一定要`vi`如果有宝塔等或者nas等可以直接去目录手动修改哈，怎么方便怎么来）,这里我直接使用了SSH工具查看json文件，

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221619754739.webp " alt="20240625221619753000" />

3. **上面进入后，我们双击里面的对应机器人QQ的配置文件打开，然后编辑箭头所指那一串，如果你的NTQQ跟你的框架是一起的，也可以用10.10.10.10或者127.0.0.1和192.xx.xx.xx都是可行的**
```
{
  "enableLLOB": true,
  "ob11": {
    "httpPort": 3000,
    "httpHosts": [],
    "httpSecret": "",
    "wsPort": 3001,
    "wsHosts": [
      "ws://autmanIP:端口/qq/receive"
    ],
    "enableHttp": false,
    "enableHttpPost": false,
    "enableWs": false,
    "enableWsReverse": true,
    "messagePostFormat": "string",
    "enableHttpHeart": false,
    "enableQOAutoQuote": false
  },
  "heartInterval": 60000,
  "token": "",
  "enableLocalFile2Url": true,
  "debug": true,
  "log": false,
  "reportSelfMessage": false,
  "autoDeleteFile": true,
  "autoDeleteFileSecond": 60,
  "enablePoke": false,
  "musicSignUrl": ""
}
```
<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221705424421.webp " alt="20240625221705425000" />


**编辑改好后，咋们记得保存，拉取镜像并run容器（不用管arm或者amd什么的，直接拉取，会自动识别）**
```
docker run -d  --restart=always --name NTQQ  -v /root/LLOneBot/:/opt/QQ/resources/app/LiteLoaderQQNT/data/LLOneBot/ -p 5900:5900 -p 3000:3000 luomubiji/ntqq:latest
```
<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221702526554.webp " alt="20240625221702525000" />


5. **注意上面的name后面的**`NTQQ`是可以更改的，还有`-p 5900:5900 -p 3000:3000` 这里的`:`前面的`5900`和`3000`是可以更改的，更改后代表后面的步骤都需要相应的替换。如果有端口冲突，还是更改为好，没有就不必更改，有没有很简单，自己用命令`lsof -i:5900`查看记得

## **VNC连接**

1. **首先VNC软件选择性很多，各个功能不一样，建所以这里直接用**`1Remote`来演示，首先打开软件，右上角选择`+`号，选择添加，点击上方`VNC`，输入名称

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221625693974.webp " alt="20240625221625692000" />


<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221630286988.webp " alt="20240625221630288000" />


VNC密码是：vncpasswd

2. **往下拉找到地址，输入上面搭建**`NTQQ服务器的地址IP（可域名）+端口号`，就是上面的第六步，里面的`5900`如果你有变动，改的什么就在此处填写什么（家宽openwrt或者爱快等，记得开放端口）。下面密码输入：`vncpasswd` (关于密码固定后续可能会优化为可自定义)，然后保存。

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221632421860.webp " alt="20240625221632420000" />

3. **保存后我们去双击你添加的，就会进行连接（如果遇到连接失败，你确定端口开放！且确定容器正常运行中！端口占用等问题！），连接成功后如图所示：**

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221643330615.webp " alt="20240625221643330000" />

4. **然后我们拿出我们准备好的机器人QQ手机，右上角**`+`号，扫一扫，然后扫出来的二维码。并登陆，确定登录。出现确认最好`勾选下次登录无需手机确认`，如果遇到闪退，扫码后黑屏等，`重新连接VNC`就行。直到出现正常QQ登陆界面。然后就进行`关键操作`！！！

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625222934903934.webp " alt="20240625222934905000" />


关键操作！

无界用户拉到最下查看下图1的反向设置，其他不变

**点击设置，找到左边最下面的bot，点击进入，确定一下端口，还有对接奥特曼的地址和端口是否有，如果没有，手动填写，最好是去一开始的配置文件修改！还要开启debug！消息上保类型选择CQ码如图所示就完事了！然后点击左边的**`登录设置`，将启动QQ自动登录`打开`，确认无需手机确认`打开`。接着找到最上的`通用`找到`软件更新关闭`！！

autMan用户配置如图，IP+端口记得替换

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221649306479.webp " alt="20240625221649306000" />


<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221652371570.webp " alt="20240625221652374000" />


<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221656138387.webp " alt="20240625221656138000" />


## **无界用户配置**

1. **NTQQ相关第3步的配置文件：**
```
{
  "enableLLOB": true,
  "ob11": {
    "httpPort": 3000,
    "httpHosts": [],
    "httpSecret": "",
    "wsPort": 3001,
    "wsHosts": [
      "ws://无界IP:端口/api/bot/qqws"
    ],
    "enableHttp": false,
    "enableHttpPost": false,
    "enableWs": false,
    "enableWsReverse": true,
    "messagePostFormat": "string",
    "enableHttpHeart": false,
    "enableQOAutoQuote": false
  },
  "heartInterval": 60000,
  "token": "",
  "enableLocalFile2Url": true,
  "debug": true,
  "log": false,
  "reportSelfMessage": false,
  "autoDeleteFile": true,
  "autoDeleteFileSecond": 60,
  "enablePoke": false,
  "musicSignUrl": ""
}
```
2. **VNC连接第5步图一示例：**

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625223202146066.webp " alt="20240625223202144000" />

3. **无界web更改**`qqOutside.js`示例图，请将`适配器模式更改为ws`,交互发送地址更改为`NTQQ的地址加端口`，记得`开启适配器`，图上没开而已，js路径在`/bncr/BncrData/Adapter`

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625223255811988.webp " alt="20240625223255810000" />


## **更新命令**

**这里使用的是watchtower来更新，但是我不知道是个人原因还是什么原因，watchtower版本无论怎么拉取最新的都是1.3.0（删除了镜像也是），所以我建议如果您的watchtower版本很低的话，就是用下面命令拉取后出现第一行为1.7.1（2024年3月14日 23:18:12目前最新）以下的话，最好还是手搓拉取指定版本，注意更新是要时间的！且更新后还需要扫码登录，且要除了配置文件外的比如自动登录，取消更新都需要重新开关！**

尾巴的NTQQ是容器名字！！！！

### NTQQ指定用watchtower1.7.1更新（跟我类似情况）
```
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower:1.7.1 -c --run-once  NTQQ
```
### NTQQ通用更新命令
```
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower -c --run-once NTQQ
```

转载至作者：落幕

链接：<https://lmu5.com/ntqq.html>

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
