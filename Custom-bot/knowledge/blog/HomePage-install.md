# HomePage导航页部署教程

> 标题：HomePage导航页部署教程
> 分类：面板与工具
> 标签：docker、Linux、nas、群晖
> 原文：https://www.xinz.fun/archives/HomePage-install

> **导读**：这篇是「HomePage导航页部署教程」的实操教程。下文按「一、部署」「一、1 创建docker-compose.yaml文件」「二、配置HomePage」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾面板与工具的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 一、部署
2. 一、1 创建docker-compose.yaml文件
3. 二、配置HomePage
4. 二、1 配置settings.yaml
5. 二、2 配置widgets.yaml
6. 二、3 配置services.yaml
7. 二、4 配置docker.yaml
8. 二、5 配置bookmarks.yaml

**效果展示**

![配图](/upload/AgAABTPCXbbbL4GIvItHdLgwx0D4zd39.png)

## 一、部署
## 一、1 创建docker-compose.yaml文件

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

### 详细解释

1. **version: "3"**

   - 定义了Docker Compose文件的版本。这里使用的是版本3。
2. **services**

   - 定义了一组服务。在这里，只有一个服务`homepage`。
3. **homepage**

   - 服务名称，表示一个单独的容器实例。
4. **image: ghcr.io/gethomepage/homepage:latest**

   - 指定了要使用的Docker镜像。`ghcr.io/gethomepage/homepage:latest`是镜像的地址和标签，`latest`表示使用最新版本的镜像。
5. **container\_name: homepage**

   - 设置容器的名称为`homepage`。这样更容易管理和识别该容器。
6. **restart: unless-stopped**

   - 配置容器的重启策略。`unless-stopped`表示容器会自动重启，除非手动停止容器。
7. **environment**

   - 设置环境变量：

     - `PUID=1000`：设置容器内应用程序使用的用户ID。
     - `PGID=1000`：设置容器内应用程序使用的组ID。 这些变量用于确保容器内应用程序以指定的用户和组权限运行，通常用于文件和目录权限管理。
8. **ports**

   - 端口映射，格式为`"主机端口:容器端口"`：

     - `3000:3000`：将主机的3000端口映射到容器的3000端口。可以根据需要更改主机端口，以避免端口冲突或增加安全性。
9. **volumes**

   - 卷挂载，用于将主机的目录或文件挂载到容器内：

     - `/volume1/docker/homepage/config:/app/config`：将主机的配置文件目录挂载到容器内的`/app/config`。
     - `/volume1/docker/homepage/images:/app/public/images`：将主机的壁纸文件目录挂载到容器内的`/app/public/images`。
     - `/volume1/docker/homepage/icons:/app/public/icons`：将主机的图标文件目录挂载到容器内的`/app/public/icons`。
     - `/volume_1:/volume_1:ro`：将主机的磁盘1路径挂载到容器内，`ro`表示只读挂载。根据实际磁盘路径修改。
     - `/volume_2:/volume_2:ro`：将主机的磁盘2路径挂载到容器内，`ro`表示只读挂载。根据实际磁盘路径修改。
     - `/run/docker.sock:/var/run/docker.sock`：将Docker套接字文件挂载到容器内，用于Docker集成。这允许容器内的应用与Docker守护进程通信，通常用于监控或管理其他容器。

### 如何使用

1. **创建**`docker-compose.yml`**文件：** 在你的项目目录下创建一个名为`docker-compose.yml`的文件，并将上面的内容粘贴进去。

**启动容器：** 在终端中导航到包含`docker-compose.yml`文件的目录，然后运行以下命令来启动容器：

```bash
sudo docker-compose up -d
```

`-d`标志表示在后台运行容器。

1. **访问HomePage导航页：** 打开浏览器，访问`http://<你的服务器IP>:3000`，你应该能看到HomePage导航页的界面。

### 其他注意事项

- **端口设置：** 如果你在公共网络中运行此服务，建议修改主机端口为一个不常见的端口，以增加安全性。例如，将`3000`改为`12345`，即`"12345:3000"`。
- **文件路径：** 确保你挂载的主机路径是正确的，并且这些路径存在。
- **权限：** 确保设置的`PUID`和`PGID`对应的用户和组在你的系统中存在，并且有适当的权限访问挂载的目录。

