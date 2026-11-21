# 搭建tg人形机器人

> 标题：搭建tg人形机器人
> 分类：机器人Bot
> 标签：docker、Linux、nas、群晖
> 原文：https://www.xinz.fun/archives/da-jian-tgren-xing-ji-qi-ren

> **导读**：这篇是「搭建tg人形机器人」的实操教程。下文按「实际步骤」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾机器人Bot的读者。执行前建议先备份原配置，并在测试环境验证。

获取tgID-tgHASH
[https://my.telegram.org/apps
拉取PagerMaid一键docker脚本](https://my.telegram.org/apps)

```bash
mkdir docker && cd /root/docker && mkdir PagerMaid && cd /root/docker/PagerMaid && wget https://gitlab.com/Xtao-Labs/pagermaid-modify/-/raw/master/utils/docker.sh -O docker.sh&& chmod +x docker.sh && bash docker.sh
```

配置完成后执行脚本将 PagerMaid 数据持久化
后期手动更新

```bash
docker pull mrwangzhe/pagermaid_modify

docker run \
-d --name=PagerMaid \
-v "$PWD/docker/PagerMaid/workdir/:/pagermaid/workdir" \
-p "3333:3333" \
--restart=always \
mrwangzhe/pagermaid_modify
```

拉取PagerMaidpro一键docker脚本

```bash
wget https://ghproxy.com/https://raw.githubusercontent.com/TeamPGM/PagerMaid-Pyro/development/utils/docker.sh -O docker.sh && chmod +x docker.sh && bash docker.sh
```

配置完成后执行脚本将 PagerMaid 数据持久化
后期手动更新

```bash
docker pull teampgm/pagermaid_pyro

docker run -dit \
-v "$PWD/docker/PagerMaid/workdir/:/pagermaid/workdir" \
--restart=always \
--name=pagermaid_pyro \
--hostname=pagermaid_pyro \
-e WEB_ENABLE=true \
-e WEB_SECRET_KEY=你的密码 \
-e WEB_HOST=0.0.0.0 \
-e WEB_PORT=3333 \
-p 3333:3333 \
teampgm/pagermaid_pyro
```

关于人形的插件
1.官方插件
[https://gitlab.com/Xtao-Labs/PagerMaid\_Plugins
2.命令安装](https://gitlab.com/Xtao-Labs/PagerMaid_Plugins)

```
#安装插件
-apt install 插件名
#禁用插件
-apt disabled 插件名
#卸载插件
-apt remove 插件名
#更新插件
-update 插件名
#重启人形bot
-restart
```

可对接傻妞 人型傻妞安装步骤
1.安装PagerMaid插件 -apt install silly\_girl
2.启用插件，首次设置需地址参数 -sillyGirl [http://傻妞地址:端口
3.设置用户或群组白名单，set](http://abc@127.0.0.1:8080/) pgm whiltelist id1&id2&id3… 每次设置后都要 -sillyGirl
如提示token安全验证设置下面的
傻妞：
set pgm token abc，
PagerMaid：
-sillyGirl [http://abc@127.0.0.1:8080](http://abc@127.0.0.1:8080/)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
