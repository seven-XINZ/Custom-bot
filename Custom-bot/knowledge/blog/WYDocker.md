# 认识Docker了解Docker深入Docker

> 标题：认识Docker了解Docker深入Docker
> 分类：Docker容器
> 标签：docker
> 原文：https://www.xinz.fun/archives/WYDocker

> **导读**：这篇围绕「认识Docker了解Docker深入Docker」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾Docker容器的读者。执行前建议先备份原配置，并在测试环境验证。

### Docker 业余笔记
#### 什么是Docker？

Docker是一个开源的容器化平台，可以让开发者打包自己的应用程序及其所有依赖项成为一个独立的容器，从而实现应用程序的快速部署、可移植性和可伸缩性。

#### 为什么要使用Docker？

- **轻量级：** Docker容器与宿主机共享操作系统内核，因此比虚拟机更轻量级。
- **快速部署：** Docker容器可以在几秒钟内启动，比传统的虚拟机启动更快。
- **环境一致性：** Docker容器可以确保应用程序在不同环境中的一致性，避免了“在我机器上可以运行”的问题。
- **资源隔离：** Docker容器提供了资源隔离，可以避免不同应用程序之间的相互影响。

#### Docker基本概念

- **镜像（Image）：** Docker镜像是一个只读的模板，可以用来创建Docker容器。
- **容器（Container）：** Docker容器是一个独立运行的应用程序，包含了应用程序和其所有依赖项。
- **仓库（Repository）：** Docker仓库用于存储Docker镜像，可以是公共的或私有的。
- **Dockerfile：** Dockerfile是一个文本文件，包含了用于自动构建Docker镜像的指令。

#### Docker使用示例

1. **安装Docker：** 使用适合您操作系统的安装方式，安装Docker引擎。
2. **拉取镜像：** 使用`docker pull`命令从仓库中拉取镜像，例如`docker pull ubuntu:latest`。
3. **运行容器：** 使用`docker run`命令来创建并运行容器，例如`docker run -it ubuntu:latest /bin/bash`。
4. **构建镜像：** 编写Dockerfile文件，然后使用`docker build`命令构建镜像，例如`docker build -t myapp .`。
5. **上传镜像：** 使用`docker push`命令将构建好的镜像上传到仓库，例如`docker push username/myapp`.

#### Docker常用命令

- `docker ps`：列出正在运行的容器。
- `docker images`：列出本地所有的镜像。
- `docker start/stop/restart`：启动/停止/重启容器。
- `docker exec`：在运行中的容器中执行命令。
- `docker rm`：删除一个或多个容器。
- `docker rmi`：删除一个或多个镜像。

#### 总结

Docker是一个强大而灵活的容器化平台，可以大大简化应用程序的开发、部署和管理过程。通过学习和使用Docker，我们可以更高效地构建和交付应用程序，提高开发和运维的效率。

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
