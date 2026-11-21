# Homepage：极简导航页二次详解

> 标题：Homepage：极简导航页二次详解
> 分类：面板与工具
> 标签：docker、nas、群晖
> 原文：https://www.xinz.fun/archives/Homepage-JJ

> **导读**：这篇围绕「Homepage：极简导航页二次详解」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾面板与工具的读者。执行前建议先备份原配置，并在测试环境验证。

官网：<https://gethomepage.dev/latest/>

GitHub：<https://github.com/gethomepage/homepage>

教程视频上集

[[老高分享]HomePage 一个好用、静态、快速、安全、可高度定制的应用、服务、Docker、控制台兼网站导航支持Emby Jellyfin Plex等\_哔哩哔哩\_bilibili](https://www.bilibili.com/video/BV1H5411C7WY/?spm_id_from=333.788&vd_source=1545f5f5d7ebb06efcf2126418416107)

教程视频下集

[[老高分享]HomePage导航下集 常见组件的设置 系统资源监控仪表盘glances安装设置PVE Portainer Emby 群晖 DS Docker为例\_哔哩哔哩\_bilibili](https://www.bilibili.com/video/BV1xZ42127eJ/?spm_id_from=333.788&vd_source=1545f5f5d7ebb06efcf2126418416107)

## 一、安装

**以Docker安装方式为例：**

使用docker compose:

```yaml
version: "3.3"
services:
  homepage:
    image: ghcr.io/gethomepage/homepage:latest
    container_name: homepage
    restart: unless-stopped
    environment:
      - PORT=3000
    ports:
      - "3000:3000"
    volumes:
      - /path/to/homepage/config:/app/config # 配置文件保存路径
      - /path/to/homepage/images:/app/public/images # 壁纸文件保存路径
      - /path/to/homepage/icons:/app/public/icons # 图标文件保存路径
      - /srv/volume_1:/volume_1:ro # 磁盘1路径，映射之后才会显示容量，根据你磁盘实际路径添加，照抄无效
      - /srv/volume_2:/volume_2:ro # 磁盘2路径，映射之后才会显示容量，根据你磁盘实际路径添加，照抄无效
      - /var/run/docker.sock:/var/run/docker.sock #  用于 Docker 集成
```

**1.2 启动**

```bash
docker compose up -d
```

使用Docker：

```bash
docker run --name homepage \
-e PUID=1000 \
-e PGID=1000 \
-p 3000:3000 \
-v /你的config目录:/app/config \
-v /var/run/docker.sock:/var/run/docker.sock:ro \
--restart unless-stopped \
ghcr.io/gethomepage/homepage:latest
```

非必要可选映射，一并添加到以上建立容器命令行中，作用是：增加本地icons图标库和本地图片库的映射目录，以便homepage在个人自定义时调用图片、图标。

```
-v /你的homepage/icons目录:/app/public/icons \
-v /你的/homepage/images目录:/app/public/images \
```

有小伙伴喜欢单行命令行，不喜欢分段。这里一并喂饭：以下单挑命令行和上面分段部署是同样的功能，二选一。

```bash
docker run 
--name homepage 
-p 3000:3000
 -v /你的config目录:/app/config
 -v /var/run/docker.sock:/var/run/docker.sock
 -v /你的homepage/icons目录:/app/public/icons
 -v /你的/homepage/images:/app/public/images ghcr.io/gethomepage/homepage:latest
```

**二、Homepage主要配置文件功能介绍**

1、settings.yaml

homepage的设置文件，用来设置：语言、布局、标题、favicon图标、背景图片等。

2、service.yaml

homepage的服务文件，用来设置：Docker或其他服务导航入口等。

3、widgets.yaml

homepage的小组件文件，用来设置：功能显示如：CPU、内存占用率、温度、上线时间等；搜索框、天气、日期和时间等。

4、bookmarks.yaml

homepage的书签文件，用来设置：网站收藏书签、书签图标、url等。

**三、常用功能设置**

**1、settings.yaml**

语言设置，如：简体中文

```
language: zh-CN
```

其他语言，按需设置：

ca, de, en, es, fr, he, hr, hu, it, nb-NO, nl, pt, ru, sv, vi, zh-CN, zh-Hant

标题设置，如：your title换成你需要的名字

```
title: your title
```

网页图标favicon设置，支持本地/http图片

```
favicon: https://www.baidu.com/favicon.ico
```

背景图片设置（**重点：从此处开始，多参数分段设置中，一定要注意层级关系，下层要比上层靠后比如多个空格（不能用制表符tab），同层对齐。否则会运行错乱**）如下：

```yaml
background:
  image: http://xxxxx.jpg
  blur: sm # sm, "", md, xl… see https://tailwindcss.com/docs/backdrop-blur
  saturate: 50 # 0, 50, 100… see https://tailwindcss.com/docs/backdrop-saturate
  brightness: 50 # 0, 50, 75… see https://tailwindcss.com/docs/backdrop-brightness
  opacity: 50 # 0-100
```

注：如仅需要1张图片做背景，无需风格，则保留image: http://xxxxx.jpg即可。下面依次为：模糊度、饱和度、亮度、不透明度。默认参数值如上。

布局设置每个人需求不同，按个人喜好自己搞吧。

**2、services.yaml**

官方给出的实例如下：

```
-- Group A:
    - Service A:
        href: http://localhost/
 
- Group B:
    - Service B:
        href: http://localhost/
```

以下为我们习惯的表述方式；

```
- 媒体影音:
    - EmbyServer:
        icon: emby.png
        href: http://x.x.x.x:8096/ # Emby IP:8096
        description: Movies & TV Shows
        ping: 127.0.0.1 # Emby IP
```

注1：层级，Group组和Service服务之前要用-，且上下级空格排列，下面参数要多几个空格对齐。

注2：homepage内置自带图标集合。使用的是如下开源图标集：

<https://github.com/walkxcode/dashboard-icons>

我们可以在icon参数中，直接调用。只要是以上图标集中存在的图标即可。具体操作见视频

注3：href中url结尾有/ 比如http://xxxx:1234/，与之后添加组件widget中的url不需要加/，两者是不同的

注4：description: 服务描述，可中/英文添加此服务的描述。

**还有常见的几个services.yaml中的参数如下：**

**ping**: x.x.x.x 或者 xxx.com/www.xxx.com IP地址或者域名都可以，测试添加http或者https，结尾添加端口也没问题比如https://ikuai.myddns.com:12345 结尾不要/

**widget:** 注意这里要区分，这是service服务的小组件，它是针对该服务的功能组件。与homepage的widgets.yaml组件是不同的。

举个栗子：

```
- 媒体影音:
    - EmbyServer:
        icon: emby.png
        href: http://x.x.x.x:8096/ # Emby IP:8096
        description: Movies & TV Shows
        ping: 127.0.0.1 # Emby IP
        widget:
          type: emby
          url: http://x.x.x.x:8096
          key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
          enableBlocks: true # optional, defaults to false
          enableNowPlaying: true # optional, defaults to true
```

> **注：type: emby 指定这个组件是emby的，**
>
> **url: Emby服务器的IP和端口号，注意此处不用/结尾**
>
> **key: 需要去EmbyServer中设置—高级——API密钥中生成，**
>
> **enableBlocks: 使能功能模块可以查看Emby中的剧集、影片等数据。默认是关闭的；**
>
> **enableNowPlaying: 使能正在播放模块，可以查看Emby正在播放的影片，并且可以控制暂定和继续播放，默认是关闭的。**

Homepage支持的服务非常多，每个具体的widget组件参数设置均不相同，具体可以查看：

<https://gethomepage.dev/latest/configs/service-widgets/>

支持的组件列表：<https://gethomepage.dev/latest/widgets/>

**对于Docker服务有几个常用的参数如下：**

以下这两参数是用在Docker服务上的，需要在docker.yaml中添加docker.sock的映射，具体操作见视频

```
server: my-server
container: my-container
```

以上两个参数添加后，Docker服务可以查看服务详情

Docker服务可添加自动展开服务详情的参数

```bash
showStats: true
```

**3、widgets.yaml** 此为homepage的功能组件，注意和service的widgets服务组件参数区分。

```
- resources:
    cpu: true
    memory: true
    disk: /
```

以上为默认的设置，还有常用的参数如下：添加时注意参数对齐

```
    cputemp: true # disabled by default
    uptime: true # disabled by default
    expanded: true # show the expanded view
```

比如上线时间、CPU使用率、温度范围最低最高等扩展显示

```
- search:
    provider: baidu
    target: _blank
```

以上为搜索框设置，可选搜索引擎：如百度、谷歌等，\_blank搜索结果开新页面显示

```
- openmeteo:
    label: 上海 # optional
    latitude: 31.2222
    longitude: 121.4581
    timezone: Asia/Shanghai # optional
    units: metric # or imperial
    cache: 5 # Time in minutes to cache API responses, to stay within limits
```

以上为天气组件：openmeteo，需要打开以下网站：

<https://open-meteo.com/en/docs>

根据您的所在区域，查找到经纬度和时区并添加到以上参数中。具体操作见我的视频

```
- datetime:
    text_size: xl
    format:
      dateStyle: short
      timeStyle: short
      hourCycle: h23
```

以上为日期和时间设置。有长短显示格式之分。12/24小时之分。具体可以见

<https://gethomepage.dev/latest/widgets/info/datetime/>

**4、bookmarks.yaml**

官方给出的默认实例如下：

```
- Developer:
    - Github:
        - abbr: GH
          href: https://github.com/
 
- Social:
    - Reddit:
        - icon: reddit.png
          href: https://reddit.com/
          description: The front page of the internet
 
- Entertainment:
    - YouTube:
        - abbr: YT
          href: https://youtube.com/
```

第一行-为标签分类，第二行-为网站，下面-跟的是设置参数

- icon: 网页图标，可使用内置图标（如上面官方示例中的- icon: reddit.png）具体支持的图标可以查看：<https://github.com/walkxcode/dashboard-icons>

也可使用http/https网页图标，如：https://www.baidu.com/favicon.ico

- abbr: 后加字母缩写，比如GitHub，可以缩写为GH，随意，仅作标识助记之用。

href: 后加网站url，以/结尾

---

**一、PVE组件设置**

1、在service.yaml中添加如下

在PVE模块下方添加以下组件代码

```
    widget:
      type: proxmox
      url: https://x.x.x.x:8006
      username: api_token_id
      password: api_token_secret
      node: pve # optional
```

**2、PVE中添加群组、用户、API令牌并为其添加权限**

**见操作视频**

**二、Portainer组件设置**

**1、在service.yaml中添加如下**

在Portainer模块下方添加以下组件代码

```
    widget:
      type: portainer
      url: https://portainer.host.or.ip:9443
      env: 1
      key: ptr_accesskeyaccesskeyaccesskeyaccesskey
```

**2、在Portainer中添加令牌**

**见操作视频**

**四、群晖及Download Station组件设置**

**1、在service.yaml中添加如下**

#在群晖模块下方添加以下组件代码

```
widget:
  type: diskstation
  url: http://diskstation.host.or.ip:port
  username: username
  password: password
  volume: volume_N # optional
 
#在Download Station模块下方添加以下组件代码
widget:
  type: downloadstation
  url: http://downloadstation.host.or.ip:port
  username: username
  password: password
```

**2、在群晖中添加管理员用户、设置目录访问和应用管理权限**

**见操作视频**

**五、系统资源监控仪表盘安装及设置**

**1、安装glances系统资源监控工具，推荐使用docker版，安装命令行如下：**

```bash
docker run --name glances
 -d --restart="always" 
-p 61208-61209:61208-61209 
-e GLANCES_OPT="-w" 
-v /opt/docker/glances/glances.conf:/glances/conf/glances.conf 
-v /:/host:ro -v /var/run/docker.sock:/var/run/docker.sock:ro --pid host nicolargo/glances:latest-full
```

**2、设置仪表盘布局**

打开settings.yaml文件，添加如下

```
layout:
  Moniter:
    style: row
    columns: 4
    header: false #不显示表头
```

**3、在service.yaml中添加如下**

```
- Moniter:
    - 系统信息:
        widget:
          type: glances
          url: http://x.x.x.x:61208
          metric: info
    - 处理器:
        widget:
          type: glances
          url: http://x.x.x.x:61208
          metric: cpu
    - 内存:
        widget:
          type: glances
          url: http://x.x.x.x:61208
          metric: memory
    - 进程:
        widget:
          type: glances
          url: http://x.x.x.x:61208
          metric: process
    - 网络:
        widget:
          type: glances
          url: http://x.x.x.x:61208
          metric: network:eth0
    - 硬盘:nvme0n1:
        widget:
          type: glances
          url: http://x.x.x.x:61208
          metric: disk:nvme0n1
    - 传感器:
        widget:
          type: glances
          url: x.x.x.x:61208
          metric: sensor:Package id 0
    - 文件系统:
        widget:
          type: glances
          url: x.x.x.x:61208
          metric: fs:/host
```

总结：以上主要4个yaml文件设置完成，Homepage的基础功能可以基本满足小伙伴们的需求。另外很多服务的功能组件设置比较复杂，需要逐一设置，比如Portainer、Emby、PVE等都是需要进入他们的管理页面，去设置API、Key、或者建立用户组和用户，开通需要的权限，否则组件不能用。也有部分服务有坑，比如群晖，按照官方流程操作下来，正确的用户名和密码，在群晖组件中运行会报400错误（用户或密码错误）认证识别而没有权限读取数据。这和服务本身有直接关系。老高抛砖引玉，期待各路大神小伙伴们分享更多Homepage的玩法。

转自:爱折腾的老高

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
