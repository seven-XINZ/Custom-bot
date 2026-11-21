# 无界bncr安装使用及开发适配

> 分类：代理与穿透
> 标签：QQ、bot、bncr
> 原文：https://www.xinz.fun/archives/bncr-KF

> **导读**：这篇是「无界bncr安装使用及开发适配」的实操教程。下文按「（无界）Bncr介绍」「项目介绍」「官方简介」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾代理与穿透的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. （无界）Bncr介绍
2. 项目介绍
3. 官方简介
4. 安装前
5. 配置免费阿里云docker加速
6. 阿里云
7. 安装开始
8. 启动服务
9. 更新
10. 查看日志
11. 进入容器控制台
12. 进入容器命令行
13. 以及其余 3 个小节

## （无界）Bncr介绍
## 项目介绍

- **项目地址：**[**https://github.com/Anmours/Bncr**](https://github.com/Anmours/Bncr)
- **开发文档：**[**https://anmours.github.io/Bncr/**](https://anmours.github.io/Bncr/)

- 使用文字转语音自用推荐:[TTS适配海豚Ai TTS-Online](https://www.ttson.cn/?source=falPMO)
- [ChatAI大聪明交流群](https://qm.qq.com/q/6BqfPZ7vXO)

## 官方简介

**Bncr 是一个开箱即用的Nodejs Chat RoBot（会话式机器人）框架。它基于OOP函数响应式编程，具有占用小、响应快、开发易等特点，允许开发者创建高度可测试、可扩展、松散耦合且易于维护的应用程序。本项目架构深受Koishi与sillyGirl的启发；**

### 特性

- **多平台多账户接入系统 ： 2个qq/3个wx/4个tg? so easy!；**
- **基于TypeScritp OOP函数响应式编程 ：源码仅1.5M，占用小，响应快，开发易 ；**
- **极简的插件开发 ： 系统高度封装，提供简便人性化的系统方法，随心所欲开发插件；**
- **异步同步执行自由控制 ： 基于nodejs async/await/Promise特性，你可以自由控制异步同步（阻塞非阻塞运行）；**
- **不仅仅是Chat RoBot ： 原生支持npm/yarn，开发潜力无穷大，如果你愿意，可以在本框架上搭建网站、图片服务器、资源共享平台、并发请求等服务，在JavaScript上能做到的事情在这里都将被实现.**

比较常用的插件/功能：

- 奶酪棒插件--对接青龙：获取|删除 配置文件，环境变量 删除|禁用|启用|查找|移动，任务 运行|停止|启用|禁用|状态|置顶|取消置顶|添加|修改|删除|日志。
- 登录插件--对接ark，rabbit扫码，pro扫码、短信登录。
- 店铺抽豆监控。
- 店铺签到监控。
- 可迁移傻妞到Bncr。
- Bncr SPY 监控变量。

目前仅支持**docker安装**

## 安装前

## 配置免费阿里云docker加速

由于部分国内镜像站被通知关闭，部分人出现拉取镜像不成功的情况，所以需要配置docker加速。

本教程使用系统：debian12

1.10.0以上版本的Docker客户端

## 阿里云

登录阿里云 搜索“容器镜像服务”，进入控制台。

<img src="https://thin-hill-428.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fab86454e-d8fc-47db-8b72-d95ac7149dba%2Fbe638cfa-31df-468f-85ce-4916aa78b9b2%2FUntitled.png?table=block&id=99bee878-f72e-40a8-b425-32a1e91a9062&spaceId=ab86454e-d8fc-47db-8b72-d95ac7149dba&width=1420&userId=&cache=v2" alt="配图" />

<img src="https://thin-hill-428.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fab86454e-d8fc-47db-8b72-d95ac7149dba%2Fad3a81cf-0a4e-4c4d-bedc-290d55be960f%2FUntitled.png?table=block&id=1c350ebb-b0e7-4b92-a644-17e4b815e529&spaceId=ab86454e-d8fc-47db-8b72-d95ac7149dba&width=1990&userId=&cache=v2" alt="配图" />


保存好你的加速器地址。

打开FinalShell连接上设备。打开/etc/docker/daemon.json (某些版本是conf文件，是一样的)

如果没有这个文件就新建一个 输入以下内容保存。

<img src="https://thin-hill-428.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fab86454e-d8fc-47db-8b72-d95ac7149dba%2Fa74b8762-afef-42a5-a0d9-060c1fd3f90a%2FUntitled.png?table=block&id=a4590654-7432-477d-a536-eb66772e99b1&spaceId=ab86454e-d8fc-47db-8b72-d95ac7149dba&width=1880&userId=&cache=v2" alt="配图" />


```
{
    "registry-mirrors": [
        "阿里云加速器地址",
    ]
}
```

保存好后重启Docker

```
sudo systemctl daemon-reload
sudo systemctl restart docker
```

（无错误可忽略）如果重启Docker失败，如下图情况，将daemon.json，改成**daemon.conf**重启即可。

## 安装开始

1. `# 在你要存放数据的目录下手动新建BncrData文件夹`
2. `# (以root目录为例)`
3. `# 警告！群晖用户请勿在root下存放任何文件！修改成你的硬盘目录！`
4. `mkdir /root/BncrData #在root目录新建BncrData文件夹`
5. `# 拉取并运行容器 并进入交互控制台`

```
docker run -dit \
 -v /sata/1panel/apps/BncrData:/bncr/BncrData \
 -p 9099:9090 \
 --name bncr \
 --hostname bncr \
 --restart on-failure:5 \
 --log-opt max-size=5m \
 --log-opt max-file=3 \
anmour/bncr && docker attach bncr
```

```
version: '3.8'  # 指定 Docker Compose 文件的版本

services:  # 定义服务
  bncr:  # 服务名称
    image: anmour/bncr  # 使用的 Docker 镜像
    container_name: bncr  # 容器名称
    hostname: bncr  # 容器的主机名
    restart: on-failure:5  # 重启策略，最多重启 5 次
    ports:  # 端口映射
      - "9090:9090"  # 将主机的 9090 端口映射到容器的 9090 端口
    volumes:  # 数据卷挂载
      - /root/BncrData:/bncr/BncrData  # 将主机的目录挂载到容器内
    logging:  # 日志配置
      driver: "json-file"  # 使用 json-file 日志驱动
      options:  # 日志选项
        max-size: "5m"  # 日志文件的最大大小
        max-file: "3"  # 保留的日志文件数量
    tty: true  # 允许容器运行终端
    stdin_open: true  # 保持标准输入打开，以便于 attach
```

## 启动服务

将上述内容保存为 `docker-compose.yml` 文件，然后在命令行中运行以下命令启动服务：

```
docker-compose up -d
```

如果需要附加到容器，可以使用：

```
docker attach bncr
```

## 更新

```
docker run --rm \
 -v /var/run/docker.sock:/var/run/docker.sock \
 containrrr/watchtower \
 -c --run-once \
bncr
```

## 查看日志

```
docker logs bncr
```

## 进入容器控制台

```
#进入
docker attach bncr
# 退出attach
Ctrl+p Ctrl+q
```

## 进入容器命令行

```
docker exec -it bncr /bin/sh
```

初次启动会在你映射的宿主机路径下创建5个文件夹，分别为 `Adapter` `config` `public` `db` `plugins` `config` 下会自动生成一些启动所需的配置文件，已进行详细注释，根据自己情况来填写；

`Adapter`下会自带 `tgbot、HumanTG 、qqbot、wxKeAImao、wxQianxun`以及系统适配器；

`public` 为静态资源目录，你可以在里边放一些文件，通过 `http://ip:9090/public/文件名`来访问这些资源

`db` 为系统数据库存放目录

`plugins` 插件目录，自带一些官方插件

会自动启动无界,启动无界后会提示输入鉴权URL，在下方链接选一个即可。

```
目前可用URL

<http://bncr.619030.xyz:2082>
<http://bncr.888862.xyz>
<http://future.free.hr:2082>
<https://rebncr.dsdog.tk>
<http://wj.yanyuwangluo.cn>
```

## 配置Bncr
### 基本配置

- Token获取

1. 先私聊 **https://t.me/red\_Lights\_Districts\_Bot**  ,否者收不到消息，然后BncrJS里发 **/get\_token**
   复制token填入config
2. 把要对接的平台开关**enable**改为**true**
3. 重启

然后把刚刚机器人获取的token输入。

其他的可以按默认选项回车即可。FinalShell不要关闭。

## 基础命令

```
//设置qq管理员 其他平台类似
set qq admin 12345698
//获取数据库
get 表 key
//例如获取管理员
get qq admin
// 设置数据库
set 表 key value
// 重启机器
重启
//获取时间
time
//启动时间
启动时间
//获取机器码
机器码
//获取版本
bncr版本
// 获取群id
群id
//获取个人id
我的id
//监听群消息 （默认屏蔽所有群）
监听该群
//屏蔽群消息
屏蔽该群
//不回复该群
不回复该群
//回复
回复该群
```

## 常见问题

> ## **为什么不回复消息，发消息没反应**

- 当发送管理员命令没有反应时，请检查管理员是否正确
- 步骤:

  - 对着机器人发 '我的id' 机器人会回复你的id然后设置一下管理员(见下文)
  - 注意! 管理员命令需要在有管理员权限的平台操作，不然无效
  - 不知道哪个平台有管理员权限的，docker attach bncr 后在控制台发

```
//设置qq管理员 其他平台类似
set qq admin 12345698
set wxKeAImao admin 12345698
set wxQianxun admin 12345698
set wxXyo admin 12345698
set tgBot admin 12345698
set HumanTG admin 12345698
```

> 当群友在群里发消息机器人没有任何回应时，说明你没对群监听

- 快捷操作

  - 管理员在群聊中发送 '监听该群' 即可响应群友消息
  - 发送 '屏蔽该群' 取消监听
  - 发送 '不回复该群' 监听消息但是不会回复任何消息
  - '回复该群' 恢复默认
- 手动设置上诉效果

```
// 监听tg频道，或者手动设置监听群
set groupWhitelist 平台名:id true
// 栗子，监听一个频道
set groupWhitelist HumanTG:-1001744932665 true
// 删除监听(屏蔽该频道)
del groupWhitelist HumanTG:-1001744932665
// 不回复手动
set noReplylist HumanTG:-1001744932665 true
// 回复手动
set noReplylist HumanTG:-1001744932665 false
或
del noReplylist HumanTG:-1001744932665
```

> # NO.2 插件安装
>
> ### 订阅厂库

>
> ```
> 订阅链接:https://github.com/seven-XINZ/bncr
> ```
>
> 仓库:github
>
> 鑫仔
>
> ### 第一步 下载插件安装依赖
>
> 在FinalShell内输入
>
> ```
> docker attach bncr
> ```
>
> 然后去无界web页面。
>
> 在插件市场内添加哆啦A梦的订阅
>
> ```
> bncrSub://UpdjUc6jid/ZFkJhEZFTW0zFEYpg7ZPidkatlTM6OSN/bOxWaExKe5VQ14AHsy+0ufSXlKVuOuRYAqkTz7a2Z3dS8aW8mj6O8MsZVFDHMpc=
> ```
>
>

<img src="https://thin-hill-428.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fab86454e-d8fc-47db-8b72-d95ac7149dba%2F70b62cd0-7023-4de0-9215-5dd042a7b78e%2FUntitled.png?table=block&id=3c55f403-54e4-48ed-8c8b-76cb4bc72ec5&spaceId=ab86454e-d8fc-47db-8b72-d95ac7149dba&width=1420&userId=&cache=v2" alt="配图" />

>
>

<img src="https://thin-hill-428.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fab86454e-d8fc-47db-8b72-d95ac7149dba%2F9602c56c-944e-4820-a5ed-3130efc23ec9%2FUntitled.png?table=block&id=cbc5453d-1d42-4f4c-9ddd-05cba39547ed&spaceId=ab86454e-d8fc-47db-8b72-d95ac7149dba&width=1420&userId=&cache=v2" alt="配图" />

>
> 保存后刷新页面，点击插件卡片右上角的下载图标下载插件，一个个下载完即可。
>
> ```
> Doraemon_config_tool.js
> Doraemon_sendNotify.ts
> Doraemon_tool.js
> Doraemon_一键安装所需依赖.js
> Doraemon_ql.js
> h5st.js
> Rebels_H.js
> Rebels_jdCommon.js
> redis_tool.js
> wx_active_tool.js
> 查询.js
> 登录.js
> ```
>
> 下载完后在FinalShell输入“重启”，重启无界。
>
> 重启后在FinalShell中输入 `*Doraemon_一键安装所需依赖` 等待依赖安装完成。安装完成后输入”重启”\*
>
> 留意重启的界面显示，如无报错则安装成功。
>
> **显示未设置@name丨@rule丨@admin 插件加载异常**

- 检查插件文件夹是否放入正确：
- 插件保存至bncr 的 **BncrData/plugins/红灯区/**下

> ##
>
> **Error: Cannot find module './xxxxx'**

- 插件文件夹下没有**mod**文件，或缺少自定义模块，谁写的插件找谁要这些模块,一般对应的插件仓库都有的,是你没装好!
- 下载 https://github.com/RedLightsDistrict/Bncr\_plugins 链接中的mod放入到红灯区下

> **Error: Cannot find module 'xxxxx'**

- 统一为缺少npm模块,通过管理员对机器人发送 npm i xxxx 命令安装模块后重启即可解决

> **查询没有反应**

- 安装依赖
```
 docker exec -it bncr /bin/sh
    cd BncrData
    npm i got@11.8.5 crypto-js
```
# NO.3 对接青龙,TgBot/人形

**青龙面板**是必须对接的，TgBot和人形自己选一个吧，都行。还有QQ微信啥的都可以，QQ微信我就不搞了，容易被封。微信公众号的话也是可以的。

老样子 先打开FInalShell 然后docker attach bncr进入交互页面。

### 对接青龙面板

打开网页 <https://github.com/RedLightsDistrict/Bncr_plugins> 点击下载zip包

<img src="https://thin-hill-428.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fab86454e-d8fc-47db-8b72-d95ac7149dba%2Fdd1c843a-939d-4255-895f-9bc3ef7f1740%2FUntitled.png?table=block&id=c663e113-948d-4456-b558-48f99ecdc319&spaceId=ab86454e-d8fc-47db-8b72-d95ac7149dba&width=1990&userId=&cache=v2" alt="配图" />


下载完解压后打开 奶酪.js 修改第四行origin为team

<img src="https://thin-hill-428.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fab86454e-d8fc-47db-8b72-d95ac7149dba%2F481dc09c-e85a-419f-b437-2b3c2eb363e1%2FUntitled.png?table=block&id=9d077b6f-024c-4bfa-886f-e3214bec7c08&spaceId=ab86454e-d8fc-47db-8b72-d95ac7149dba&width=1990&userId=&cache=v2" alt="配图" />


将奶酪.js和mod文件夹拖入/root/BncrData/plugins/红灯区 然后重启

<img src="https://thin-hill-428.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fab86454e-d8fc-47db-8b72-d95ac7149dba%2Fe6c4342c-a12f-41d6-9d2f-113eae06257d%2FUntitled.png?table=block&id=2accef17-6d1e-4940-80cd-e2579f872e7a&spaceId=ab86454e-d8fc-47db-8b72-d95ac7149dba&width=1990&userId=&cache=v2" alt="配图" />


重启完成后打开青龙面板-系统设置-应用设置 为无界创建一个应用。

<img src="https://thin-hill-428.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fab86454e-d8fc-47db-8b72-d95ac7149dba%2Fb54c66d1-767f-4ba7-81c8-45c50dccd700%2FUntitled.png?table=block&id=ee268994-a4cf-41cf-84e6-a1aa3b19f93b&spaceId=ab86454e-d8fc-47db-8b72-d95ac7149dba&width=1990&userId=&cache=v2" alt="配图" />


打开无界网页端，右下角的web交互页面，输入”面板管理”按提示输入即可。

添加完面板后把ABCD的面板都设置好。

<img src="https://thin-hill-428.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fab86454e-d8fc-47db-8b72-d95ac7149dba%2Fae2bb0c5-565f-48d8-9971-99b063345484%2FUntitled.png?table=block&id=e4b43624-ea81-4a50-9f59-665c77dc61f7&spaceId=ab86454e-d8fc-47db-8b72-d95ac7149dba&width=1990&userId=&cache=v2" alt="配图" />


## 对接TgBot

**注意：必须要有一个域名才可使用反代。**

打开TG,到@BotFather 中创建一个bot，记住token。

## 反向代理设置

推荐cf的worker，详细教程上网去搜，注意三点即可。

1、必须要域名，几块钱一年的也行，cf提供的免费域名不行。

2、设置完worker以后要设置路由。

3、忘了

<https://www.cloudflare.com/zh-cn/>

下面贴一下我的worker代码，注意修改第一行即可。XXXXX是你Bot token的数字部分，其他不变，要带/bot和：
```
const whitelist = ["/botXXXXXXX:"];
const tg_host = "api.telegram.org";
addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request))
})
function validate(path) {
    for (var i = 0; i < whitelist.length; i++) {
        if (path.startsWith(whitelist[i]))
            return true;
    }
    return false;
}
async function handleRequest(request) {
    var u = new URL(request.url);
    u.host = tg_host;
    if (!validate(u.pathname))
        return new Response('Unauthorized', {
            status: 403
        });
    var req = new Request(u, {
        method: request.method,
        headers: request.headers,
        body: request.body
    });
    const result = await fetch(req);
    return result;
}
```
准备好反代和token，到无界插件市场下载tgbot.js 然后在FinalShell输入“重启”

重启完成后在无界插件配置下打开适配器，然后输入反代和token，再重启。

<img src="https://thin-hill-428.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fab86454e-d8fc-47db-8b72-d95ac7149dba%2Fc075a4fd-a120-462e-85e8-f4cee4367036%2FUntitled.png?table=block&id=d81b594a-8222-440e-94e2-217f5bab6788&spaceId=ab86454e-d8fc-47db-8b72-d95ac7149dba&width=1990&userId=&cache=v2" alt="配图" />


重启完成后,设置好tg管理员即可。
```
set tgBot admin 管理员ID
```
## 对接TG人形

必须有国外鸡或者clash。

如何申请apiID和apiHash自己上网搜，如果多次出现error就换节点。

插件市场下载适配器HumanTG.js，填写上面获取的apiID和apiHash，代理配置选填，保存，重启无界

# N0.4 无界spy和监听配置

无界spy可以代替spy，**使用前必须对接了青龙面板，TgBot或者人形**。

## 配置变量

上期教程我们下载了红灯区的zip包，没下的再下一遍。

<https://github.com/RedLightsDistrict/Bncr_plugins>

下载完我们打开Bncr\_spy.js 改一下第4行origin到team，不知道要不要改，我改了反正

<img src="https://thin-hill-428.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fab86454e-d8fc-47db-8b72-d95ac7149dba%2F4372ea42-fcd2-464f-bc1c-52be71cb0a6b%2FUntitled.png?table=block&id=a028e396-61e9-4007-9126-9fe3727e53a4&spaceId=ab86454e-d8fc-47db-8b72-d95ac7149dba&width=1990&userId=&cache=v2" alt="配图" />


改完以后打开mod下的SpyConfig.js 改为适配Faker库的监听配置。配置是Faker3库的，Faker2的自己改一下就行。

### **最下方的运行日志输出自己按需修改下。**
```
let RspyList = {
    /* 监控信息配置Faker*/
    SpyList:[
      {
    "Name": "【Faker】完善信息有礼（超级会员）",
    "Script": "shufflewzc_faker3_main/jd_completeInfoActivity.js",
    "ListenEnv": ['jd_completeInfoActivity_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】每日抢好礼（超级无线/超级会员）",
    "Script": "shufflewzc_faker3_main/jd_daily.js",
    "ListenEnv": ['jd_daily_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】大牌联合 - 浏览",
    "Script": "shufflewzc_faker3_main/jd_dplh_viewShop.js",
    "ListenEnv": ['jd_dplh_viewShop_ids'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】批量店铺签到（活动查询）",
    "Script": "shufflewzc_faker3_main/jd_dpqd_main.js",
    "ListenEnv": ['jd_dpqd_tokens'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】店铺抽奖中心（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_drawCenter.js",
    "ListenEnv": ['jd_drawCenter_activityId'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】店铺关注有礼",
    "Script": "shufflewzc_faker3_main/jd_drawShopGift.js",
    "ListenEnv": ['jd_drawShopGift_argv'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】粉丝福利红包",
    "Script": "shufflewzc_faker3_main/jd_fansDraw.js",
    "ListenEnv": ['jd_fansDraw_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】关注有礼（无线营销）",
    "Script": "shufflewzc_faker3_main/jd_gzsl_contactWare.js",
    "ListenEnv": ['jd_gzsl_contactWare_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】幸运大转盘（无线营销）",
    "Script": "shufflewzc_faker3_main/jd_gzsl_getLottery.js",
    "ListenEnv": ['jd_gzsl_getLottery_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】店铺礼包（无线营销）",
    "Script": "shufflewzc_faker3_main/jd_gzsl_shopGiftBag.js",
    "ListenEnv": ['jd_gzsl_shopGiftBag_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】积分兑换（京耕）",
    "Script": "shufflewzc_faker3_main/jd_jinggeng_exchangeActDetail.js",
    "ListenEnv": ['jd_jinggeng_exchangeActDetail_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】盖楼有礼（京耕）",
    "Script": "shufflewzc_faker3_main/jd_jinggeng_floor.js",
    "ListenEnv": ['jd_jinggeng_floor_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】惊喜开盲盒（京耕）",
    "Script": "shufflewzc_faker3_main/jd_jinggeng_loadBlindBox.js",
    "ListenEnv": ['jd_jinggeng_loadBlindBox_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】加购有礼（京耕）",
    "Script": "shufflewzc_faker3_main/jd_jinggeng_showCart.js",
    "ListenEnv": ['jd_jinggeng_showCart_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】积分抽奖（京耕）",
    "Script": "shufflewzc_faker3_main/jd_jinggeng_showDrawOne.js",
    "ListenEnv": ['jd_jinggeng_showDrawOne_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】关注店铺有礼（京耕）",
    "Script": "shufflewzc_faker3_main/jd_jinggeng_showFavoriteShop.js",
    "ListenEnv": ['jd_jinggeng_showFavoriteShop_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】邀请入会赢好礼（京耕）",
    "Script": "shufflewzc_faker3_main/jd_jinggeng_showInviteJoin.js",
    "ListenEnv": ['jd_jinggeng_showInviteJoin_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】组队瓜分奖品（京耕）",
    "Script": "shufflewzc_faker3_main/jd_jinggeng_showPartition.js",
    "ListenEnv": ['jd_jinggeng_showPartition_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】完善有礼（京耕）",
    "Script": "shufflewzc_faker3_main/jd_jinggeng_showPerfectInformation.js",
    "ListenEnv": ['jd_jinggeng_showPerfectInformation_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】签到有礼（京耕）",
    "Script": "shufflewzc_faker3_main/jd_jinggeng_showSign.js",
    "ListenEnv": ['jd_jinggeng_showSign_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】幸运抽奖（京耕）",
    "Script": "shufflewzc_faker3_main/jd_jinggeng_showTaskDraw.js",
    "ListenEnv": ['jd_jinggeng_showTaskDraw_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】直播互动抽奖",
    "Script": "shufflewzc_faker3_main/jd_liveLottery.js",
    "ListenEnv": ['jd_liveLottery_ids'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】店铺抽奖（超级无线/超级会员）",
    "Script": "shufflewzc_faker3_main/jd_luck_draw.js",
    "ListenEnv": ['LUCK_DRAW_URL'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】加购有礼（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_cart.js",
    "ListenEnv": ['jd_lzkj_cart_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】每日抢好礼（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_dailyGrabs.js",
    "ListenEnv": ['jd_lzkj_dailyGrabs_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】签到有礼（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_daySign.js",
    "ListenEnv": ['jd_lzkj_daySign_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】幸运抽奖（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_draw.js",
    "ListenEnv": ['jd_lzkj_draw_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】关注商品有礼（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_followGoods.js",
    "ListenEnv": ['jd_lzkj_followGoods_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】邀请关注店铺有礼（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_inviteFollowShop.js",
    "ListenEnv": ['jd_lzkj_inviteFollowShop_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】知识超人（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_know.js",
    "ListenEnv": ['jd_lzkj_know_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】关注店铺有礼（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_lkFollowShop.js",
    "ListenEnv": ['jd_lzkj_lkFollowShop_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】邀请入会有礼（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_loreal_invite.js",
    "ListenEnv": ['jd_lzkj_loreal_invite_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】分享有礼（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_loreal_share.js",
    "ListenEnv": ['jd_lzkj_loreal_share_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】签到抽奖（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_loreal_sign.js",
    "ListenEnv": ['jd_lzkj_loreal_sign_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】组队瓜分奖品（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_organizeTeam_url.js",
    "ListenEnv": ['jd_lzkj_organizeTeam_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】完善有礼（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_perfectInfo.js",
    "ListenEnv": ['jd_lzkj_perfectInfo_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】积分兑换（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_pointsExchange.js",
    "ListenEnv": ['jd_lzkj_pointsExchange_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】店铺礼包（超级无线）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_shopGift.js",
    "ListenEnv": ['jd_lzkj_shopGift_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】生日礼包（超级无线V2）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_v2_birthday.js",
    "ListenEnv": ['jd_lzkj_v2_birthday_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】幸运抽奖（超级无线V2）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_v2_draw.js",
    "ListenEnv": ['jd_lzkj_v2_draw_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】完善有礼（超级无线V2）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_v2_perfectInfo.js",
    "ListenEnv": ['jd_lzkj_v2_perfectInfo_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】签到有礼（超级无线V2）",
    "Script": "shufflewzc_faker3_main/jd_lzkj_v2_sign.js",
    "ListenEnv": ['jd_lzkj_v2_sign_url'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】强制入会",
    "Script": "shufflewzc_faker3_main/jd_opencard_force.js",
    "ListenEnv": ['jd_opencard_force_venderId'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】入会礼包",
    "Script": "shufflewzc_faker3_main/jd_opencard_gift.js",
    "ListenEnv": ['jd_opencard_venderId'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】积分兑换京豆（超级会员）",
    "Script": "shufflewzc_faker3_main/jd_pointExgBeans.js",
    "ListenEnv": ['jd_pointExgBeans_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】积分兑换红包（超级会员）",
    "Script": "shufflewzc_faker3_main/jd_pointExgHb.js",
    "ListenEnv": ['jd_pointExgHb_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】积分兑换实物（超级会员）",
    "Script": "shufflewzc_faker3_main/jd_pointExgShiWu.js",
    "ListenEnv": ['jd_pointExgShiWu_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】邀请好友入会得好礼",
    "Script": "shufflewzc_faker3_main/jd_prodev.js",
    "ListenEnv": ['jd_prodev_actCode'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】店铺刮刮乐（刮一刮）",
    "Script": "shufflewzc_faker3_main/jd_shopLottery.js",
    "ListenEnv": ['jd_shopLottery_venderIds'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】无线店铺签到（超级无线/超级会员）",
    "Script": "shufflewzc_faker3_main/jd_shopSign.js",
    "ListenEnv": ['jd_shopSign_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  },
  {
    "Name": "【Faker】无线店铺签到（超级无线/超级会员）",
    "Script": "shufflewzc_faker3_main/jd_shopSign.js",
    "ListenEnv": ['jd_shopSign_activityUrl'],
    "SetEnv": {},
    "TimeOut": 50,
    "Interval": 0,
    "RunPanel": [
      0
    ],
    "Disable": false
  }
],
    /* 监控列表 */
    ListenList: [
        {
            Name: 'Faker线报频道',
            Id: '-1001670294604',
        },
        {
            Name: 'Faker线报群',
            Id: '-1001712811852',
        }

    ],

    //非静默触发消息多少秒撤回 0不撤回
    delMsgWaitTime: 10,
    //静默功能  默认false,会在监听到消息的地方回复监听结果 true则推送到静默推送设置的地方
    Taboo: true,
    TabooOriginalMsg: false /* 静默后推送的消息是否显示触发消息 */,
    //1 禁用任何日志输出 改为true后,不会向社交平台推送任何消息,且2 3开关失效 控制台除外
    DisableAllLogs: false,
    //2 禁用错误日志输出 改为true后,不会向社交平台推送任何错误消息 控制台除外
    DisableErrLogs: false,
    //3 禁用正常运行日志输出 改为true后,不会向社交平台推送任何任务运行成功的消息 控制台除外
    DisableRunLogs: false,
    //4 禁用控制台日志 改为true后,控制台不会显示任何消息
    DisableConsoleLog: false,
    //队列模式 1先进先出  2先进后出  其他值均视为 先进先出
    ListMode: 2,
    /* 运行日志输出位置,例如错误运行日志/任务运行成功等日志,只能设置1个 */
    runLogsInfo: {
        platform: 'tgbot', //发送平台
        toGroupOrUser: 'groupId', //通知类型,个人userId //群groupId
        Id: '0000', //个人id 或群id
    },
    /* 静默后监控结果输出位置  可填多个*/
    TabooLogsInfo: [
        /*  {
            platform: "wxXyo",
            toGroupOrUser: "groupId",   //通知类型,个人userId //群groupId
            Id: "44871814466"
         },*/
         {
             platform: 'tobot', //发送平台
             toGroupOrUser: 'groupId', //通知类型,个人userId //群groupId
             Id: '0000', //个人id 或群id
         },
    ],
};

module.exports = {
    RspyList,
};
```
修改完以后保存。将Bncr\_spy.js和mod文件夹拖入/root/BncrData/plugins/红灯区

<img src="https://thin-hill-428.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fab86454e-d8fc-47db-8b72-d95ac7149dba%2F4ae830c5-f02b-470b-b3fb-fa45f97fed37%2FUntitled.png?table=block&id=4c46f403-8823-48e1-98ab-9686475f7cee&spaceId=ab86454e-d8fc-47db-8b72-d95ac7149dba&width=1990&userId=&cache=v2" alt="配图" />


## 监听群组和频道

Tgbot无法监听频道，人形可监听频道和群组。

上方配置已配置好Faker线报频道和Faker线报群，没加入的加入一下。

Bot添加进群如果无权访问消息，需要管理员权限，最好用人形。

<https://t.me/fakertoulu>

<https://t.me/faketoulu>

在无界网页端添加监听列表，ID在频道和群的简介中有，记得把回复按钮关掉，避免被小蒲sb。

<img src="https://thin-hill-428.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fab86454e-d8fc-47db-8b72-d95ac7149dba%2F13228d54-0c5a-4008-ac9b-8e2406e50610%2FUntitled.png?table=block&id=522a976b-5661-44be-989f-1a8db0a72e12&spaceId=ab86454e-d8fc-47db-8b72-d95ac7149dba&width=1420&userId=&cache=v2" alt="配图" />


## 面板

在上期已经对接好了青龙面板，默认已经可以传到青龙面板了。

# 对接QQ

> ## [**【NTQQ】利用LiteLoaderQQNT插件实现NTQQ对接机器人框架（Docker版）**](https://www.luomubiji.host/ntqq.html)

->

## LLOneBot-Docker

[DockerHub](https://hub.docker.com/r/mlikiowa/llonebot-docker)

### Alternative

如果 LLOneBot Docker 如果无法正常启动。

而你的服务器有没有GUI环境或者内存太小 可以迁移至 [NapCatQQ](https://github.com/NapNeko/NapCatQQ) ，该项目无需GUI与图形环境

### Information

请注意! 该项目使用应当遵守上游开源库协议与要求，遵守当地法律与规范。

该项目适用于快速将NTQQ Bot托管容器，提供 VNC，以便远程登录和配置。

LLOneBot容器已经带有ffmpeg不需要额外配置，如手动点击配置 导致容器配置数据异常

### Support Platform/Arch

- Linux/Amd64
- Linux/Arm64

### Image Layer

- mlikiowa/llonebot-docker:latest

  - 不提供 VNC, 只能通过 LLWebUiApi 来登录
- mlikiowa/llonebot-docker:vnc

  - 提供了 VNC

### Install

1. 安装参考已选方案一与方案二 启动
2. 远程登录，VNC登录 `服务器IP:5900`

## 使用方案（一）VNC登录
```
sudo docker run -d --name onebot-docker0 -e VNC_PASSWD=vncpasswd -p 3000:3000 -p 5900:5900 -p 3001:3001 -v ${PWD}/LiteLoader:/opt/QQ/resources/app/LiteLoader mlikiowa/llonebot-docker:vnc
```
其中vncpasswd换成你的VNC密码 或者下载代码中的docker-compose.yml，然后执行
```
sudo docker-compose up -d
```
等待 docker 启动完毕后使用 vnc 客户端连接进入 docker Linux 桌面登录 QQ 和配置 LLOneBot

## 使用方案（二）LLWebuiApi 登录
```
sudo docker run -d --name onebot-docker0 -e VNC_PASSWD=vncpasswd -p 3000:3000 -p 6099:6099 -p 3001:3001 -v ${PWD}/LiteLoader:/opt/QQ/resources/app/LiteLoader mlikiowa/llonebot-docker:latest
```
然后浏览器访问 扫码登录`http://你的docker-ip:6099/api/panel/getQQLoginQRcode`

登录之后访问 进行 llonebot 的配置`http://你的docker-ip:6099/plugin/LLOneBot/iframe.html`

## 快速配置脚本（实验性)
```
curl https://cdn.jsdelivr.net/gh/LLOneBot/llonebot-docker/fastboot.sh -o fastboot.sh & chmod +x fastboot.sh & sudo sh fastboot.sh
```

```
wget -O fastboot.sh https://cdn.jsdelivr.net/gh/LLOneBot/llonebot-docker/fastboot.sh & chmod +x fastboot.sh & sudo sh fastboot.sh
```
## Feat

### 崩溃快速重启

你仅仅需要到设置配置自动登录，保证崩溃时手机QQ不在线即可，其余时间可以使用手机QQ

### 数据固化

暂时忽略 未实现QQ本体数据固化 仅实现LiteLoader包括其所有插件数据固化(按照以上流程启动无须考虑，已自动启用) 无需阅读该条目录

### 参考与基础

[LLOneBot/LLOneBot](https://github.com/LLOneBot/LLOneBot)

[yuuki-nya/chronocat-docker](https://github.com/yuuki-nya/chronocat-docker/blob/main/Dockerfile)

### 已知问题与提示

### 1.快速闪退

如果连接反向ws后快速闪退 清空容器数据之后 再次配置先启用上报自身消息 在vnc窗口复制 之前触发机器人的消息 使用机器人账号发送 再正常使用bot

### 2.发送文件

需要挂载相应文件夹

## ntqq图形化安装--落幕版本

### **准备**

1. **准备一个**`VNC`软件。我会在群内准备一些手机上的和PC端的。这里直接用青柠提供的`1Remote`
2. **准备手机登陆机器人**`QQ号`，扫码

### NTQQ一键脚本（适用于小白支持autMan/无界）

**复制以下代码，在服务器发送即可。按照提示步骤**`输入正确参数`，如果出现输错可以自行去文件夹内`修改`！（如果`脚本有问题`，欢迎加`Q群反馈`，找时间会优化。）搞好后就跳转下面的`VNC连接`接着连接操作
```
cd && curl -o "ntqq.sh" "https://raw.githubusercontent.com/baquanluomu/ntapiconfig/main/ntqq.sh" && chmod +x ntqq.sh && ./ntqq.sh
```
**示例图：**

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221624265832.webp" alt="20240625221624267000" />


### 手动搭建NTQQ（建议老手）

**SSH链接你的服务器，在**`root`目录下，没有的请`cd /root`，然后输入下面命令创建对应文件夹并创建配置文件，请注意将`记得换`文字换成机器人的`QQ号码`
```
mkdir -p LLOneBot && cd LLOneBot && touch config_记得换.json
```
请把记得换更改为机器人QQ号码

1. **如果不确定是否成功，可以自行查看下目录或者**`ll`看查目录。正确后我们进行编辑配置文件，配置地址端口。（并不是一定要`vi`如果有宝塔等或者nas等可以直接去目录手动修改哈，怎么方便怎么来）,这里我直接使用了SSH工具查看json文件，

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221619754739.webp" alt="20240625221619753000" />


1. **上面进入后，我们双击里面的对应机器人QQ的配置文件打开，然后编辑箭头所指那一串，如果你的NTQQ跟你的框架是一起的，也可以用10.10.10.10或者127.0.0.1和192.xx.xx.xx都是可行的**

### 无界bncr
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
**编辑改好后，咋们记得保存，拉取镜像并run容器（不用管arm或者amd什么的，直接拉取，会自动识别）**
```
docker run -d  --restart=always --name NTQQ  -v /root/LLOneBot/:/opt/QQ/resources/app/LiteLoaderQQNT/data/LLOneBot/ -p 5900:5900 -p 3000:3000 luomubiji/ntqq:latest
```
<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221702526554.webp " alt="20240625221702525000" />


5. **注意上面的name后面的**`NTQQ`是可以更改的，还有`-p 5900:5900 -p 3000:3000` 这里的`:`前面的`5900`和`3000`是可以更改的，更改后代表后面的步骤都需要相应的替换。如果有端口冲突，还是更改为好，没有就不必更改，有没有很简单，自己用命令`lsof -i:5900`查看记得

## **VNC连接**

1. **首先VNC软件选择性很多，各个功能不一样，建所以这里直接用**`1Remote`来演示，首先打开软件，右上角选择`+`号，选择添加，点击上方`VNC`，输入名称

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221625693974.webp " alt="20240625221625692000" />

2. VNC密码是：
```
vncpasswd
```
2. **往下拉找到地址，输入上面搭建**`NTQQ服务器的地址IP（可域名）+端口号`，就是上面的第六步，里面的`5900`如果你有变动，改的什么就在此处填写什么（家宽openwrt或者爱快等，记得开放端口）。下面密码输入：`vncpasswd` (关于密码固定后续可能会优化为可自定义)，然后保存。

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221632421860.webp " alt="20240625221632420000" />

3. **保存后我们去双击你添加的，就会进行连接（如果遇到连接失败，你确定端口开放！且确定容器正常运行中！端口占用等问题！），连接成功后如图所示：**

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625221643330615.webp " alt="20240625221643330000" />

4. **然后我们拿出我们准备好的机器人QQ手机，右上角**`+`号，扫一扫，然后扫出来的二维码。并登陆，确定登录。出现确认最好`勾选下次登录无需手机确认`，如果遇到闪退，扫码后黑屏等，`重新连接VNC`就行。直到出现正常QQ登陆界面。然后就进行`关键操作`！！！

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625222934903934.webp " alt="20240625222934905000" />


关键操作！

2. **VNC连接第5步图一示例：**

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625223202146066.webp " alt="20240625223202144000" />

3. **无界web更改**`qqOutside.js`示例图，请将`适配器模式更改为ws`,交互发送地址更改为`NTQQ的地址加端口`，记得开启适配器，图上没开而已，js路径在`/bncr/BncrData/Adapter`

<img src="https://lmu5.com/wp-content/uploads/2024/06/20240625223255811988.webp " alt="20240625223255810000" />


## **更新命令**

**这里使用的是watchtower来更新，但是我不知道是个人原因还是什么原因，watchtower版本无论怎么拉取最新的都是1.3.0（删除了镜像也是），所以我建议如果您的watchtower版本很低的话，就是用下面命令拉取后出现第一行为1.7.1（2024年3月14日 23:18:12目前最新）以下的话，最好还是手搓拉取指定版本，注意更新是要时间的！且更新后还需要扫码登录，且要除了配置文件外的比如自动登录，取消更新都需要重新开关！**

尾巴的NTQQ是容器名字！！！！

### NTQQ指定用watchtower1.7.1更新（跟我类似情况）
```
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower:1.7.1 -c --run-once  NTQQ
```
**Copy**

### NTQQ通用更新命令
```
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower -c --run-once NTQQ
```
## 最新NCQQ

vnc链接同上
```
docker run -d  --restart=always --name ncqq -v /root/ncqq/:/opt/QQ/resources/app/LiteLoaderQQNT/plugins/NapCat.Framework/config/ -p 5900:5900 -p 3000:3000 -p 6099:6099  luomubiji/ncqq:latest
```
NTQQ部分内容转载至落幕

链接：<https://lmu5.com/ntqq.html>

# ChatGpt中转

自用推荐: [大聪明各种模型中转站](https://chatai.master-jsx.top/)
[TTS适配海豚Ai TTS-Online](https://www.ttson.cn/?source=qDBPb2)

# 插件仓库和插件使用教程

## 无界 | Bncr | Xinz / XianYu

> **无界机器人插件以及其他的一些自己写的或者从开源项目二改转载的脚本 也是自己的备份 请勿乱用谢谢 尽量做到开源 可以自己修改 尽量做到web配置；** [鑫仔博客教程](https://www.xinz.fun/archives/1717170773466) [鑫仔Github](https://github.com/seven-XINZ/bncr)
>
> 鑫仔插件商城订阅:<https://github.com/seven-XINZ/bncr> XINZ

## xinz/ChatGPT.js 完美版

ChatGpt聊天，适配无界3.0，增加 ai 画图 TTS 功能

请先到WEB界面完成插件首次配置 无界web插件配置 配置ChatGpt 。

ApiBaseUrl： 必填项，一般为"域名/v1" <https://chatai.master-jsx.top/v1>

ApiKey：必填项 sk-64---------------------------------------edf7d

HumanTG是否开启编辑模式： 关闭则逐条回复，不编辑消息

选择预设角色： 请根据需要选择 猫娘

选择GPT模型：请根据需要选择web-gpt-4o-mini

请输入自定义Prompt： 输入自定义Prompt会使预设角色失 请输入

请输入画图的ApiBaseUrl：启用画图功能必填，一般为"域名/v1" <https://chatai.master-jsx.top/v1>

画图的模型：启用画图功能必填，根据自己的API支持情况填写 dall-e-3

画图的ApiKey：启用画图功能必填，根据自己的API支持情况填写 sk-64---------------------------------------edf7d

启用TTS功能： 开启后将使用TTS功能 TTS

ApiBaseUrl： 启用TTS功能必填，一般为"域名/v1" <https://chatai.master-jsx.top/v1>

TTS ApiKey：启用TTS功能必填，根据自己的API支持情况填写 sk-64---------------------------------------edf7d

自定义TTS模型： 可根据需要输入自定义的TTS模型名称 zh-CN-XiaoyiNeural

<img src="/upload/gpt-wluz.png" alt="配图" />


## ChatGpt中转

自用推荐: [大聪明各种模型中转站](https://chatai.master-jsx.top/)
[TTS适配海豚Ai TTS-Online](https://www.ttson.cn/?source=qDBPb2)

## xinz/Bncr\_ChatGPT.js 插件转载自大佬仓库

1. 添加对话模型引入 ✔
2. 添加对话模型选择 gpt3.5 gpt4 gpts(联网能力) ✔
3. initPrompt,发起会话调用数据库内prompt，数据库内无数据则生成，prompt为默认，修改handleUserActions，添加当前使用模型xx
4. gpt 4 mobile 的连续对话中对于img的传递 ✔
5. handleInput对于用户输入的img的处理,如何修改ntqq适配器使其接收图片的输出为[CQ:image,file=xxx] ✔
6. 取消模型的选择，加入命令ai model ,并在第一条输出中提示当前使用模型 12.17 添加画图功能 ✔ 12.19 添加backendUrl，用于调用pandoraToV1Api ✔ 12.21 优化请求格式，实现连续对话中对于img的传递 2024.2.8 取消画图 backendurl *@rule ^(画图) ([\s\S]+)$ ✔ 2024.4.10 添加tts功能* @rule ^(yy) ([\s\S]+)$ ✔,重写调用chatgpt模块，got发送请求

## xinz/Gemini.js

gemini聊天 来自谷歌的ai v1.0.1 优化代码，增加单问答模式，修改触发命令，界面增加Max Tokens选项 v1.0.0 基于sumuen大佬的插件修改，本人仅修复bug和适配2.0界面 v1.0.2 适配3.0

## xinz/IKUN.js

发送IKUN语录和表情包

## xinz/ping.js

ping/web测速插件 ping [www.xinz.fun](http://www.xinz.fun/) dns: 154.37.152.17 地区: Los Angeles, California, US ip: 154.37.152.17 延迟: 190.059 ms 访问 [https://www.xinz.fun](https://www.xinz.fun/) 成功，用时: 2275 ms 发包: 4 接收: 4 丢包率: 0% 成功率: 0.00%

## xinz/qbittorent操作.js

请发送磁力连接(发送'q'退出'u'返回

鑫仔插件商城订阅:<https://github.com/seven-XINZ/bncr> XINZ

# 接下来是无界开发者文档有兴趣自主开发功能插件继续往下看

## [**开发文档**](https://anmours.github.io/Bncr/#/md/develop?id=%e5%bc%80%e5%8f%91%e6%96%87%e6%a1%a3)

4200 字   |  11 分钟

> - Bncr 是一个 Node.js 框架，开发框架需要有一定的 JavaScript 和 Node.js 基础。
> - 本人用傻妞(sillyGirl)比较多一点，习惯了一些语法与功能，所以 Bncr 上有很多傻妞语语法的身影~ 如果你是一个傻妞开发者，切换至 Bncr 可以说是无缝切换！

## [**开发环境搭建**](https://anmours.github.io/Bncr/#/md/develop?id=%e5%bc%80%e5%8f%91%e7%8e%af%e5%a2%83%e6%90%ad%e5%bb%ba) [**通过 vscode 远程开发**](https://anmours.github.io/Bncr/#/md/develop?id=%e9%80%9a%e8%bf%87-vscode-%e8%bf%9c%e7%a8%8b%e5%bc%80%e5%8f%91)

- 百度 `vscode 安装 Remote-SSH` 并链接远程主机
- 打开 BncrData 映射目录
- 新建终端,输入 docker attach bncr 链接容器控制台,在这里你可以直接输入信息调试、以及观察 console.log 输出信息、收发消息情况等信息
- npm/yarn： 你可以直接在根目录下新建终端，直接 `npm/yarn i xxx` ，如果本机没有 npm/yarn 环境，可以 `docker exec -it bncr /bin/sh` 后 `npm/yarn i 你的内容`
- 本人开发姿势：两个终端，一个 `docker attach bncr` 用于调试，另一个 `docker exec -it bncr /bin/sh` 用于安装 npm，这样开发插件非常方便~

<img src="https://anmours.github.io/Bncr/md/image/develop/1677296097624.png" alt="1677296097624" />

本人开发插件示例

## [**文件目录说明**](https://anmours.github.io/Bncr/#/md/develop?id=%e6%96%87%e4%bb%b6%e7%9b%ae%e5%bd%95%e8%af%b4%e6%98%8e)

- 适配器开发

  - Adapter 下只有根目录下的.js 文件才会被尝试载入，二级以下的目录不会加载
  - 重载：适配器本身开发需求并不是太大，所以没有做热重载，需要重启重载
- 插件开发

  - 注意 与 Adapter 不同，因为要做作者分类或者作用域分类，所以 plugins 下只有二级目录下的.js 文件才会被尝试载入，根目录以及 3 级以下不会加载，示例 ：

    ```
    plugins/官方插件/命令.js  //会被当做插件载入
    plugins/命令.js  //忽略
    plugins/官方插件/mod/qlmod.js //忽略 因此你可以在三级目录放一些自己写的模块Copy to clipboardErrorCopied
    ```
  - 重载：plugins 下的所有文件都是保存既重载
- 静态资源

  - public 目录下的文件将被作为静态资源公开，访问 `http://ip:9090/public/对应文件名` 即可访问到，因此，你可以操控 bncr 把文件存放到该目录，在通过本机 url 的方式发送出去（建议用 uuid 或其他随机数来表示文件名，否则资源多的情况下可能会导致误发文件）。

# [**全局方法介绍**](https://anmours.github.io/Bncr/#/md/develop?id=%e5%85%a8%e5%b1%80%e6%96%b9%e6%b3%95%e4%bb%8b%e7%bb%8d)

## [**router 系统路由**](https://anmours.github.io/Bncr/#/md/develop?id=router-%e7%b3%bb%e7%bb%9f%e8%b7%af%e7%94%b1)

该路由基于 express.Router()，挂载在系统/路径下,你可以在 9090/下扩展服务
```
//示例
// get访问http://bncrip:9090/api/bot/qqws
router.get('/api/bot/qqws', (req, res) => {
    res.send({ msg: '这是Bncr 外置qq Api接口，你的get请求测试正常~，请用ws交互数据' });
});
// post访问http://bncrip:9090/api/bot/qqws
router.post('/api/bot/qqws', async (req, res) => {
    res.send({ msg: '这是Bncr 外置qq Api接口，你的post请求测试正常~，请用ws交互数据' });
});
// ws监听ws://bncrip:9090/api/bot/qqws
router.ws('/api/bot/qqws', ws => {
    ws.on('message', msg => {
        console.log('收到ws请求', msg);
    });
});Copy to clipboardErrorCopied
```
## [**sysMethod 系统方法**](https://anmours.github.io/Bncr/#/md/develop?id=sysmethod-%e7%b3%bb%e7%bb%9f%e6%96%b9%e6%b3%95)

### [**async sysMethod.sleep(time)**](https://anmours.github.io/Bncr/#/md/develop?id=async-sysmethodsleeptime)

休眠(阻塞运行),传 number,注意单位是秒
```
//休眠5秒 不用await 关键字无效
await sysMethod.sleep(5);Copy to clipboardErrorCopied
```
### [**sysMethod.getTime(string)**](https://anmours.github.io/Bncr/#/md/develop?id=sysmethodgettimestring)

获取时间
```
sysMethod.getTime('hh:mm:ss'); //18:19:20
sysMethod.getTime('yyyy-MM-dd'); //2023-02-24
sysMethod.getTime('yyyy-MM-dd hh:mm:ss'); //2023-02-24 18:19:20Copy to clipboardErrorCopied
```
### [**sysMethod.config**](https://anmours.github.io/Bncr/#/md/develop?id=sysmethodconfig)

存储着 config.js 下的全部信息

### [**sysMethod.cron**](https://anmours.github.io/Bncr/#/md/develop?id=sysmethodcron)

#### [**sysMethod.cron.newCron(string,()=>{})**](https://anmours.github.io/Bncr/#/md/develop?id=sysmethodcronnewcronstringgt)

系统内置的定时器
```
//8点执行回调函数
sysMethod.cron.newCron('0 0 8 * * *', () => {
    console.log('执行了');
});Copy to clipboardErrorCopied
```
#### [**sysMethod.cron.isCron(string)**](https://anmours.github.io/Bncr/#/md/develop?id=sysmethodcroniscronstring)

判断字符串是否是定时表达式
```
sysMethod.cron.isCron('0 0 8 * * *'); //true
sysMethod.cron.isCron('* * *'); //falseCopy to clipboardErrorCopied
```
### [**sysMethod.npmInstall 安装 npm 包**](https://anmours.github.io/Bncr/#/md/develop?id=sysmethodnpminstall-%e5%ae%89%e8%a3%85-npm-%e5%8c%85)
```
await sysMethod.npmInstall('request'); //会返回执行信息String
await sysMethod.npmInstall('request', { outConsole: true }); // 将会在控制台实时打印安装情况，返回结果为nullCopy to clipboardErrorCopied
```
### [**sysMethod.testModule 测试npm包是否存在**](https://anmours.github.io/Bncr/#/md/develop?id=sysmethodtestmodule-%e6%b5%8b%e8%af%95npm%e5%8c%85%e6%98%af%e5%90%a6%e5%ad%98%e5%9c%a8)
```
await sysMethod.testModule(['telegram', 'input']); //将只测试，返回结果
await sysMethod.testModule(['telegram', 'input'], { install: true }); //发现少模块自动安装Copy to clipboardErrorCopied
```
### [**sysMethod.inline(string)**](https://anmours.github.io/Bncr/#/md/develop?id=sysmethodinlinestring)

内联 以系统管理员的身份向平台内部发送消息
```
//例子 9点整以系统管理员身份 触发重启命令 from类型为system
sysMethod.cron.newCron('0 0 9 * * *', () => {
    sysMethod.inline('重启');
});Copy to clipboardErrorCopied
```
### [**sysMethod.push(pushInfo)**](https://anmours.github.io/Bncr/#/md/develop?id=sysmethodpushpushinfo)

系统推送消息方法
```
//通过tgBot向用户或者群发消息
//群id和个人id必须存在一个,否则不会推送消息,如果同时存在,则群和人都推
// type为可选字段,如果不传该值默认为text
sysMethod.push({
    platform: 'tgBot',
    groupId: `-1001704263871`,
    userId: `1629887728`,
    msg: '这是一条推送消息',
    type: 'text',
});Copy to clipboardErrorCopied
```
### [**sysMethod.Adapters(msgInfo,'tgBot','delMsg', 参数) 1.0.7增**](https://anmours.github.io/Bncr/#/md/develop?id=sysmethodadaptersmsginfo39tgbot3939delmsg39-%e5%8f%82%e6%95%b0-107%e5%a2%9e)

等同于tgBot触发的插件内调用sender.delMsg(参数) msgInfo格式可在插件内打印sender.msgInfo查看 基于此次更新可以实现不同平台插件之间互相流转工作流

### [**sysMethod.pushAdmin(pushInfo)**](https://anmours.github.io/Bncr/#/md/develop?id=sysmethodpushadminpushinfo)

通知各个适配器管理员
```
//必选字段
//[platform]需要推送平台的sting数组,如果为空数组,则会推送所有平台.
//[msg]要发送的消息
//可选字段
//[type],发送消息的类型,默认为text
sysMethod.pushAdmin({
    //推送所有平台
    platform: [],
    //只推送wxKeAImao 、qqbot 、tgBot
    platform: ['wxKeAImao', 'qqbot', 'tgBot'],
    msg: '这是一条推送消息',
});Copy to clipboardErrorCopied
```

```
Copy to clipboardErrorCopied
```
## [**Adapter ( ) 适配器构造函数**](https://anmours.github.io/Bncr/#/md/develop?id=adapter-%e9%80%82%e9%85%8d%e5%99%a8%e6%9e%84%e9%80%a0%e5%87%bd%e6%95%b0)

- 具体使用方法参见适配器开发

## [**BncrDB ( ) 系统数据库构造函数**](https://anmours.github.io/Bncr/#/md/develop?id=bncrdb-%e7%b3%bb%e7%bb%9f%e6%95%b0%e6%8d%ae%e5%ba%93%e6%9e%84%e9%80%a0%e5%87%bd%e6%95%b0)

系统数据库为轻量型内嵌式 KV 数据库。

开发插件时，你可以使用任意你喜欢的数据库来存放数据 （不建议，会破坏用户使用体验）

有关数据库操作，你可以在官方插件中找到全部用法示例

> **警告! db 文件可能看起来是 json 格式文件，但实则不是！不要试图用任何工具直接修改 db 文件，这可能会造成数据损坏!**

### [**get()获取数据**](https://anmours.github.io/Bncr/#/md/develop?id=get%e8%8e%b7%e5%8f%96%e6%95%b0%e6%8d%ae)

该方法接受三个参数

- 需要读取的 key
- 未读取到值默认返回值（可选）
- 布尔值，默认 false，true 返回该数据的全部数据 （可选）
```
//创建一个系统数据库实例
const sysdb = new BncrDB('system');

//读取一个key的 value 值 如果没有该数据返回undefined
await sysdb.get('name1'); // undefined
// 第二个参数作为未读取到数据的返回值
await sysdb.get('name1', '空值'); // 空值
// 读取到数据 返回 value 值
await sysdb.get('name', '空值'); // Aming

// 读取该数据数据结构
await sysdb.get('name', '空值', true);
/** 如果读取到数据返回以下结构，否则返回第二个参数
    {
        name: 'system',
         key: 'name',
         value: 'Aming',
         _id: 'pptOvhDn8rOyb3m4',
         createdAt: 2023-02-17T14:15:33.246Z,
         updatedAt: 2023-02-17T14:29:31.197Z
    }

*/Copy to clipboardErrorCopied
```
### [**set()存储数据**](https://anmours.github.io/Bncr/#/md/develop?id=set%e5%ad%98%e5%82%a8%e6%95%b0%e6%8d%ae)

该方法接受三个参数

- 需要设置的 key
- 需要设置的 value
- 可选参数 （可选）
```
//创建一个系统数据库实例
const sysdb = new BncrDB('system');

await sysdb.get('name'); // Aming
await sysdb.set('name', 'Aming3'); // 成功 true 失败false
await sysdb.get('name'); // Aming3

//第三个参数为对象，如果传入def字段，则改变设置成功返回的值 ，该对象还有一些其他的字段可设置，还在开发ing...
await sysdb.set('name', 'Aming4', { def: '设置成功' }); // 成功 设置成功 失败 false
await sysdb.get('name'); // Aming4

//其他使用
//异步设置，不会阻塞程序执行，如果需要等待设置结果，此方法不可用
sysdb.set('name', 'Aming5'); // 返回一个Promise
//注意！set操作可以设置任何Object Number Array等js值，不会将value转为字符串设置进数据库，get读取到的和设置时的相同。Copy to clipboardErrorCopied
```
### [**del()删除数据**](https://anmours.github.io/Bncr/#/md/develop?id=del%e5%88%a0%e9%99%a4%e6%95%b0%e6%8d%ae)

该方法接受两个参数

- 需要删除的 key
- 删除成功返回的值

同 get 使用相同，删除成功返回 true，有第二个参数则返回第二个参数，失败返回 false ，没有该值会返回 undefined

### [**getAllForm() 读取所有 form(表)名 返回一个 Array**](https://anmours.github.io/Bncr/#/md/develop?id=getallform-%e8%af%bb%e5%8f%96%e6%89%80%e6%9c%89-form%e8%a1%a8%e5%90%8d-%e8%bf%94%e5%9b%9e%e4%b8%80%e4%b8%aa-array)

### [**keys()读取所有 key 返回一个 Array**](https://anmours.github.io/Bncr/#/md/develop?id=keys%e8%af%bb%e5%8f%96%e6%89%80%e6%9c%89-key-%e8%bf%94%e5%9b%9e%e4%b8%80%e4%b8%aa-array)

返回一个字符串数组

# [**适配器开发**](https://anmours.github.io/Bncr/#/md/develop?id=%e9%80%82%e9%85%8d%e5%99%a8%e5%bc%80%e5%8f%91)

## [**元信息配置**](https://anmours.github.io/Bncr/#/md/develop?id=%e5%85%83%e4%bf%a1%e6%81%af%e9%85%8d%e7%bd%ae)

通过 jsdoc 注释的方式来定义元信息
```
/**
- 作者
- @author Aming
- 适配器名称
- @name HumanTG
- 组织名  预留字段，未来发布插件会用到
- @origin 官方
- 版本号
- @version 1.0.0
- 说明
- @description 适配器
- 只有该值为true才会被作为适配器载入
- @adapter true
- 是否发布该插件（预留）
- @public false
- 是否禁用，true时该适配器不会被载入
- @disable false
- 载入优先级
- @priority 101
- 版权信息
- @Copyright ©2023 Aming and Anmours. All rights reserved
- Unauthorized copying of this file, via any medium is strictly prohibited
 */Copy to clipboardErrorCopied
```
## [**初始化一个适配器**](https://anmours.github.io/Bncr/#/md/develop?id=%e5%88%9d%e5%a7%8b%e5%8c%96%e4%b8%80%e4%b8%aa%e9%80%82%e9%85%8d%e5%99%a8)

在本框架下，所有插件都必须遵循 CommonJS 模块化规范导出一个函数作为启动入口

例:
```
//当导出的函数为async异步函数时，系统载入该适配器的时候会 await 等待该异步结束才会加载下一个适配器
module.exports = async () => {
  //you code
}

// 上面的代码等同于

module.exports = () => {
  return new Promise(async (resolve, reject) => {
    //you code
  }
}Copy to clipboardErrorCopied
```
或：
```
async function mian () {
  //you code
}

// 上面的代码等同于
function mian () {
  return new Promise(async (resolve, reject) => {
    //you code
  }
}

module.exports = mian
Copy to clipboardErrorCopied
```
基本使用方法：
```
/**
- @author Aming
- @name 钉钉
- @origin 官方
- @version 1.0.0
- @description 钉钉适配器
- @adapter true
- @public false
- @disable false
- @priority 50
- @Copyright ©2023 Aming and Anmours. All rights reserved
- Unauthorized copying of this file, via any medium is strictly prohibited
 */

module.exports = () => {
    //实例化一个适配器，传入名，该名会作为唯一标识符，所以请避免和其他适配器冲突
    const Ding = new Adapter('Ding');
    /* 注入发送消息方法 */
    /*
    replyInfo 为固定结构：
    该结构中的内容完全于插件内sender.reply()函数决定，详细参见插件开发说明
    replyInfo = {
        type: 'text', //image/video/ 等
        msg: '要发送的消息',
        userId: '发送的用户id',
        groupId: '发送的群id',
        toMsgId: '发送者的消息id',
    }
    */
    Ding.reply = async function (replyInfo) {};
    /* 注入推送消息方法 */
    Ding.push = async function (replyInfo) {};
    /* 注入删除消息方法 */
    /* args = string[] */
    Ding.delMsg = async function (args) {};

    /*
    桥
    其他方法请定义在Bridge中，在插件中通过 sender.Bridge.xxx来访问
     */
    Ding.Bridge = {
        logTime: () => {},
    };

    //向框架内部发送信息，以下除了type都是必填字段,如果是number或其他值必须全部转为string
    Ding.receive({
        userId: '用户id' || '',
        userName: '用户名' || '',
        groupId: '群id' || '0',
        groupName: '群名' || '',
        msg: '消息' || '',
        msgId: '消息id' || '',
        type: `Social`, //消息类型（预留字段，可不填）Social意为社交
    });

    //最后必须返回该实例对象
    return Ding;
};

//详细适配器开发请见bncr官方自带的适配器Copy to clipboardErrorCopied
```
# [**插件开发**](https://anmours.github.io/Bncr/#/md/develop?id=%e6%8f%92%e4%bb%b6%e5%bc%80%e5%8f%91)

## [**sender 方法合集**](https://anmours.github.io/Bncr/#/md/develop?id=sender-%e6%96%b9%e6%b3%95%e5%90%88%e9%9b%86)

开发插件前,我们先了解一下 sender,该方法只有在插件中可用

### [**sender.getMsg() 获取消息**](https://anmours.github.io/Bncr/#/md/develop?id=sendergetmsg-%e8%8e%b7%e5%8f%96%e6%b6%88%e6%81%af)

### [**sender.setMsg() 篡改消息**](https://anmours.github.io/Bncr/#/md/develop?id=sendersetmsg-%e7%af%a1%e6%94%b9%e6%b6%88%e6%81%af)

### [**sender.getMsgId() 获取消息 id**](https://anmours.github.io/Bncr/#/md/develop?id=sendergetmsgid-%e8%8e%b7%e5%8f%96%e6%b6%88%e6%81%af-id)

### [**sender.getUserId() 获取用户 id**](https://anmours.github.io/Bncr/#/md/develop?id=sendergetuserid-%e8%8e%b7%e5%8f%96%e7%94%a8%e6%88%b7-id)

### [**sender.getUserName() 获取获取用户名**](https://anmours.github.io/Bncr/#/md/develop?id=sendergetusername-%e8%8e%b7%e5%8f%96%e8%8e%b7%e5%8f%96%e7%94%a8%e6%88%b7%e5%90%8d)

### [**sender.getGroupId() 获取群消息 id**](https://anmours.github.io/Bncr/#/md/develop?id=sendergetgroupid-%e8%8e%b7%e5%8f%96%e7%be%a4%e6%b6%88%e6%81%af-id)

### [**sender.getGroupName() 获取群名**](https://anmours.github.io/Bncr/#/md/develop?id=sendergetgroupname-%e8%8e%b7%e5%8f%96%e7%be%a4%e5%90%8d)

### [**sender.getFrom() 获取来自什么平台**](https://anmours.github.io/Bncr/#/md/develop?id=sendergetfrom-%e8%8e%b7%e5%8f%96%e6%9d%a5%e8%87%aa%e4%bb%80%e4%b9%88%e5%b9%b3%e5%8f%b0)

### [**sender.param() 提取触发词中的$x**](https://anmours.github.io/Bncr/#/md/develop?id=senderparam-%e6%8f%90%e5%8f%96%e8%a7%a6%e5%8f%91%e8%af%8d%e4%b8%ad%e7%9a%84x)

### [**sender.Bridge 适配器<桥>**](https://anmours.github.io/Bncr/#/md/develop?id=senderbridge-%e9%80%82%e9%85%8d%e5%99%a8lt%e6%a1%a5gt)

该值是一个对象，如果在适配器中定义了 Bridge，则可以通过 sender.Bridge.xxx 来访问

### [**async sender.isAdmin() 是否管理员消息**](https://anmours.github.io/Bncr/#/md/develop?id=async-senderisadmin-%e6%98%af%e5%90%a6%e7%ae%a1%e7%90%86%e5%91%98%e6%b6%88%e6%81%af)
```
await sender.isAdmin(); //true or falseCopy to clipboardErrorCopied
```
### [**sender.inlineSugar(msg) 内联**](https://anmours.github.io/Bncr/#/md/develop?id=senderinlinesugarmsg-%e5%86%85%e8%81%94)

以触发者的身份向系统内部发送消息
```
await sender.inlineSugar('重启'); //以触发者的身份向系统内部发送消息Copy to clipboardErrorCopied
```
### [**async sender.delMsg() 删除/撤销消息**](https://anmours.github.io/Bncr/#/md/develop?id=async-senderdelmsg-%e5%88%a0%e9%99%a4%e6%92%a4%e9%94%80%e6%b6%88%e6%81%af)
```
//立即撤回消息
sender.delMsg('id1', 'id2');

//等待2秒 阻塞
await sysMethod.sleep(2);
sender.delMsg('id1', 'id2');
/* 上下两种方法等价 */
//等待2秒 阻塞
await sender.delMsg('id1', 'id2', { wait: 2 });

//异步非阻塞 会挂载到后台等待，继续运行下面的代码
sender.delMsg('id1', 'id2', { wait: 2 });Copy to clipboardErrorCopied
```
### [**async sender.reply() 回复消息**](https://anmours.github.io/Bncr/#/md/develop?id=async-senderreply-%e5%9b%9e%e5%a4%8d%e6%b6%88%e6%81%af)
```
let s = sender;
//方式1
await s.reply('发送的消息');
//方式2
await s.reply({
    msg: '发送的消息',
});
//方式3
await s.reply({
    type: 'text',
    msg: '发送的消息',
});
//如果只发送字符串这三种写法是等价的 ,不指定消息类型默认是text

// 他们的区别在于可以指定发送消息的类型
await s.reply({
    type: 'image', // video
    msg: '图片来啦',
    path: 'https://pic3.zhimg.com/v2-58d652598269710fa67ec8d1c88d8f03_r.jpg',
});

//进阶
let replyid = await s.reply({
    type: 'image', // video
    path: 'https://pic3.zhimg.com/v2-58d652598269710fa67ec8d1c88d8f03_r.jpg',
    msg: '图片来啦',
    userId: '发给谁', //不传该字段默认是收到消息的人
    groupId: '发给群id', //不传该字段默认是收到消息的群
    toMsgId: '回复的消息id', //不传该字段默认是收到消息id
});
//撤回刚刚发的消息
await sender.delMsg(replyid);Copy to clipboardErrorCopied
```
### [**async sender.waitInput(()=>{},time) 监听消息**](https://anmours.github.io/Bncr/#/md/develop?id=async-senderwaitinputgttime-%e7%9b%91%e5%90%ac%e6%b6%88%e6%81%af)

与

### [**async sender.again()**](https://anmours.github.io/Bncr/#/md/develop?id=async-senderagain)
```
// 第一个参数必须为函数，第二个参数为时间，单位秒，
// 监听到该用户继续发信息时，会触发回调函数，返回一个 新的sender
// 监听该用户从新输入信息，等待30秒，
let newMsg =  await sender.waitInput(()=> {}, 30)
//超时未发送 newMsg = null
newMsg.getMsg()//获取监听到的信息

/* 进阶 */
// 回调函数中return 'again'会再次监听，并且监听时间重置为设定的时间
// again()方法会调用reply方法把传过去的值发送一遍，强制返回"again" ，所以是上述语法糖
// 因此以下回调函数中两种消息分支是等价的
let phone = await sender.waitInput(async (s)=> {
    //手机号
    let num = sender.getMsg();
    if (num === 'q') {
    } else if (num - 1 !== num - 1) {
        await s.reply('错误,重新输出')
        return 'again'                  //等价
    } else if (num.length !== 11) {
        return await s.again('错误,重新输出');  //等价
    }
}, 30);
if (phone === null) return sender.reply('超时退出');
if (phone.getMsg() === 'q') return sender.reply('已退出');
//撤回用户发的信息
sender.delMsg(phone.getMsgId();)
Copy to clipboardErrorCopied
```
## [**元信息配置**](https://anmours.github.io/Bncr/#/md/develop?id=%e5%85%83%e4%bf%a1%e6%81%af%e9%85%8d%e7%bd%ae-1)
```
/**作者
- @author Aming
- 插件名
- @name 官方命令
- 组织名  预留字段，未来发布插件会用到
- @origin 官方
- 版本号
- @version 1.0.5
- 说明
- @description 官方命令
- 限制平台 不在该范围内的平台消息该插件不会被触发
- @platform tgBot qqBot
- 触发正则   在bncr 所有的rule都被视为正则
- @rule ^(重启|bncr版本|启动时间|机器码)$
- @rule ^(编辑测试|撤销测试|推送消息测试|来个图片)$
- @rule ^(监听该群|屏蔽该群|回复该群|不回复该群)$
- @rule ^(eval) ([^\n]+)
- @rule ^(name|time|我的id|群id)$
- @rule ^(等待) ([^ \n]+)
- @rule ^(get|del) ([^ \n]+) ([^ \n]+)
- @rule ^(set) ([^ \n]+) ([^ \n]+) ([^ \n]+)
- // 是否管理员才能触发命令
- @admin true
- // 是否发布插件，预留字段，可忽略
- @public false
- // 插件优先级，越大优先级越高  如果两个插件正则一样，则优先级高的先被匹配
- @priority 9999
- // 是否禁用插件
- @disable false
- // 每5小时运行一次插件
- @cron 0 0 *\/5 * * *
- // 是否服务模块，true不会作为插件加载，会在系统启动时执行该插件内容
- @service false
 */Copy to clipboardErrorCopied
```
## [**初始化一个插件**](https://anmours.github.io/Bncr/#/md/develop?id=%e5%88%9d%e5%a7%8b%e5%8c%96%e4%b8%80%e4%b8%aa%e6%8f%92%e4%bb%b6)

在本框架下，所有插件都必须遵循 CommonJS 模块化规范导出一个函数作为启动入口 @service true 除外

例:
```
//当导出的函数为async异步函数时，系统运行插件时候会 await 等待该异步结束才会加载判断是否运行下一个插件
// 上面学到的 sender 在这时候用到，运行插件时，会传递sender进来~
module.exports = async (sender) => {
  //you code

  //插件运行结束时 如果返回 'next' ，则继续向下匹配插件 否则只运行当前插件
  return 'next'  //继续向下匹配插件
}
// 上下两种写法是等价的
module.exports = (sender) => {
  return new Promise(async (resolve, reject) => {
    //you code

    //插件运行结束时 如果返回 'next' ，则继续向下匹配插件 否则只运行当前插件
    resolve('next') //继续向下匹配插件
  }
}Copy to clipboardErrorCopied
```
或：
```
async function mian () {
  //you code

  //插件运行结束时 如果返回 'next' ，则继续向下匹配插件 否则只运行当前插件
  return 'next'  //继续向下匹配插件
}
// 上下两种写法是等价的
function mian () {
  return new Promise(async (resolve, reject) => {
    //you code

    //插件运行结束时 如果返回 'next' ，则继续向下匹配插件 否则只运行当前插件
    resolve('next') //继续向下匹配插件
  }
}

module.exports = mianCopy to clipboardErrorCopied
```
## [**写一个简单的 hello world**](https://anmours.github.io/Bncr/#/md/develop?id=%e5%86%99%e4%b8%80%e4%b8%aa%e7%ae%80%e5%8d%95%e7%9a%84-hello-world)
```
/**作者
- @author Aming
- @name 官方命令
- @version 1.0.5
- @description 官方命令
- @rule ^(hello|你好) ([^ \n]+)$
- @admin true
- @public false
- @priority 1
- @disable false

 */
module.exports = async s => {
    /*
   rule ^(hello|你好) ([^ \n]+)$
  上面的rule定义 发送:
  hello 任何值
  你好 任何值
  都会触发该插件
  */

    /* 如果是发送的 hello bncr 且 消息平台来自于tgBot 则回复 hello world  */
    if (s.param(1) === 'hello' && s.param(2) === 'bncr' && s.getFrom() === 'tgBot') {
        await s.reply('hello world');
    }
};Copy to clipboardErrorCopied
```
## [**插件加密**](https://anmours.github.io/Bncr/#/md/develop?id=%e6%8f%92%e4%bb%b6%e5%8a%a0%e5%af%86)

为保护开发者知识产权，如果不想公开插件源码，可以用块级注释来包裹需要加密的内容
`/* HideStart */` 开始，`/* HideEnd */`结束，必须严格按照要求，多/少空格都不会被识别到
如果插件中有加密块注释，保存时会在插件对应的目录中生成 EncryptFiles 目录，下面存放着加密后的插件，将此插件发布出去，用户使用时并不影响执行效果
```
/* HideStart */
let key = 1234;
/* HideEnd */

console.log('key');Copy to clipboardErrorCopied
```

到底啦~ 详细的开发还是要靠插件来说明,多看看官方插件吧~~

1.文中二维码和链接可能带有邀请性质，请各位玩家自行抉择。
2.请勿通过链接填写qq号与密码、银行卡号与密码等个人隐私信息。
3.禁止纯拉人头，拉app注册等信息，发现必小黑屋。
4.同一种信息仅发一次，多发会被删除。
5.文章中源码或APP等，无法保证其绝对安全，需自行辨别。
6.文章关联方不想展示也可以微信站长“socutesheep”删除。

本文由 xinz发布 如若转载，请注明出处： [科技玩家](https://www.kejiwanjia.net/) » [无界 | Bncr | Boundless Nodejs Chat Robot 安装使用教程](https://www.kejiwanjia.net/jiaocheng/125849.html) »[LLOneBot/llonebot-docker: 一键部署基于NTQQ的OneBot协议的Bot容器 (github.com)](https://github.com/LLOneBot/llonebot-docker)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
