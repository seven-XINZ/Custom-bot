# QQ签名服务器搭建

> 标题：QQ签名服务器搭建
> 分类：机器人Bot
> 标签：docker、Linux、nas、QQ
> 原文：https://www.xinz.fun/archives/QQ签名服务器搭建

> **导读**：这篇是「QQ签名服务器搭建」的实操教程。下文按「实际步骤」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾机器人Bot的读者。执行前建议先备份原配置，并在测试环境验证。

必须加ANDROID\_ID了！这东西在你的device.json里！找出来替换掉{android\_id}
不然直接退出的！跑了白跑！
运行命令之后，用docker container ls -a查看一下你的容器是否跑起来，没跑起来的（状态是Exited (1)）用docker container logs qsign看一下是不是没填android\_id！

```bash
 docker run -d \
    --restart=always \
    --name qsign \
    -p 8081:8080 \
    -e ANDROID_ID={android_id} \
    -e BASE_PATH=/srv/qsign/qsign/txlib/{version} \
    -v $PWD/docker/qsign/config.json:/srv/qsign/qsign/txlib/{version}/config.json \
    xzhouqd/qsign:core-{core-ver}
```

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
