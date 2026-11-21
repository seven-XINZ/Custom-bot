# [DSM & Docker容器]自动家庭影片系统-搭建Jackett和flaresolverr

> 标题：[DSM & Docker容器]自动家庭影片系统-搭建Jackett和flaresolverr
> 分类：影音媒体
> 标签：docker、Linux、nas、群晖
> 原文：https://www.xinz.fun/archives/Jackett-flaresolverr

> **导读**：这篇是「[DSM & Docker容器]自动家庭影片系统-搭建Jackett和flaresolverr」的实操教程。下文按「前言」「安装」「可能遇到的问题」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾影音媒体的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 前言
2. 安装
3. 可能遇到的问题
4. DOCKER命令安装

## 前言

**全文摘要** 本文详细介绍了如何为家庭影片系统搭建自动化工具，包括Jackett和FlareSolverr的安装和配置。Jackett是一个跨平台的开源应用，用于集成种子站点并通过API响应查询。FlareSolverr是一个代理服务器，用于绕过Cloudflare和DDoS-GUARD保护。文章通过Docker在群晖系统中安装并配置了这两个工具，以实现自动获取影片资源种子信息的功能。

**关键段落**

- **Jackett介绍**: Jackett是一个跨平台的开源应用，支持OSX、Windows和Linux平台，集成了众多种子站，可作为代理服务器通过API响应查询，用于搜索种子信息或为其他工具提供信息源。
- **什么是 Jackett ？**

  > Jackett 是跨平台的开源应用，支持 OSX ，Windows 和 Linux 平台，集成了众多种子站，可作为代理服务器通过 API 来响应来自应用程序（ Sonarr ， Radarr ，SickRage ，CouchPotato ，Mylar ，Lidarr ，DuckieTV ，qBittorrent ，Nefarious 等）的查询，然后将结果发送回请求软件。
  >
  > Jackett 的用途有两个：一个是可以直接在 Jackett 中进行搜索，另一个就是给其他工具提供信息源。

  我们将使用Jeckett搭配bt/pt站,实现为家庭影片系统的其他工具应用提供影片资源的种子信息自动获取
- **FlareSolverr介绍**: FlareSolverr是一个绕过Cloudflare和DDoS-GUARD保护的代理服务器，与Jackett搭配使用，因为Jackett自身没有绕过Cloudflare的ddos验证机制。
- **什么是flaresolverr?**

  > FlareSolverr是一个绕过Cloudflare和DDoS-GUARD保护的代理服务器。

  jackett需要和flaresolverr搭配使用,因为jackett自身是没有绕过cloudflare的ddos验证机制,而大部分网站都使用了cloudflare的CDN服务,需要使用flaresolverr来绕过此机制.
- **Docker安装**: 文章通过Docker在群晖系统中安装Jackett和FlareSolverr，详细说明了下载容器镜像、创建容器、设置端口和环境变量的步骤。
- **Jackett页面设置**: 容器配置完成后，通过局域网访问Jackett界面，添加所需的BT/PT站，配置FlareSolverr API URL。
- **可能遇到的问题**: 包括下载docker镜像时长时间无反应或报错，提供了通过SSH命令拉取镜像和设置国内docker镜像源两种解决方法。
- **DOCKER命令安装**: 提供了Jackett和FlareSolverr的DOCKER命令安装详解，包括设置容器名称、用户ID、组ID、时区、端口映射和自动重启选项。

## 安装

我们将使用群晖系统中的docker进行以上两款工具的安装(其他系统的docker安装大同小异,可以参考使用)

### 1.下载容器镜像

在群晖"docker"的注册表中搜索`linuxserver/jackett`和`flaresolverr/flaresolverr`,双击选择下载

[![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_0.jpg?resize=640%2C369&ssl=1)](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_0.jpg?ssl=1)

[![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_flaresolverr_0.jpg?resize=640%2C369&ssl=1)](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_flaresolverr_0.jpg?ssl=1)

### 2.创建docker容器
#### jackett容器设置

1.在"映像"栏中找到我们刚才下载的linuxserver/jackett镜像,双击创建容器,选择`高级设置`.

[![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_1.jpg?resize=640%2C453&ssl=1)](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_1.jpg?ssl=1)

2."高级设置"中开启`启用自动重新启动`

[![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_2.jpg?resize=640%2C542&ssl=1)](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_2.jpg?ssl=1)

3."存储空间"添加容器保存配置和数据的文件夹(这里我已经提前创建好了文件夹,各位可以仿照我的设置,或者根据自己需求自行选择数据保存地址,建议单独创建一个共享文件夹以保存docker数据)

装载路径填写为`/config`

[![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_3.png?resize=640%2C540&ssl=1)](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_3.png?ssl=1)

4."端口设置"本地端口设置为`9117`

[![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_4.png?resize=640%2C540&ssl=1)](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_4.png?ssl=1)

5."环境"中添加`TZ`环境变量为`Asia/shanghai`,以设置时区

[![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_5.png?resize=640%2C536&ssl=1)](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_5.png?ssl=1)

5.点击右下角`应用`后依次点击`下一步`-`确定`,完成容器创建.

[![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_6.png?resize=640%2C458&ssl=1)](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_6.png?ssl=1)

#### flaresolverr容器设置

1.跟上面同理,"高级设置"中开启`启用自动重新启动`

