# Docker部署qchatgpt(仅推荐在Linux上使用)

> 标题：Docker部署qchatgpt(仅推荐在Linux上使用)
> 分类：AI大模型
> 标签：docker
> 原文：https://www.xinz.fun/archives/qchatgpt

> **导读**：这篇是「Docker部署qchatgpt(仅推荐在Linux上使用)」的实操教程。下文按「实际步骤」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾AI大模型的读者。执行前建议先备份原配置，并在测试环境验证。

### 自用docker run参考

```bash
docker run -d \
  --name qchatgpt \
  --restart always \
  -v /opt/1panel/apps/QChatGPT/data:/app/data \
  -v /opt/1panel/apps/QChatGPT/plugins:/app/plugins \
  --network host \
  rockchin/qchatgpt:latest
```

### 参数说明

- `-d`：以分离模式运行容器。
- `--name qchatgpt`：为容器指定名称为 `qchatgpt`。
- `--restart always`：设置容器自动重启策略。
- `-v /opt/1panel/apps/QChatGPT/data:/app/data`：挂载主机目录到容器中的 `/app/data`。
- `-v /opt/1panel/apps/QChatGPT/plugins:/app/plugins`：挂载主机目录到容器中的 `/app/plugins`。
- `--network host`：使用主机网络模式，允许容器直接访问主机的网络接口。
- `rockchin/qchatgpt:latest`：使用的 Docker 镜像及其标签。

### 注意事项

- 在使用 `host` 网络模式时，请注意容器内的服务将直接暴露在主机的网络上，这可能会导致端口冲突，特别是当主机上已经有其他服务在使用相同端口时。
- 确保在运行命令之前，挂载的目录存在并具有适当的权限。
- 确保 Docker 已安装并正在运行。

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
