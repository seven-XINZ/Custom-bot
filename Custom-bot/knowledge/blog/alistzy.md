# docker安装alist

> 标题：docker安装alist
> 分类：AList网盘
> 标签：alist
> 原文：https://www.xinz.fun/archives/alistzy

> **导读**：这篇是「docker安装alist」的实操教程。下文按「实际步骤」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾AList网盘的读者。执行前建议先备份原配置，并在测试环境验证。

```bash
docker run -d \
  --name ${CONTAINER_NAME} \
  --restart always \
  --cpus ${CPUS} \
  --memory ${MEMORY_LIMIT} \
  -e PUID=0 \
  -e PGID=0 \
  -e UMASK=022 \
  --network host \
  -v ./data/data:/opt/alist/data \
  -v /opt/1panel/apps/alist/下载:/下载 \
  xhofe/alist:v3.36.0
```

```bash
docker run -d \
  --name ${CONTAINER_NAME} \
  --restart always \
  --cpus ${CPUS} \
  --memory ${MEMORY_LIMIT} \
  -e PUID=0 \
  -e PGID=0 \
  -e UMASK=022 \
  -p ${HOST_IP}:${PANEL_APP_PORT_HTTP}:5244 \
  -v ./data/data:/opt/alist/data \
  -v /opt/1panel/apps/alist/下载:/下载 \
  --network 1panel-network \
  xhofe/alist:v3.36.0

# 参数说明
# --network host：指定使用主机网络模式。
# 由于使用了 host 网络模式，您不需要使用 -p 参数进行端口映射，因为容器将直接使用主机的网络接口
```

### 参数说明

- `-d`：以分离模式运行容器。
- `--name ${CONTAINER_NAME}`：为容器指定名称。
- `--restart always`：设置容器自动重启策略。
- `--cpus ${CPUS}`：限制容器使用的 CPU 数量。
- `--memory ${MEMORY_LIMIT}`：限制容器使用的内存。
- `-e PUID=0`：设置环境变量 `PUID`。
- `-e PGID=0`：设置环境变量 `PGID`。
- `-e UMASK=022`：设置环境变量 `UMASK`。
- `-p ${HOST_IP}:${PANEL_APP_PORT_HTTP}:5244`：映射主机端口到容器端口。
- `-v ./data/data:/opt/alist/data`：挂载数据卷。
- `-v /opt/1panel/apps/alist/下载:/下载`：挂载另一个数据卷。
- `--network 1panel-network`：指定容器连接到的网络。
- `xhofe/alist:v3.36.0`：使用的 Docker 镜像及其标签。

### 注意事项

- 确保在运行命令之前，已创建 `1panel-network` 网络，因为 `docker run` 不会自动创建外部网络。
- 在执行命令之前，确保环境变量 `${CONTAINER_NAME}`、`${CPUS}`、`${MEMORY_LIMIT}`、`${HOST_IP}` 和 `${PANEL_APP_PORT_HTTP}` 已正确设置。

通过这个 `docker run` 命令，您应该能够启动一个与您在 Docker Compose 中定义的 `alist` 服务相同的 Docker 容器。

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
