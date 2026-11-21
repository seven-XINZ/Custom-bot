# 群晖NAS安装frp内网穿透工具方法

> 标题：群晖NAS安装frp内网穿透工具方法
> 分类：代理与穿透
> 标签：nas、群晖、frp、内网穿透
> 原文：https://www.xinz.fun/archives/frp

> **导读**：这篇是「群晖NAS安装frp内网穿透工具方法」的实操教程。下文按「一、启动SSH功能」「二、下载frp工具」「下载地址：https://github.com/fatedier/frp/releases」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾代理与穿透的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 一、启动SSH功能
2. 二、下载frp工具
3. 下载地址：https://github.com/fatedier/frp/releases
4. （1）服务端配置
5. （2）客户端配置
6. 三、创建开机启动任务

> \*简介：本文介绍在群晖NAS上安装内网穿透工具frp的过程，及详细的配置和使用方法。

## 一、启动SSH功能

[![配图](https://qiniucdn.xinac.net/blog/image_1594783649869.png)](https://qiniucdn.xinac.net/blog/image_1594783649869.png)

## 二、下载frp工具

## 下载地址：https://github.com/fatedier/frp/releases

服务端版本：frp\_0.33.0\_linux\_amd64.tar.gz

客户端版本：frp\_0.33.0\_linux\_386.tar.gz

## （1）服务端配置

```bash
cd  /opt
tar -zxvf frp_0.33.0_linux_amd64.tar.gz
cd  frp_0.33.0_linux_amd64
vim frps.ini
```

```json
[common]
# 监听地址
bind_addr = 0.0.0.0
# TCP端口
bind_port        = 7010
# UDP端口，用于辅助客户端进行打洞穿透 NAT
bind_udp_port    = 7011
# KCP端口，KCP 协议的 UDP 端口，可与 TCP 端口相同
kcp_bind_port    = 7010
# 虚拟主机HTTP端口，可与通用设置的 TCP 端口相同
vhost_http_port  = 7010
# 虚拟主机HTTPS端口，可与通用设置的 TCP 端口相同
vhost_https_port = 7010
# 日志级别
log_level = warn
# 日志切割，按设定时间进行日志切割，单位：天
log_max_days = 3
# 验证密钥
token = 1234567890
# 最大连接池
max_pool_count = 5
# 最大端口数，限制每个客户端最多创建的端口数量，设置为 0 表示不限制
max_ports_per_client = 0
# 二级域名
subdomain_host = frp.xinac.com
# TCP多路复用
tcp_mux = true
# 端口白名单
allow_ports = 6000-50000
log_file = /var/log/frps.log
```

服务器端配置完成，以上内容需要在有公网IP的服务器上配置

## （2）客户端配置

```
# 切换到root用户
sudo -i
 
cd  /opt
tar -zxvf frp_0.33.0_linux_386.tar.gz
cd  frp_0.33.0_linux_386
vim frpc.ini
```

```json
[common]
server_addr = frp.xinac.com
server_port = 7010
privilege_token = 1234567890
token           = 1234567890
 
[nas_dsm]
type = http
local_ip        = 127.0.0.1
local_port      = 5000
subdomain       = dsm
 
[nas_web]
type = http
local_ip        = 127.0.0.1
local_port      = 80
subdomain       = web
```

```
# 创建启动脚本
vim start.sh
 
# 脚本内容
nohup /opt/frp_0.33.0_linux_386/frpc -c /opt/frp_0.33.0_linux_386/frpc.ini &
 
# 启动脚本
/opt/frp_0.33.0_linux_386/start.sh
 
# 可能需要修改权限
# chmod 755 /opt/frp_0.33.0_linux_386/start.sh
```

## 三、创建开机启动任务

1. 任务计划->新增->触发的任务->用户定义的脚本

![配图](https://qiniucdn.xinac.net/blog/image_1594785444263.png)

2. 创建开机任务

![配图](https://qiniucdn.xinac.net/blog/image_1594785587631.png)3.任务设置

用户定义的脚本内容：

```bash
cd /opt/frp_0.33.0_linux_386/ & bash /opt/frp_0.33.0_linux_386/start.sh
```

4. 查看运行结果

可以手动执行测试，执行后可查看运行结果。

![配图](https://qiniucdn.xinac.net/blog/image_1594785818911.png)![配图](https://qiniucdn.xinac.net/blog/image_1594785847089.png)**四、测试效果**

1. 启动服务端和客户端程序
2. 访问域名测试：[http://dsm.frp.xinac.com](https://www.xinac.com/go/?url=https://blog.xinac.cn/)
3. 如果不能访问，注意检查端口号、防火墙、日志、网络
4. 确认可正常访问后，关闭SSH服务

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
