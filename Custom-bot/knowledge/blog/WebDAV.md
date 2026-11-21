# 如何使用 Docker 化的 WebDAV 客户端

> 标题：如何使用 Docker 化的 WebDAV 客户端
> 分类：面板与工具
> 标签：docker、alist
> 原文：https://www.xinz.fun/archives/WebDAV

> **导读**：这篇是「如何使用 Docker 化的 WebDAV 客户端」的实操教程。下文按「前言:」「使用教程」「步骤 2：运行 Docker 容器」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾面板与工具的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 前言:
2. 使用教程
3. 步骤 2：运行 Docker 容器
4. 自动卸载
5. 不自动删除容器 并自动重启 按需修改

## 前言:

如何使用 Docker 化的 WebDAV 客户端的教程，帮助你将远程 WebDAV 资源挂载到容器中，并确保能够在主机上访问这些资源。

### 全文摘要

本文是一份关于如何使用 Docker 化的 WebDAV 客户端的详细教程，旨在指导用户将远程 WebDAV 资源挂载到 Docker 容器中，并确保在主机上能够访问这些资源。文章介绍了安装 Docker 的先决条件、创建挂载目录、运行 Docker 容器、参数说明、访问挂载资源以及自动卸载的步骤，并提供了一些注意事项。

### 关键段落

- **先决条件**: 确保系统已安装 Docker，拥有可用的 WebDAV URL、用户名和密码。
- **创建挂载目录**: 在主机上创建目录（如 /mnt/tmp）以挂载 WebDAV 资源。
- **运行 Docker 容器**: 使用具体命令和参数运行 Docker 容器，包括挂载 WebDAV 资源到指定目录。
- **参数说明**: 详细解释了运行命令中的每个参数，如设备权限、系统管理员权限、安全配置、环境变量等。
- **访问挂载的 WebDAV 资源**: 容器运行后，通过访问主机目录来使用 WebDAV 资源。
- **自动卸载**: 容器退出时自动卸载 WebDAV 资源，可执行其他命令。
- **注意事项**: 避免在容器运行期间手动更改或删除挂载目录中的文件，以防数据丢失。

## 使用教程

#### 先决条件

**安装 Docker**：确保你的系统上已经安装了 Docker。可以通过以下命令检查 Docker 是否安装成功：

```bash
docker --version
```

1. **远程 WebDAV 资源**：确保你有一个可用的 WebDAV URL、用户名和密码。

#### 步骤 1：创建挂载目录

在主机上创建一个目录，用于挂载 WebDAV 资源。这里我们使用 `/mnt/tmp` 作为示例：

```bash
mkdir -p /mnt/tmp
```

## 步骤 2：运行 Docker 容器

使用以下命令运行 Docker 容器，将远程 WebDAV 资源挂载到 `/mnt/tmp` 目录。请替换 `<YourUserName>` 和 `<SuperSecretPassword>` 以及 URL 为你的实际值。

```bash
docker run -it --rm \
    --device /dev/fuse \
    --cap-add SYS_ADMIN \
    --security-opt "apparmor=unconfined" \
    --env "WEBDRIVE_USERNAME=admin" \
    --env "WEBDRIVE_PASSWORD=password" \
    --env "WEBDRIVE_URL=http://172.17.0.1:5244/dav" \
    --env "DAVFS2_ASK_AUTH=0" \
    -v /opt/1panel/apps/webdav:/mnt/webdrive:rshared \
    efrecon/webdav-client
```

### 参数说明

**未注释的可以不改动**

- `--device /dev/fuse`：允许容器使用 FUSE（用户空间文件系统）。
- `--cap-add SYS_ADMIN`：添加系统管理员权限，允许容器进行挂载操作。
- `--security-opt "apparmor=unconfined"`：禁用 AppArmor 安全配置。
- `--env "WEBDRIVE_USERNAME=<YourUserName>"`：WebDAV 资源的用户名。 网盘用户名
- `--env "WEBDRIVE_PASSWORD=<SuperSecretPassword>"`：WebDAV 资源的密码。 网盘用户密码
- `--env "WEBDRIVE_URL=https://dav.box.com/dav"`：WebDAV 资源的 URL。 网盘地址url 默认docker网关模式
- `--env "DAVFS2_ASK_AUTH=0"`：禁止交互式身份验证。
- `-v /mnt/tmp:/mnt/webdrive:rshared`：将主机的 `/mnt/tmp` 目录挂载到容器的 `/mnt/webdrive` 目录。 可以不动

