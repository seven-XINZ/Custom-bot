# docker全自动影视库

> 标题：docker全自动影视库
> 分类：影音媒体
> 标签：docker、Linux、jellyfin、nastoos
> 原文：https://www.xinz.fun/archives/video-nas

> **导读**：这篇围绕「docker全自动影视库」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾影音媒体的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 全自动影视库架构图
2. nas-toos安装
3. MoviePilot安装
4. Emby安装
5. 官方版
6. 开心版
7. EMBY优化及美化
8. qBittorrent安装
9. 改版镜像
10. 官方镜像
11. transmission安装
12. 安装Transmission-Web-Control
13. 以及其余 6 个小节

## 全自动影视库架构图

```
+-------------------------------------------------+
|                  全自动影视库                   |
|                                                 |
| +------------------+  +----------------------+ |
| |      Docker      |  |       NAS-Tools      | |
| |                  |  |                      | |
| |  +------------+  |  |  +----------------+  | |
| |  |   Emby     |  |  |  |  Web UI       |  | |
| |  +------------+  |  |  |  (http://IP:3000)| |
| |                  |  |  +----------------+  | |
| |  +------------+  |  |                      | |
| |  | qBittorrent |  |  +--------------------+ | |
| |  +------------+  |  |                      | |
| |  | transmission |  |  +--------------------+ | |
| |  +------------+  |  |                      | |
| |  | 其他支持组件 |  |  +--------------------+ | |
| | (如 Jackett, flaresolverr.)  |  |          | |
| |  +------------+  |  |                      | |
| |                  |  |  ( IYUU )  | |
| +------------------+  +----------------------+ |
|                                                 |
+-------------------------------------------------+
```

1.在linux下安装好Docker

2.安装 nas-toos

3.安装 emby 如需硬解请安装开心版

4.安装 qBittorrent

5.安装transmission

6.安装 jackeet

7.安装flaresolverr

8.如有 pt 站不需要操作下面步骤

9.安装iyuu

10.iyuu辅种转种设置

---

## nas-toos安装

安装命令

**安装命令不可直接复制请按需配置**

```bash
docker run -d \
    --name nas-tools \
    --hostname nas-tools \
    -p 3000:3000 \
    -v /opt/1panel/apps/nas-tools/config:/config \
    -v /sata/media:/media    `# 媒体目录，多个目录需要分别映射进来` \
    -e PUID=0 \
    -e PGID=0 \
    -e UMASK=000 \
    -e NASTOOL_AUTO_UPDATE=false \
    -e NASTOOL_CN_UPDATE=false \
    hsuyelin/nas-tools
```

### 安装命令解析

`docker run -d \`

`--name nas-tools \`

`--hostname nas-tools \`

`-p 3000:3000 # 默认的webui控制端口 \`

`-v $(pwd)/config:/config # 冒号左边请修改为你想在主机上保存配置文件的路径 \`

`-v /你的媒体目录:/你想设置的容器内能见到的目录 # 媒体目录，多个目录需要分别映射进来 \`

`-e PUID=0 # 想切换为哪个用户来运行程序，该用户的uid，详见下方说明 \`

`-e PGID=0 # 想切换为哪个用户来运行程序，该用户的gid，详见下方说明 \`

`-e UMASK=000 # 掩码权限，默认000，可以考虑设置为022 \`

`-e NASTOOL_AUTO_UPDATE=false # 如需在启动容器时自动升级程程序请设置为true \`

