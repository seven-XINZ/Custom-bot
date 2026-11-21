# Docker安装qb下载容器

> 标题：Docker安装qb下载容器
> 分类：影音媒体
> 标签：docker
> 原文：https://www.xinz.fun/archives/qb

> **导读**：这篇是「Docker安装qb下载容器」的实操教程。下文按「实际步骤」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾影音媒体的读者。执行前建议先备份原配置，并在测试环境验证。

### 自用命令参考

```bash
docker run -d \
  --name ${CONTAINER_NAME} \
  --restart always \
  --cpus ${CPUS} \
  --memory ${MEMORY_LIMIT} \
  -e PUID=1000 \
  -e PGID=1000 \
  -e UMASK_SET=022 \
  -e TZ=${TIME_ZONE} \
  -e WEBUI_PORT=${PANEL_APP_PORT_HTTP} \
  -e TORRENTING_PORT=${PANEL_TORRENTING_PORT} \
  -p ${HOST_IP}:${PANEL_TORRENTING_PORT}:${PANEL_TORRENTING_PORT} \
  -p ${HOST_IP}:${PANEL_TORRENTING_PORT}:${PANEL_TORRENTING_PORT}/udp \
  -p ${HOST_IP}:${PANEL_APP_PORT_HTTP}:${PANEL_APP_PORT_HTTP} \
  -v /opt/1panel/apps/qb:/config \
  -v /opt/1panel/apps/qb:/downloads \
  --network 1panel-network \
  linuxserver/qbittorrent:4.6.5
```

### 参数说明

- `-d`：以分离模式运行容器。
- `--name ${CONTAINER_NAME}`：为容器指定名称。
- `--restart always`：设置容器自动重启策略。
- `--cpus ${CPUS}`：限制容器使用的 CPU 数量。
- `--memory ${MEMORY_LIMIT}`：限制容器使用的内存。
- `-e PUID=1000`：设置环境变量 `PUID`。
- `-e PGID=1000`：设置环境变量 `PGID`。
- `-e UMASK_SET=022`：设置环境变量 `UMASK_SET`。
- `-e TZ=${TIME_ZONE}`：设置时区环境变量。
- `-e WEBUI_PORT=${PANEL_APP_PORT_HTTP}`：设置 Web UI 端口。
- `-e TORRENTING_PORT=${PANEL_TORRENTING_PORT}`：设置 torrenting 端口。
- `-p ${HOST_IP}:${PANEL_TORRENTING_PORT}:${PANEL_TORRENTING_PORT}`：映射 torrenting 端口。
- `-p ${HOST_IP}:${PANEL_TORRENTING_PORT}:${PANEL_TORRENTING_PORT}/udp`：映射 torrenting UDP 端口。
- `-p ${HOST_IP}:${PANEL_APP_PORT_HTTP}:${PANEL_APP_PORT_HTTP}`：映射 Web UI 端口。
- `-v /opt/1panel/apps/qb:/config`：挂载配置目录。
- `-v /opt/1panel/apps/qb:/downloads`：挂载下载目录。
- `--network 1panel-network`：指定容器连接到的网络。
- `linuxserver/qbittorrent:4.6.5`：使用的 Docker 镜像及其标签。

### 注意事项

- 确保在运行命令之前，已创建 `1panel-network` 网络，因为 `docker run` 不会自动创建外部网络。
- 确保环境变量 `${CONTAINER_NAME}`、`${CPUS}`、`${MEMORY_LIMIT}`、`${TIME_ZONE}`、`${HOST_IP}`、`${PANEL_APP_PORT_HTTP}` 和 `${PANEL_TORRENTING_PORT}` 已正确设置。
- 在执行命令之前，确保挂载的目录存在并具有适当的权限。

通过这个 `docker run` 命令，您应该能够启动与您在 Docker Compose 中定义的 `qbittorrent` 服务相同的 Docker 容器

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