[![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_flaresolverr_1.png?resize=640%2C302&ssl=1)](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_flaresolverr_1.png?ssl=1)

2."端口设置"本地端口设置成8191(该容器不需要存储数据,故跳过"存储空间"设置)

[![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_flaresolverr_2.png?resize=640%2C283&ssl=1)](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_flaresolverr_2.png?ssl=1)

3."环境"中添加`TZ`环境变量为`Asia/shanghai`,以设置时区

注意:机器如果在国内,建议另外添加一个变量`TEST_URL`为`https://www.baidu.com`,因为该镜像启动时会访问google以验证网络连通性,但是国内是访问不了的,所以需要修改测试地址

[![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_flaresolverr_3.png?resize=640%2C539&ssl=1)](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_flaresolverr_3.png?ssl=1)

之后完成容器创建

### 3.jackett页面设置

上面容器配置完后,在同局域网内即可通过`http://你群晖机子IP地址:9117`访问Jackett界面

点击上方`Add indexer`按钮,添加自己所需的BT/PT站(这里不做推荐,请自行查找)

[![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_7.png?resize=640%2C313&ssl=1)](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_7.png?ssl=1)

之后将页面拉到最底下,在`FlareSolverr API URL:`一栏中填写`http://你群晖机子IP地址:8191`(建议将下方`FlareSolverr Max Timeout (ms):`改为60000)

[![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_8.png?resize=640%2C313&ssl=1)](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_8.png?ssl=1)

**至此,本章Jackett和flaresolverr的搭建和配置已完成**

## 可能遇到的问题
### 1.下载docker镜像时长时间卡在"加载中"无反应或报错"操作超时"等情况

有两个解决办法:

#### 第一种方法

在群晖的`控制面板`-`终端和snmp`开启ssh功能(默认端口为22)

[![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_10.png?resize=640%2C365&ssl=1)](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_10.png?ssl=1)

之后可以通过各类ssh工具(如Putty,xshell等)连接到群晖,直接使用命令拉取docker镜像

```bash
sudo -i
```

|  |  |
| --- | --- |
|  | //切换成root |
|  |  |
|  | docker pull linuxserver/jackett |
|  | //这里的linuxserver/jackett可以换成任意你需要拉取的镜像名 |

#### 第二种方法

在docker注册表页面左上角`设置`,选中`Docker Hub`后,点击上方`编辑`,打开`启用注册表镜像`选项,添加国内docker镜像源(如网易的<https://hub-mirror.c.163.com/> 科大的<https://docker.mirrors.ustc.edu.cn/>)

![配图](https://i0.wp.com/blog.mstg.top/wp-content/uploads/docker_jackett_9.png?resize=640%2C368&ssl=1)

## DOCKER命令安装

jackett

```bash
docker run -d \
  --name=jackett \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Asia/Shanghai \
  -p 9117:9117 \
  -v /opt/1panel/apps/jackett/config:/config \
  --restart unless-stopped \
  jackett/jackett
```

#### 命令详解

- `docker run -d`: 以分离模式运行容器。
- `--name=jackett`: 给容器命名为 `jackett`。
- `-e PUID=1000`: 设置容器内的用户 ID，通常用于文件权限。
- `-e PGID=1000`: 设置容器内的组 ID，通常用于文件权限。
- `-e TZ=Asia/Shanghai`: 设置时区为上海。
- `-p 9117:9117`: 将主机的 9117 端口映射到容器的 9117 端口。
- `-v /opt/1panel/apps/jackett/config:/config`: 将主机的配置目录挂载到容器内的 `/config` 目录。
- `--restart unless-stopped`: 容器在停止后会自动重启，除非手动停止。
- `jackett/jackett`: 使用 Jackett 的 Docker 镜像。

#### 启动 Jackett

在运行上述命令后，Jackett 将在后台启动。您可以通过访问 `http://localhost:9117` 来查看 Jackett 的 Web 界面。

#### 配置 Jackett

1. **添加索引器**：在 Jackett 的 Web 界面中，您可以添加不同的 torrent 索引器。
2. **获取 API 密钥**：在设置页面中找到 API 密钥，以便在其他应用（例如 Node.js 脚本）中调用 Jackett 的 API。

### FlareSolverr

```bash
docker run -d \
  --name=flaresolverr \
  -e TZ=Asia/Shanghai \
  -e TEST_URL=https://www.baidu.com \
  -p 8191:8191 \
  --restart unless-stopped \
flaresolverr/flaresolverr:latest
```

#### 命令详解

- `docker run -d`: 以分离模式运行容器。
- `--name=flaresolverr`: 给容器命名为 `flaresolverr`。
- `-e TZ=Asia/Shanghai`: 设置容器的时区为上海。
- `-e TEST_URL=https://www.baidu.com`: 设置测试 URL，以确保容器在国内运行时能够验证网络连通性。
- `-p 8191:8191`: 将主机的 8191 端口映射到容器的 8191 端口。
- `--restart unless-stopped`: 容器在停止后会自动重启，除非手动停止。
- `ghcr.io/flaresolverr/flaresolverr:latest`: 使用 FlareSolverr 的最新 Docker 镜像。
- 您可以通过访问 `http://localhost:9117` 来查看 FlareSolverr 的 Web 界面

提示如下信息即安装成功

![配图](/upload/image-vfjy.png)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
