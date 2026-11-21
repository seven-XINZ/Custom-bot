# Docker安装v2ray

> 标题：Docker安装v2ray
> 分类：代理与穿透
> 标签：docker、Linux
> 原文：https://www.xinz.fun/archives/v2ray

> **导读**：这篇是「Docker安装v2ray」的实操教程。下文按「实际步骤」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾代理与穿透的读者。执行前建议先备份原配置，并在测试环境验证。

### 自用docerk run 参考

```bash
docker run -d \
  --restart=always \
  --privileged \
  --network=host \
  --name v2raya \
  -e V2RAYA_ADDRESS=0.0.0.0:2017 \
  -e V2RAYA_LOG_FILE=/tmp/v2raya.log \
  -e V2RAYA_V2RAY_BIN=/usr/local/bin/v2ray \
  -v /lib/modules:/lib/modules \
  -v /etc/resolv.conf:/etc/resolv.conf \
  -v /opt/1panel/apps/v2ray:/etc/v2raya \
  mzz2017/v2raya
```

![配图](/upload/image-kjwh.png)

### 参数说明

- `-d`：以分离模式运行容器，使其在后台运行。
- `--restart=always`：设置容器在停止时自动重启。
- `--privileged`：给予容器额外的权限，允许访问主机的设备和内核功能。
- `--network=host`：使用主机网络模式，容器将直接使用主机的网络接口。
- `--name v2raya`：为容器指定名称为 `v2raya`。
- `-e V2RAYA_ADDRESS=0.0.0.0:2017`：设置环境变量 `V2RAYA_ADDRESS`，指定 V2Raya 监听的地址和端口。
- `-e V2RAYA_LOG_FILE=/tmp/v2raya.log`：设置环境变量 `V2RAYA_LOG_FILE`，指定日志文件的路径。
- `-e V2RAYA_V2RAY_BIN=/usr/local/bin/v2ray`：设置环境变量 `V2RAYA_V2RAY_BIN`，指定 V2Ray 可执行文件的路径。
- `-v /lib/modules:/lib/modules`：将主机的 `/lib/modules` 目录挂载到容器中，通常用于加载内核模块。
- `-v /etc/resolv.conf:/etc/resolv.conf`：将主机的 DNS 配置文件挂载到容器中，以确保容器使用主机的 DNS 设置。
- `-v /opt/1panel/apps/v2ray:/etc/v2raya`：将主机的 `/opt/1panel/apps/v2ray` 目录挂载到容器的 `/etc/v2raya`，用于配置文件和数据。
- `mzz2017/v2raya`：指定要使用的 Docker 镜像。

### 注意事项

- 确保 Docker 已安装并正在运行。
- 在使用 `--privileged` 和 `--network=host` 时，请了解这些设置可能带来的安全风险。
- 确保在运行命令之前，挂载的目录和文件存在并具有适当的权限。

通过这个命令，您可以启动 `v2raya` 服务，它将监听所有 IP 地址的 2017 端口，并能够访问主机的网络和资源。

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
