# v2ray 个人docker

> 标题：v2ray 个人docker
> 分类：代理与穿透
> 标签：v2ray、nas、群晖
> 原文：https://www.xinz.fun/archives/v2ray-ge-ren-docker

> **导读**：这篇围绕「v2ray 个人docker」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾代理与穿透的读者。执行前建议先备份原配置，并在测试环境验证。

docker -v2ray

```bash
sudo docker run -d \
  --restart=always \
  --privileged \
  --network=host \
  --name v2raya \
  -e V2RAYA_LOG_FILE=/etc/docker/v2ray/v2raya.log \
  -e V2RAYA_V2RAY_BIN=/usr/local/bin/v2ray \
  -v /lib/modules:/lib/modules:ro \
  -v /etc/resolv.conf:/etc/resolv.conf \
  mzz2017/v2raya
```

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
