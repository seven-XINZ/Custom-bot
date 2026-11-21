# Docker 安装 alist

> 标题：Docker 安装 alist
> 分类：AList网盘
> 标签：docker、Linux、nas、群晖、alist、alist美化
> 原文：https://www.xinz.fun/archives/docker-an-zhuang-alist

> **导读**：这篇是「Docker 安装 alist」的实操教程。下文按「初始密码请查看日志输出：」「稳定版」「开发版」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾AList网盘的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 初始密码请查看日志输出：
2. 稳定版
3. 开发版
4. alist带aria2离线下载

## 初始密码请查看日志输出：

```bash
docker logs alist
# 或者
docker exec -it alist ./alist -password
```

## 稳定版

```bash
docker run -d \
	--restart=always \
	-v $PWD/docker/alist:/opt/alist/data \
	-v $PWD/docker/alist/data:/root/ \
	-v /mnt/:/mnt/ \
	-v $PWD/docker/nasdownloads:/root/nas同步 \
	-p 5244:5244 \
	--name="alist" \
	xhofe/alist:latest
```

## 开发版

```bash
docker run -d --restart=always -v /etc/alist:/opt/alist/data -p 5244:5244 --name="alist" xhofe/alist:v2
```

## alist带aria2离线下载

```bash
	docker run -d \
	--restart=always \
	-v $PWD/docker/alist:/opt/alist/data \
	-p 5244:5244 \
	-e PUID=0 \
	-e PGID=0 \
	-e UMASK=022 \
	--name="alist" \
	xhofe/alist-aria2:latest
```

查看账号密码

```bash
docker exec -it alist ./alist admin
```

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
