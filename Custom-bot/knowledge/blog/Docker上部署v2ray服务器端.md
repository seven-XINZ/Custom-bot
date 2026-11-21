# Docker上部署v2ray服务器端

> 标题：Docker上部署v2ray服务器端
> 分类：代理与穿透
> 标签：docker、Linux、v2ray、nas、群晖
> 原文：https://www.xinz.fun/archives/Docker上部署v2ray服务器端

> **导读**：这篇是「Docker上部署v2ray服务器端」的实操教程。下文按「实际步骤」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾代理与穿透的读者。执行前建议先备份原配置，并在测试环境验证。

一、在docker hub上拉取v2ray最新版镜像

```bash
docker pull v2ray/official:latest
```

二、创建配置
/root/docker/v2ray/config.json

```json
{
  "log" : {
	"access": "/var/log/v2ray/access.log",
	"error": "/var/log/v2ray/error.log",
	"loglevel": "warning"
  },
  "inbounds": [{
	"port": 8001,//端口
	"protocol": "vmess",//传输协议
	"settings": {
	  "clients": [
		{
		  "id": "466eb1fe-6943-4935-b893-9e8adb3c6b00",//这里GUID请通过工具生成
		  "level": 1,
		  "alterId": 64
		}
	  ]
	}
  }],
  "outbounds": [{
	"protocol": "freedom",
	"settings": {}
  }]
}
```

需要注意的是clients节点里的id需要自行生成并替换，[生成工具](http://www.ofmonkey.com/transfer/guid)
三、运行v2ray

```bash
docker run \
--restart=always \
--name=v2ray \
--net=host \
-v $PWD/docker/v2ray/config.json:/etc/v2ray/config.json \
-v $PWD/docker/v2ray/log/:/var/log/v2ray \
-i -t -d \
v2ray/official:latest
```

四、客户端使用

```
vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIuWuouaIt+err+mFjee9riIsDQogICJhZGQiOiAiMTI3LjAuMC4xIiwNCiAgInBvcnQiOiAiODAwMSIsDQogICJpZCI6ICI0NjZlYjFmZS02OTQzLTQ5MzUtYjg5My05ZThhZGIzYzZiMDAiLA0KICAiYWlkIjogIjY0IiwNCiAgInNjeSI6ICJhdXRvIiwNCiAgIm5ldCI6ICJ0Y3AiLA0KICAidHlwZSI6ICJub25lIiwNCiAgImhvc3QiOiAiIiwNCiAgInBhdGgiOiAiLyIsDQogICJ0bHMiOiAiIiwNCiAgInNuaSI6ICIiLA0KICAiYWxwbiI6ICIiDQp9
```

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