`-e NASTOOL_CN_UPDATE=false # 如果开启了容器启动自动升级程序，并且网络不太友好时，可以设置为true，会使用国内源进行软件更新 \`

`hsuyelin/nas-tools`

### ## 关于PUID/PGID的说明

`- 如在使用诸如emby、jellyfin、plex、qbittorrent、transmission、deluge、jackett、sonarr、radarr等等的docker镜像，请保证创建本容器时的PUID/PGID和它们一样。`

`` - 在docker宿主上，登陆媒体文件所有者的这个用户，然后分别输入`id -u`和`id -g`可获取到uid和gid，分别设置为PUID和PGID即可。 ``

`` - `PUID=0` PGID=0指root用户，它拥有最高权限，若你的媒体文件的所有者不是root，不建议设置为`PUID=0` PGID=0。 ``

### 使用说明

浏览器 你的ip:3000 或者你自定义端口 默认用户名 admin 密码 password

### nas-tools基础设置

#### 系统
#### 更改用户名和密码

![配图](/upload/image-qqlo.png)

#### 媒体

获取[TMDB](https://www.themoviedb.org/)api

[点击进入TMDB注册](https://www.themoviedb.org/)

进入设置查看api

![配图](/upload/image-sipr.png)

![配图](/upload/image-btxu.png)

获取tmdb api 填入

![配图](/upload/image-pacp.png)

根据需求设置刮削

![配图](/upload/image-zplr.png)

![配图](/upload/image-jkuw.png)

![配图](/upload/image-ctiv.png)

#### 服务

基本保持默认即可特殊需求除外

![配图](/upload/image-wdri.png)

**安全**

按需设置 无需求保持默认即可

![配图](/upload/image-yzjy.png)

#### CRO

按需设置 无需求保持默认即可

![配图](/upload/image-lruq.png)

#### 实验室

按需设置 无需求保持图片内容即可

![配图](/upload/image-yzkb.png)

#### 用户管理

自行添加额外访问用户

![配图](/upload/image-qcos.png)

#### 媒体库

这个是媒体库访问目录填写整理后的`links`目录

![配图](/upload/image-nxyc.png)

#### 目录同步

下载文件和媒体库自动同步

源目录为分类下载目录

目的目录是媒体库目录

使用硬链接即可

![配图](/upload/image-wxlx.png)

#### 消息通知

按需设置

![配图](/upload/image-ifzl.png)

#### 过滤规则

日常规则够用

![配图](/upload/image-dfej.png)

#### 下载器

配置你的下载器 qb举例

新增

![配图](/upload/image-krod.png)

![配图](/upload/image-tldu.png)

![配图](/upload/image-ghyi.png)

下载目录设置 和图片相同也可

![配图](/upload/image-iyci.png)

#### 媒体服务器

emby为例

根据说明填入地址

外部访问地址为你反代后的域名

![配图](/upload/image-ipsl.png)

![配图](/upload/image-jvkt.png)

---

## MoviePilot安装

**安装命令不可直接复制请按需配置**

```bash
docker run -itd \
    --name moviepilot \
    --hostname moviepilot \
    -p 30000:3000 \
    -v /sata/media:/media \
    -v /opt/1panel/apps/moviepilot/config:/config \
    -v /opt/1panel/apps/moviepilot/core:/moviepilot/.cache/ms-playwright \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -e 'NGINX_PORT=30000' \
    -e 'PORT=30001' \
    -e 'PUID=0' \
    -e 'PGID=0' \
    -e 'UMASK=000' \
    -e 'TZ=Asia/Shanghai' \
    -e 'AUTH_SITE=iyuu' \
    -e 'IYUU_SIGN=IYUUxxxxxxxxxxxxxxxxxxxxx' \
    -e 'SUPERUSER=admin' \
    -e 'API_TOKEN=api秘钥' \
    -e 'BIG_MEMORY_MODE=false' \
    --restart always \
    jxxghp/moviepilot:latest
```

```bash
docker run -itd \
    --name moviepilot \
    --hostname moviepilot \
    -p 30000:3000 \
    -v /sata/media:/media \
    -v /opt/1panel/apps/moviepilot/config:/config \
    -v /opt/1panel/apps/moviepilot/core:/moviepilot/.cache/ms-playwright \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -e 'NGINX_PORT=30000' \
    -e 'PORT=30001' \
    -e 'PUID=0' \                  # 设置为运行程序用户的 UID，通常是非 root 用户
    -e 'PGID=0' \                  # 设置为运行程序用户的 GID，通常是非 root 用户
    -e 'UMASK=000' \                   # 设置文件创建的权限掩码
    -e 'TZ=Asia/Shanghai' \            # 设置时区
    -e 'AUTH_SITE=iyuu,hhclub' \       # 设置多个认证站点，使用逗号分隔
    -e 'IYUU_SIGN=your_iyuu_sign' \    # 替换为实际的 IYUU 登录令牌
    -e 'HHCLUB_USERNAME=your_username' \ # 替换为 HHClub 用户名（如果使用 hhclub 作为认证站点）
    -e 'HHCLUB_PASSKEY=your_passkey' \  # 替换为 HHClub 密钥（如果使用 hhclub 作为认证站点）
    -e 'SUPERUSER=admin' \              # 超级管理员用户名
    -e 'API_TOKEN=your_api_token' \     # 替换为复杂的 API 密钥
    -e 'BIG_MEMORY_MODE=false' \         # 是否启用大内存模式
    -e 'DOH_ENABLE=true' \               # 启用 DNS over HTTPS
    -e 'GITHUB_TOKEN=your_github_token' \ # 替换为 GitHub token（用于提高 API 请求限流）
    -e 'TMDB_API_DOMAIN=api.themoviedb.org' \ # TMDB API 地址
    --restart always \
    jxxghp/moviepilot:latest
