# docker搭建ddnsgo

> 标题：docker搭建ddnsgo
> 分类：代理与穿透
> 标签：docker、Linux、nas、群晖
> 原文：https://www.xinz.fun/archives/dockerda-jian-ddnsgo

> **导读**：这篇是「docker搭建ddnsgo」的实操教程。下文按「实际步骤」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾代理与穿透的读者。执行前建议先备份原配置，并在测试环境验证。

```bash
docker run -d \
--name ddns-go \
--restart=always \
--net=host \
-v $PWD/docker/ddns-go:/root \
jeessy/ddns-go
```

设置名称服务器
[ns1.alidns.com](http://ns1.alidns.com)
[ns2.alidns.com](http://ns2.alidns.com)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