### 步骤 3：访问挂载的 WebDAV 资源

在容器运行后，你可以在主机的 `/mnt/tmp` 目录中访问挂载的 WebDAV 资源：

```
ls /mnt/tmp
```

## 自动卸载

容器在退出时会自动卸载 WebDAV 资源。如果你希望在容器内执行其他命令，可以使用 `empty.sh` 作为命令传递：

```bash
docker run -it --rm \ 
--device /dev/fuse \ 
--cap-add SYS_ADMIN \ 
--security-opt "apparmor=unconfined" \ 
--env "WEBDRIVE_USERNAME=<YourUserName>" \ 
--env "WEBDRIVE_PASSWORD=<SuperSecretPassword>" \ 
--env "WEBDRIVE_URL=https://dav.box.com/dav" \ 
--env "DAVFS2_ASK_AUTH=0" \ 
-v /mnt/tmp:/mnt/webdrive:rshared \ 
efrecon/webdav-client empty.sh
```

### 注意事项

- 确保在容器运行期间，不要手动更改或删除 `/mnt/tmp` 目录中的文件，以避免潜在的数据丢失。
- 如果你希望使用文件而不是环境变量来管理密码，可以使用 `WEBDRIVE_PASSWORD_FILE` 环境变量指向一个包含密码的文件。

### 结束

通过以上步骤，你可以成功将远程 WebDAV 资源挂载到 Docker 容器中，并在主机上访问这些资源。确保根据你的具体需求调整环境变量和挂载路径。

## 不自动删除容器 并自动重启 按需修改

### 设置 Docker 容器在系统启动时自启，你可以使用 Docker 的重启策略。下面是如何实现这一目标的步骤。

### 1. 修改 Docker 命令以设置重启策略

将你的 `docker run` 命令修改为使用 `--restart` 选项。以下是一个示例，使用 `unless-stopped` 策略：

```bash
docker run -d \
--restart unless-stopped \
--device /dev/fuse \
--cap-add SYS_ADMIN \
--security-opt "apparmor=unconfined" \
--env "WEBDRIVE_USERNAME=admin" \
--env "WEBDRIVE_PASSWORD=password" \
--env "WEBDRIVE_URL=http://192.168.0.0:5244/dav" \
--env "DAVFS2_ASK_AUTH=0" \
-v /opt/1panel/webdav:/mnt/webdrive:rshared \
efrecon/webdav-client
```

### 2. 启动 Docker 服务

确保 Docker 服务在系统启动时自动启动。你可以使用以下命令检查 Docker 服务的状态：

```bash
sudo systemctl status docker
```

如果 Docker 服务未设置为开机自启，可以使用以下命令启用它：

```bash
sudo systemctl enable docker
```

### 3. 启动容器

使用修改后的命令启动容器。由于使用了 `-d` 选项，容器将以后台模式运行。

### 4. 验证容器状态

你可以使用以下命令检查容器的状态，确保它在运行：

```bash
docker ps -a
```

### 5. 容器重启策略选项

`--restart` 选项的可用值包括：

- `no`: 默认值，容器不会自动重启。
- `always`: 无论容器退出的原因如何，Docker 都会始终重启容器。
- `unless-stopped`: 只有在容器被手动停止时，Docker 才不会重启容器。
- `on-failure`: 只在容器因错误退出时重启，可以指定最大重启次数。

### 6. 其他注意事项

- 确保你的 Docker 守护进程正常运行，并且你有足够的权限执行 Docker 命令。
- 如果需要查看容器的输出日志，可以使用以下命令：

```bash
docker logs <container_id>
```

`docker logs <container_id>`

将 `<container_id>` 替换为实际的容器 ID。

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