```

## Emby安装
## 官方版

**安装命令不可直接复制请按需配置**

```bash
docker run -d \
  --name emby \
  -p 8096:8096 \
  -p 8920:8920 \
  -v /opt/1panel/apps/embyks:/config \
  -v /sata/media:/media \
  emby/embyserver
```

- `-d`：后台运行容器。
- `--name emby`：容器名称为 `emby`。
- `-p 8096:8096`：将主机的 8096 端口映射到容器的 8096 端口。
- `-p 8920:8920`：将主机的 8920 端口映射到容器的 8920 端口。
- `-v emby:/emby`：将名为 `emby` 的数据卷挂载到容器的 `/emby` 目录。
- `emby/embyserver`：要运行的镜像名称。

***开心版和官方版区别于开启硬解 不需要则直接使用官版***

## 开心版

**安装命令不可直接复制请按需配置**

```bash
docker run -d \
  -v /opt/1panel/apps/embyks:/config \
  -v /sata/media:/media \
  --net=bridge \
  --restart=always \
  --device=/dev/dri:/dev/dri \
  --name Emby \
  -p 8096:8096 \
  -p 8920:8920 \
  amilys/embyserver:4.8.0.56
```

### 说明

- `-v`：用于挂载卷（volume），用于指定主机目录与容器目录的映射。
- `--net=bridge`：指定使用桥接网络。
- `--restart=always`：如果容器停止，则总是重启容器。
- `--device=/dev/dri:/dev/dri`：用于映射主机的显卡设备，以便进行硬件解码。
- `--name Emby`：为容器指定一个名称。
- `-p`：用于映射容器的端口到主机的端口。

### 开心版开启硬解

需要在终端运行一下命令

chmod 777 /dev/dri/render128

## EMBY优化及美化

### **emby调用外部播放器用户脚本,只支持网页**:

[篡改猴地址](https://greasyfork.org/en/scripts/459297-embylaunchpotplayer)

### 添加多种播放按钮

项目是这个 <https://github.com/bpking1/embyExternalUrl>，感谢bpking1大佬的付出。 成功后将有如下的排版显示：

![配图](/upload/emby_1-vvns.png)

先下载上面项目，解压后将其中`embyWebAddExternalUrl`目录复制到emby安装目录的`dashboard-ui`中。 再修改`dashboard-ui/index.html`文件，在`</head>`前添加：

```
<link rel="stylesheet" id="theme-css" href="embyWebAddExternalUrl/icons/ExternalPlayer.css" type="text/css" media="all" />
<script src="embyWebAddExternalUrl/embyLaunchPotplayer.js"></script>
```

如下：

![配图](/upload/emby_2-kxhc.png)

此时保存后刷新页面就可以看到相关的图标了。

进阶

原作者的`embyLaunchPotplayer.js` 中引用了`js cdn`的地址，有时候在某些环境下刷不出来，这里可以将其改为本地地址，具体来说就是编辑`embyLaunchPotplayer.js`文件将

```
https://fastly.jsdelivr.net/gh/bpking1/embyExternalUrl@0.0.5/
```

找到类似替换即可。也即是这部分:

更改下面代码到这个部分即可

```
(function () {
    'use strict';
    const useRealFileName = false;
    const iconConfig = {
        iconOnly: false,
        baseUrl: "embyWebAddExternalUrl/icons" // 本地图标路径
    };
```

### emby优化及美化

打开emby是不是感觉加载非常的慢，如果你的内存够用，可以在emby设置中找到数据库-数据库缓存，设置为2048即可，为什么设置成这个数字

![配图](/upload/image-jhxi-zfxf.png)

**接下来是美化教程，项目地址https://github.com/newday-life/emby-front-end-mod，也可以看下他的教程。执行以下脚本先安装插件，容器名字输入emby。然后重启emby容器。**

```bash
wget -O script.sh --no-check-certificate https://raw.githubusercontent.com/Shurelol/Emby.CustomCssJS/main/src/script.sh && bash script.sh
```

![配图](/upload/image-biny.png)添加自定义JavaScript，使用这个网站[点击打开](https://github.com/newday-life/emby-front-end-mod/blob/main/emby-swiper/emby-swiper.js)的内容。状态设置为强制使用，就能全部客户端生效了。另外一个自定义css用的这个网站[点击打开](https://github.com/jackloves111/EMBY.JS.CSS/blob/main/%E9%A1%B5%E9%9D%A2%E7%BE%8E%E5%8C%96%E5%90%88%E9%9B%86/emby.css)的。强制刷新CRTL+F5就能看到效果了。

![配图](/upload/image-dfdp_WG9bvc.png)

---

## qBittorrent安装

**安装命令不可直接复制请按需配置**

## 改版镜像

```bash
docker run -d \
  --name=qbittorrent \
  -p 7881:7881 \
  -p 7881:7881/udp \
  -p 18080:18080 \
  -v /opt/1panel/apps/qBittorrent/config:/etc/qBittorrent \
  -v /opt/1panel/apps/qBittorrent/data:/data \
  -v /sata/media/9kg:/9kg \
  -v /sata/media/bok/bokh:/bokh \
  -v /sata/media/bok/boks:/boks \
  -v /sata/media/tv:/tv \
  -v /sata/media/videotv:/videotv \
  -v /sata/media/video:/video \
  -v /sata/downloads:/downloads \
  --restart unless-stopped \
  helloz/qbittorrent
```

- 7881：用于传入连接的端口，TCP/UDP都需要映射，且主机端口和[容器](https://cloud.tencent.com/product/tke?from_column=20065&from=20065)端口必须一致，否则无法下载和上传
- 18080：qBittorrentWEBUI访问端口，主机端口和容器端口必须一致，否则无法打开WEB界面
- /data/qbittorrent/config：qbittorrent配置[文件存储](https://cloud.tencent.com/product/cfs?from_column=20065&from=20065)目录，可自行修改
- /data/qbittorrent/downloads：下载目录，可自行修改

### 使用说明

运行成功后可通过`http://IP:18080`进行访问，用户名为`admin`，密码为`adminadmin`，默认已经设置为了中文界面。

---

## 官方镜像

```bash
docker run -d \
  --name=qbittorrent \
  --network host \
  -e PUID=0 \
  -e PGID=0 \
  -e TZ=Asia/Shanghai \
  -e WEBUI_PORT=18080 \
  -e TORRENTING_PORT=6881 \
  -v /opt/1panel/apps/qBittorrent/config:/config \
  -v /sata/downloads:/downloads \
  -v /sata/media/9kg:/9kg \
  -v /sata/media/bok/bokh:/bokh \
  -v /sata/media/bok/boks:/boks \
  -v /sata/media/tv:/tv \
  -v /sata/media/videotv:/videotv \
  -v /sata/media/video:/video \
  --restart unless-stopped \
  linuxserver/qbittorrent:latest
```

**WEBUI\_PORT=18080** 根据自己需求更改 webui 访问端口

- 7881：用于传入连接的端口，TCP/UDP都需要映射，且主机端口和[容器](https://cloud.tencent.com/product/tke?from_column=20065&from=20065)端口必须一致，否则无法下载和上传
- 18080：qBittorrentWEBUI访问端口，主机端口和容器端口必须一致，否则无法打开WEB界面
- /data/qbittorrent/config：/config qbittorrent配置[文件存储](https://cloud.tencent.com/product/cfs?from_column=20065&from=20065)目录，可自行修改 : 左边的内容
- /data/qbittorrent/downloads：/downloads 下载目录，可自行修改 : 左边的内容

### 使用说明

运行成功后可通过`http://IP:18080`进行访问，用户名为`admin`，密码`查看容器日志`

---

## transmission安装

**安装命令不可直接复制请按需配置**

```bash
docker run -d \
  --name=transmission \
  --network=host \
  -e PUID=0 \
  -e PGID=0 \
  -e TZ=Etc/UTC \
  -e TRANSMISSION_WEB_HOME="/webui" \
  -e USER=seven \
  -e PASS=sevenchen \
  -e PEERPORT="51453" \
  -v /opt/1panel/apps/transmission/config:/config \
  -v /sata/media/videotv:/videotv \
  -v /sata/media/video:/video \
  -v /sata/media/tv:/tv \
  -v /sata/media/9kg:/9kg \
  -v /sata/media/bok:/bok \
  -v /opt/1panel/apps/transmission/webui:/webui \
  --restart unless-stopped \
  dockers.cn.com/linuxserver/transmission:latest
```

## 安装Transmission-Web-Control

运行完启动Docker容器的命令后就可以来安装WebUI了

**下载压缩包**：

- 你可以使用`wget`命令直接从GitHub下载压缩包。打开终端并运行以下命令：

```bash
wget https://github.com/ronggang/transmission-web-control/archive/refs/tags/v1.6.1-update1.zip -O /tmp/transmission-web-control.zip
```

**解压缩文件**：

- 下载完成后，将压缩包中的`src`文件夹内的内容解压到目标目录`/opt/transmission/webui`。可以使用`unzip`和`mv`命令来完成此操作：

```
unzip /tmp/transmission-web-control.zip "transmission-web-control-1.6.1-update1/src/*" -d /tmp
sudo mv /tmp/transmission-web-control-1.6.1-update1/src/* /opt/transmission/webui
```

### **src**内的全部文件

[**![配图](https://www.xinz.fun/upload/9b924390357e943aba1082ebe1c48e4e.png)**](https://www.xinz.fun/upload/9b924390357e943aba1082ebe1c48e4e.png)

[**![配图](https://www.xinz.fun/upload/09817f27198db894d48e377dfde27c69.png)**](https://www.xinz.fun/upload/09817f27198db894d48e377dfde27c69.png)

[**![配图](https://www.xinz.fun/upload/11374be6d6654999fadd52f88241eac2.png)**](https://www.xinz.fun/upload/11374be6d6654999fadd52f88241eac2.png)

备用地址下载到本地自己上传 : [**点击即可下载**](https://al.xinz.fun:5244/d/xinz.fun/xinz/%E5%A4%87%E4%BB%BD/src.zip?sign=Q5IpEoMVIljARzJrr4P0kTVVdlRprpezYM8m4C92Fc0=:0)

接下来访问IP:9091输入账号密码就可以正常使用transmission了

## jackett安装

**安装命令不可直接复制请按需配置**

```bash
docker run -d \
  --name=jackett \
  -e PUID=0 \
  -e PGID=0 \
  -e TZ=Asia/Shanghai \
  -p 9117:9117 \
  -v /opt/1panel/apps/jackett/config:/config \
  --restart unless-stopped \
  linuxserver/jackett
```

### 命令解析：

- `docker run`: 这个命令用于创建并启动一个新的容器。
- `-d`: 这个标志表示以分离模式（在后台）运行容器。
- `--name=jackett`: 这个选项将容器的名称设置为 "jackett"。
- `-e PUID=100`: 这个选项设置一个环境变量 `PUID` 为 `100`，通常用于指定容器内应用程序运行的用户 ID。
- `-e PGID=100`: 这个选项设置一个环境变量 `PGID` 为 `100`，用于指定应用程序运行的组 ID。
- `-e TZ=Asia/Shanghai`: 这个选项将容器的时区设置为 "Asia/Shanghai"。
- `-p 9117:9117`: 这个选项将主机的 `9117` 端口映射到容器的 `9117` 端口，使你可以通过主机的 IP 地址在该端口访问 Jackett。
- `-v /opt/1panel/apps/jackett/config:/config`: 这个选项挂载一个卷，意味着主机上的目录 `/opt/1panel/apps/jackett/config` 将作为容器内 Jackett 的配置目录。这允许你在删除容器后保留配置数据。
- `--restart unless-stopped`: 这个标志告诉 Docker 除非手动停止容器，否则会自动重启容器。这对于确保容器在重新启动或崩溃后保持运行非常有用。
- `linuxserver/jackett`: 这个选项指定要使用的 Docker 镜像，即来自 Docker Hub 的官方 Jackett 镜像。

## `flaresolverr安装`

**安装命令不可直接复制请按需配置**

```bash
docker run -d \
  --name=flaresolverr \
  -p 8191:8191 \
  -e LOG_LEVEL=info \
  -e TEST_URL=https://www.baidu.com \
  --restart unless-stopped \
  ghcr.io/flaresolverr/flaresolverr:latest
```

- `docker run -d`: 在后台启动一个新的容器。
- `--name=flaresolverr`: 给这个容器命名为 `flaresolverr`。
- `-p 8191:8191`: 将主机的 `8191` 端口映射到容器的 `8191` 端口，使你可以通过访问主机的 `8191` 端口来访问容器内部的服务。
- `-e LOG_LEVEL=info`: 设置环境变量 `LOG_LEVEL` 为 `info`，这通常用于控制日志的详细程度。
- `-e TEST_URL=https://www.baidu.com`: 设置环境变量 `TEST_URL` 为 `https://www.baidu.com`，这可能用于配置 `flaresolverr` 服务所需的 URL。
- `--restart unless-stopped`: 设置容器的重启策略为“除非手动停止”，即容器在崩溃或主机重启后会自动重新启动。
- `ghcr.io/flaresolverr/flaresolverr:latest`: 指定要使用的 Docker 镜像，这里是 `flaresolverr` 的最新版本。

## IYUU安装

**安装命令不可直接复制请按需配置**

```bash
docker run -itd \
    -v /opt/1panel/apps/IYUU/iyuu:/iyuu \
    -v /opt/1panel/apps/IYUU/data:/data \
    -p 8780:8780 \
    --name IYUUPlus \
    --restart=always \
    iyuucn/iyuuplus-dev:latest
```

| **参数** | **解释** |
| --- | --- |
| `--name` | 容器名字 |
| `-v` | 资源挂载到容器，冒号分隔 本地目录文件:容器目录文件 |
| `-p` | 本地端口绑定到容器端口，冒号分隔 本地端口:容器端口 |
| `--net=host` | 容器所使用的网络模式。 |
| `--restart` | 启动模式 |
| `iyuucn/iyuuplus-dev:latest` | `iyuu/iyuuplus-dev`是镜像名字，`latest`是标签名 |

**关于 8780 端口**

**通过docker安装的用户只需要绑定一个** `8780` 端口

注：`8780`是容器内nginx的监听端口，反向代理了 `8787`、`3131`

**注意**

安装时需要挂载两个目录和一个端口；

容器内目录`/iyuu`和`/data`为固定值，他们是**兄弟关系**，不是父子关系，切勿套娃。

本地目录`/root/iyuu`挂载到容器内`/iyuu`（存放源码）；

本地目录`/root/data`挂载到容器内`/data`（存放mysql数据库）；

**你可以自定义本地目录**`/root/iyuu`和`/root/data`

## **访问**[****](https://doc.iyuu.cn/guide/getting-started#setup-wizard)

您可以访问WEBUI安装界面，从而进行下一步；如您是在IP地址为`192.168.1.11`的局域网机器，通过docker安装的IYUU，那么地址就是`http://192.168.1.11:8780`

在浏览器中访问 URL 以查看IYUU的运行情况吧！

**本机IP地址127.0.0.1**

如果您是通过本机的docker安装的，那么地址就是：

`http://127.0.0.1:8780` 或 `http://localhost:8780`

## IYUU辅种转种

## 首先添加你的下载器

![配图](/upload/ef066c53dfcc195e0958dee9779963c1.png)

### 添加图中的内容 提示一下 tr 好像需要反代后才有用户名和密码

![配图](/upload/2b74473cbe2cc07b707fa8bc0c7ccb96.png)

### 种子目录来源

qb安装目录 /opt/1panel/apps/qBittorrent/config/data/BT\_backup:/qbzz

/qbzz 按你喜好修改

tr安装目录 /opt/1panel/apps/transmission/config/torrents:/trzz

/trzz 按你喜好修改

![配图](/upload/image-bfbu.png)

目录用于转种使用 因为我不需要转移下载的文件所以 qb 和 tr 都映射相同的路径 默认下载路径是必须要自己映射的 其它下载路径自定义

### 设置辅种和转种任务

![配图](/upload/41a5bec100f567e82a0c6d240d7ea552.png)

### 先设置辅种

![配图](/upload/image-pfry.png)

### 设置转种任务

![配图](/upload/image-ciid.png)

### 先设置转种后暂停

![配图](/upload/image-pelg.png)

检查任务成功否

查看日志先点左边然后再点右边

![配图](/upload/image-gnjd.png)

可以看到输出日志

![配图](/upload/image-yukw.png)

再设置转种后开始任务并自动删源种

![配图](/upload/image-lwjt.png)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
