# 如何使用Docker搭建NginxWebUI

> 标题：如何使用Docker搭建NginxWebUI
> 分类：反代与网络
> 标签：docker
> 原文：https://www.xinz.fun/archives/如何使用Docker搭建NginxWebUI

> **导读**：这篇是「如何使用Docker搭建NginxWebUI」的实操教程。下文按「实际步骤」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾反代与网络的读者。执行前建议先备份原配置，并在测试环境验证。

### 介绍：NginxWebUI是一款用于配置Nginx负载均衡和反向代理可视化管理工具。你可以使用这个工具来轻松管理和配置Nginx，以及查看Nginx的运行状态和日志。
#### 第一步：更新源

对于Ubuntu/Debian：

bash

```bash
01sudo apt-get update -y && sudo apt-get upgrade -y
```

对于CentOS：

bash

```bash
01sudo yum update -y && sudo yum upgrade -y
```

#### 第二步：安装并配置Docker

安装Docker：

bash

```bash
01curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh ./get-docker.sh
```

启动Docker：

bash

```bash
01sudo systemctl start docker
```

设置Docker在开机时自动启动：

bash

```bash
01sudo systemctl enable docker
```

#### 第三步：拉取 NginxWebUI 的 Docker 镜像

可以从 Docker Hub或者阿里云镜像库中拉取 NginxWebUI 的 Docker 镜像。选择以下命令中的其中一个来运行：

bash

```
01docker pull cym1102/nginxwebui:latest
```

或

bash

```
01docker pull registry.cn-hangzhou.aliyuncs.com/cym19871102/nginxwebui:latest
```

#### 第四步：运行 NginxWebUI 的 Docker 镜像

创建并启动一个 NginxWebUI 的 Docker 容器，使用以下指令：

bash

```
010203040506docker run -itd \
  -v /home/nginxWebUI:/home/nginxWebUI \
  -e BOOT_OPTIONS="--server.port=8080" \
  --privileged=true \
  --net=host \
  cym1102/nginxwebui:latest
```

请注意，需要使用 `--net=host` 参数来映射本机所有端口，因为内部的Nginx可能使用任意一个端口。

同时，需要映射 `/home/nginxWebUI:/home/nginxWebUI` 目录，此目录下存放项目所有数据文件，包括数据库、Nginx配置文件、日志、证书等，升级镜像时，此目录可以保证项目数据不丢失。请注意备份。

可以在`-e BOOT_OPTIONS` 参数可以填充Java启动参数，通过这个参数来修改端口号。`--server.port` 是占用的端口，如果不填写，那么默认以8080端口启动。

日志默认存放在 `/home/nginxWebUI/log/nginxWebUI.log`。

当然也可以使用 docker-compose 来启动 NginxWebUI，配置文件如下：

bash

```yaml
010203040506070809101112version: "3.2"
services:
  nginxWebUi-server:
    image: cym1102/nginxwebui:latest
    volumes:
      - type: bind
        source: "/home/nginxWebUI"
        target: "/home/nginxWebUI"
    environment:
      BOOT_OPTIONS: "--server.port=8080"
    privileged: true
    network_mode: "host"
```

#### 第五步：登录网站进行配置

在浏览器中访问 `IP:8080`，当第一次打开这个地址时，会被要求初始化管理员账号。

![配图](https://pic.imgdb.cn/item/64c924731ddac507cc9b9eed.jpg)

在http参数配置中可以配置nginx的http项目,进行http转发。

![配图](https://pic.imgdb.cn/item/64c92c301ddac507ccab4855.jpg)

在TCP参数配置中配置nginx的stream项目参数。

![配图](https://pic.imgdb.cn/item/64c92d931ddac507ccafb27f.jpg)

在反向代理中配置nginx的反向代理即server项功能, 可开启ssl功能, 也可以直接从网页上上传pem文件和key文件, 或者使用系统内申请的证书, 可以直接开启http转跳https功能，也可开启http2协议

![配图](https://pic.imgdb.cn/item/64c92db51ddac507ccaff7f2.jpg)

在负载均衡中可配置nginx的负载均衡即upstream项功能, 在反向代理管理中可选择代理目标为配置好的负载均衡

![配图](https://pic.imgdb.cn/item/64c92de01ddac507ccb0500e.jpg)

在html静态文件上传中可直接上传html压缩包到指定路径,上传后可直接在反向代理中使用,省去在Linux中上传html文件的步骤

![配图](https://pic.imgdb.cn/item/64c92dea1ddac507ccb068a0.jpg)

在证书管理中可添加证书, 并进行签发和续签, 开启定时续签后, 系统会自动续签即将过期的证书, **注意**:[证书的签发是用的acme.sh](http://证书的签发是用的acme.sh)的dns模式, 需要配合阿里云的aliKey和aliSecret来使用. 请先申请好aliKey和aliSecret

![配图](https://pic.imgdb.cn/item/64c92e0d1ddac507ccb0b71a.jpg)

备份文件管理, 这里可以看到nginx.cnf的备份历史版本, nginx出现错误时可以选择回滚到某一个历史版本

![配图](https://pic.imgdb.cn/item/64c92e271ddac507ccb0ec16.jpg)

最终生成conf文件,可在此进行进一步手动修改,确认修改无误后,可覆盖本机conf文件,并进行效验和重启, 可以选择生成单一nginx.conf文件还是按域名将各个配置文件分开放在conf.d下

![配图](https://pic.imgdb.cn/item/64c92e3c1ddac507ccb11a2c.jpg)

支持远程服务器管理, 如果有多台nginx服务器, 可以都部署上nginxWebUI, 然后登录其中一台, 在远程管理中添加其他服务器的ip和用户名密码, 就可以在一台机器上管理所有的nginx服务器了. 提供一键同步功能, 可以将某一台服务器的数据配置和证书文件同步到其他服务器中

![配图](https://pic.imgdb.cn/item/64c92e541ddac507ccb150b9.jpg)

如果需要通过API调用NginxWebUI的功能，可以访问 `IP:8080/doc.html` 来查看smart-doc接口页面。

如果忘记了登录密码或没有保存两步验证二维码，可以按照以下步骤来重置密码和关闭两步验证。

1. 停止nginxWebUI进程或停止docker容器运行
2. 使用找回密码参数运行nginxWebUI.jar，需单独下载nginxWebUI.jar运行此命令

bash

```
01java -jar nginxWebUI.jar --project.home=/home/nginxWebUI/ --project.findPass=true
```

`--project.home` 是项目文件所在的目录，使用docker容器时为映射目录。

`--project.findPass` 是是否打印用户名密码。

运行成功后即可重置并打印出全部用户名密码并关闭两步验证.

如果觉得文章对你有用，请随意赞赏

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
