# linux远程桌面管理工具xrdp

> 标题：linux远程桌面管理工具xrdp
> 分类：Linux运维
> 标签：Linux、xrdp
> 原文：https://www.xinz.fun/archives/linuxyuan-cheng-zhuo-mian-guan-li-gong-ju-xrdp

> **导读**：这篇围绕「linux远程桌面管理工具xrdp」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾Linux运维的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 一、概述
2. 二、安装过程
3. 三、测试验证

## 一、概述

我们知道，我们日常通过vnc来远程管理linux图形界面，今天分享一工具Xrdp，它是一个开源工具，允许用户通过Windows RDP访问Linux远程桌面。除了Windows RDP之外，xrdp工具还接受来自其他RDP客户端的连接，如FreeRDP，rdesktop和NeutrinoRDP。

实验环境说明：

Linux操作系统：centos7.9
Windows客户端操作系统：win10
xrdp软件版本：xrdp-0.9.19-1.el7.x86\_64

## 二、安装过程

1、安装GNOME默认桌面环境

```
yum groupinstall "X Window System" -y
yum group install "GNOME" -y
```

2、安装Xrdp

```
yum install xrdp -y
```

3.启动Xrdp服务，并设置开机启动

```bash
systemctl enable xrdp --now
```

4.查看Xrdp的启动状态

```bash
systemctl status xrdp
```

输出如下显示成功

5、配置Xrdp

设置Xrdp使用GNONE，编辑配置文件，添加如下行

```bash
sudo vim /etc/xrdp/xrdp.ini
exec gnome-session
```

重启Xrdp服务

```bash
sudo systemctl restart xrdp
```

6、配置防火墙（如果启用了防火墙的话），放行3389端口

默认情况下，Xrdp监听3389端口，如果使用的是云服务器（如阿里云、华为云），可以通过安全组规则放行3389端口。

## 三、测试验证

1、使用windows自带的远程桌面客户端进行连接

2、输入用户名和密码等信息

3、登录成功

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