如无法直接从ghcr.io拉取镜像，可先通过<https://dockerproxy.com/>容器镜像代理站拉取，镜像拉下来之后再启动。容器镜像代理站拉取教程打开网址即可看到。

## 二、配置HomePage
## 二、1 配置settings.yaml

**官方帮助页面：**<https://gethomepage.dev/latest/configs/settings/>

```yaml
---
# For configuration options and examples, please see:
# https://gethomepage.dev/latest/configs/settings

providers:
  openweathermap: openweathermapapikey
  weatherapi: weatherapiapikey

# 自定义页面的标题
title: Homepage
# 背景不透明度和滤镜
background:
# 背景壁纸路径
  image: /images/wallhaven.png
# 模糊程度
  blur: sm # sm, "", md, xl... see https://tailwindcss.com/docs/backdrop-blur
# 饱和度，范围 0-100
  saturate: 100 # 0, 50, 100... see https://tailwindcss.com/docs/backdrop-saturate
# 亮度，范围 0-100
  brightness: 75 # 0, 50, 75... see https://tailwindcss.com/docs/backdrop-brightness
#不透明度，范围 0-100
  opacity: 100
# 卡背景模糊
cardBlur: md # sm, "", md, etc... see https://tailwindcss.com/docs/backdrop-blur
layout:
  重要服务:
#   tab: First  #分页标题
#    header: false  #隐藏布局中每个部分的标题
    style: column  #可设置“列“或“行“ "column" or "row"
    columns: 3
  系统监测:
#   tab: First
#    header: false  #隐藏布局中每个部分的标题
    style: column  #可设置“列“或“行“ "column" or "row"
    columns: 3
  下载服务:
#   tab: First  #分页标题
#    header: false  #隐藏布局中每个部分的标题
    style: column  #可设置“列“或“行“ "column" or "row"
    columns: 3
    useEqualHeights: true # 服务组启用等高卡
  观影日历:
#   tab: First  #分页标题
#    header: false  #隐藏布局中每个部分的标题
    style: column  #可设置“列“或“行“ "column" or "row"
    columns: 1
  影音服务:
#   tab: First  #分页标题
#    header: false  #隐藏布局中每个部分的标题
    style: row  #可设置“列“或“行“ "column" or "row"
    columns: 2
    useEqualHeights: true # 服务组启用等高卡
  常用:
#    header: false  #隐藏布局中每个部分的标题
#   tab: Second  #分页标题
    style: row  #可设置“列“或“行“ "column" or "row"
    columns: 3
  书签:
#    header: false  #隐藏布局中每个部分的标题
#   tab: Second  #分页标题
    style: row  #可设置“列“或“行“ "column" or "row"
    columns: 5
# 标题样式(underlined,boxed,clean,boxedWidgets)
headerStyle: underlined
# 设置语言
language: zh-CN
# 首页版本
hideVersion: true
# 状态风格
# statusStyle: "basic" # basic or dot
# 显示 Docker 统计信息
# showStats: true
```

## 二、2 配置widgets.yaml

**官方帮助页面：**<https://gethomepage.dev/latest/widgets/>

```
---
# For configuration options and examples, please see:
# https://gethomepage.dev/latest/configs/widgets
# 获取系统运行状态
- resources:
    label: 系统状态
    expanded: true
    cpu: true
    memory: true
    cputemp: true
    uptime: true
    units: metric # only used by cpu temp
    refresh: 3000 # optional, in ms
# 获取磁盘容量状态，多磁盘需提前映射进容器中。
- resources:
    label: 存储空间
    expanded: true
    disk:
      - /
      - /volume_1
      - /volume_2
# 设置搜索工具
- search:
    provider: [baidu, google, bing]
    target: _blank
# 设置天气
- openmeteo:
    label: 广州 # optional
    latitude: 23.129110 # Guangzhou's latitude
    longitude: 113.264385 # Guangzhou's longitude
    timezone: Asia/Shanghai # China Standard Time
    units: metric # or imperial
    cache: 5 # Time in minutes to cache API responses, to stay within limits
# 设置日期和时间
- datetime:
    text_size: xl
    locale: zh-CN
    format:
      dateStyle: long    # long or short
      timeStyle: short   # long or short
      hourCycle: h23
```

## 二、3 配置services.yaml

**官方帮助页面：**<https://gethomepage.dev/latest/configs/services/>

```
---
# For configuration options and examples, please see:
# https://gethomepage.dev/latest/configs/services

- 重要服务:
    - Portainer:
        icon: /icons/portainer-alt.png
        href: http://192.168.xx.xx:9000
        description: 一个简单的Docker管理解决方案。
        siteMonitor: http://192.168.xx.xx:9000
        server: my-docker
        container: portainer
        widget:
          type: portainer
          url: http://192.168.xx.xx:9000
          env: 2
          key: 
- 系统监测:
    - DiskStation:
        icon: /icons/synology-dsm.png
        href: https://192.168.xx.xx:5001
        description: 专属私有云盘——群晖NAS。
        siteMonitor: https://192.168.xx.xx:5001
        widget:
          type: diskstation
          url: https://192.168.xx.xx:5001
          username: 
          password: 
          volume: volume_1 # optional
- 下载服务:
    - Transmission:
        icon: /icons/transmission.png
        href: http://192.168.xx.xx:9091
        description: 一个功能强大且易于使用的BitTorrent客户端。
        siteMonitor: http://192.168.xx.xx:9091
        server: my-docker
        container: transmission
        widget:
          type: transmission
          url: http://192.168.xx.xx:9091
          username: test
          password: test
          rpcUrl: /transmission/ # Optional. Matches the value of "rpc-url" in your Transmission's settings.json file
- 观影日历:
    - 日历:
        widget:
          type: calendar
          firstDayInWeek: Monday
          view: monthly
          maxEvents: 10
          showTime: true
          timezone: Asia/Shanghai
- 影音服务:
    - Jellyfin:
        icon: /icons/jellyfin.png
        href: http://192.168.xx.xx:8096
        description: 一个自由软件媒体系统。
        siteMonitor: http://192.168.xx.xx:8096
        server: my-docker
        container: jellyfin
        widget:
          type: jellyfin
          url: http://192.168.xx.xx:8096
          key: test
          enableBlocks: true # optional, defaults to false
          enableNowPlaying: true # optional, defaults to true
- 常用:
    - Debian:
        icon: /icons/debian.png
        href: https://192.168.xx.xx:9090
        description: 一个完全自由的操作系统！
        siteMonitor: https://192.168.xx.xx:9090
    - Chromium:
        icon: /icons/chromium.png
        href: https://192.168.xx.xx:3001
        description: 由Google主导开发的网页浏览器。
        siteMonitor: http://192.168.xx.xx:3001
        server: my-docker
        container: chromium
```

## 二、4 配置docker.yaml

**官方帮助页面：**<https://gethomepage.dev/latest/configs/docker/#using-docker-socket-proxy>

```
---
# For configuration options and examples, please see:
# https://gethomepage.dev/latest/configs/docker/

# my-docker:
#   host: 127.0.0.1
#   port: 2375

my-docker:
  socket: /var/run/docker.sock
```

## 二、5 配置bookmarks.yaml

**官方帮助页面：**<https://gethomepage.dev/latest/configs/bookmarks/>

```
---
# For configuration options and examples, please see:
# https://gethomepage.dev/latest/configs/bookmarks

- 书签:
    - Github:
        - abbr: GH
          href: https://github.com/
    - XPEnology:
        - abbr: XP
          href: http://xpenology.com/forum/
    - Synology:
        - abbr: SY
          href: https://www.synology.com/
    - IPThreat:
        - abbr: IP
          href: https://ipthreat.net/
    - HomePage:
        - abbr: HP
          href: https://gethomepage.dev/
```

官网：<https://gethomepage.dev/>

教程结束！

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
