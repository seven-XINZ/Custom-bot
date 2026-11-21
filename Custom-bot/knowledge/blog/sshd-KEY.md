# 如何修复“sshd 错误：无法加载主机密钥”

> 标题：如何修复“sshd 错误：无法加载主机密钥”
> 分类：Linux运维
> 标签：ubuntu
> 原文：https://www.xinz.fun/archives/sshd-KEY

> **导读**：这篇记录「如何修复“sshd 错误：无法加载主机密钥”」的排查与处理过程。先说明问题现象，再给出配置或命令，最后补充验证方法；遇到相似报错时可按顺序对照。
>
> 适合正在折腾Linux运维的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. SSH 问题描述
2. 如何解决SSH登录错误
3. debian打开root登陆
4. To disable tunneled clear text passwords, change to no here!
5. Debian 软件源

---

> **问题：**当我尝试通过 SSH 连接到远程服务器时，SSH 客户端失败，并显示`连接被 X.X.X.X 关闭`。在 SSH 服务器端，我看到错误消息：`sshd error: Could not load host key`。这是怎么回事，如何修复此错误？
>
> ![配图](/upload/image-cmvc.png)

## SSH 问题描述

此 SSH 连接错误的详细症状如下。

在SSH客户端，您已为远程SSH服务器启用密钥身份验证。但是，当您尝试连接到 SSH 服务器时，您看不到登录屏幕，并且 SSH 连接会立即关闭，并显示以下消息：

```
Connection closed by XXXX
```

```
Connection reset by XXXX
```

在SSH服务器端，系统日志有以下错误信息：

在 Ubuntu、Debian 或 Linux Mint 上的 `/var/log/auth.log` 中：

```
Oct 16 08:59:45 openstack sshd[1214]: error: Could not load host key: /etc/ssh/ssh_host_rsa_key
Oct 16 08:59:45 openstack sshd[1214]: error: Could not load host key: /etc/ssh/ssh_host_dsa_key
Oct 16 08:59:45 openstack sshd[1214]: error: Could not load host key: /etc/ssh/ssh_host_ecdsa_key
Oct 16 08:59:45 openstack sshd[1214]: fatal: No supported key exchange algorithms [preauth]
```

在 CentOS、Fedora 或 RHEL 上的 `/var/log/secure` 中：

```
Feb 18 21:48:25 localhost sshd[14226]: fatal: No supported key exchange algorithms [preauth]
```

## 如何解决SSH登录错误

此问题的根本原因是 `sshd` 守护进程无法正确加载 SSH 主机密钥。

当首次在 Linux 系统上安装 OpenSSH 服务器时，应自动生成 SSH 主机密钥以供后续使用。但是，如果密钥生成未成功完成，则可能会导致类似这样的 SSH 登录问题。

让我们检查一下是否在应有的位置找到了 SSH 主机密钥。

```
$ ls -al /etc/ssh/ssh*key
```

![配图](https://cn.linux-console.net/common-images/sshd-error-could-not-load-host-key.html/151a.png)

如果在那里找不到 SSH 主机密钥，或者它们的大小全部截断为零（如上所示），则需要从头开始重新生成 SSH 主机密钥。

### 以发行版特定的方式重新生成 SSH 主机密钥

在 Ubuntu、Debian 或其衍生版本上，您可以使用 dpkg-reconfigure 工具重新生成 SSH 主机密钥，如下所示。

```bash
$ sudo rm -r /etc/ssh/ssh*key
$ sudo dpkg-reconfigure openssh-server
```

![配图](https://cn.linux-console.net/common-images/sshd-error-could-not-load-host-key.html/151b.png)

在 CentOS、RHEL 或 Fedora 上，您所要做的就是在删除现有（有问题的）密钥后重新启动 sshd。

```bash
$ sudo rm -r /etc/ssh/ssh*key
$ sudo systemctl restart sshd
```

### 使用 ssh-keygen 重新生成 SSH 主机密钥

重新生成 SSH 主机密钥的另一种方法是使用 ssh-keygen 命令手动生成它们，如下所示。

```bash
$ sudo ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key
$ sudo ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key
$ sudo ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
```

![配图](https://cn.linux-console.net/common-images/sshd-error-could-not-load-host-key.html/151c.png)

生成新的 SSH 主机密钥后，请确保在 `/etc/ssh` 目录中找到它们。此时无需重新启动 sshd。

```
$ ls -al /etc/ssh/ssh*key
```

现在再次尝试通过 SSH 连接到 SSH 服务器，看看问题是否消失。

原地址:[debian (linux-console.net)](https://cn.linux-console.net/?dist=debiant)

## debian打开root登陆

![配图](/upload/U$O(%60IL%5BM)%60ES0%25%5DDXGV%5D_Q.png)

#LoginGraceTime 2m

#PermitRootLogin prohibit-password

PermitRootLogin yes

#StrictModes yes

#MaxAuthTries 6

#MaxSessions 10

原文中没有PermitRootLogin yes 则加到#PermitRootLogin prohibit-password下一行

## To disable tunneled clear text passwords, change to no here!

#PasswordAuthentication yes

#PermitEmptyPasswords no

这里的#PasswordAuthentication yes不用动保持默认就好

这里表示是否允许使用密码登陆。当这两行都被注释掉时，SSH 服务器默认允许 使用密码进行认证，但不允许使用空密码进行登，取消yes这行注释表示明确允许密码登陆。取消no这行注释表示明确禁止密码登陆。

## Debian 软件源

大部分 Debian 的软件源配置文件使用传统的 One-Line-Style，路径为 `/etc/apt/sources.list`；但是对于容器镜像，从 Debian 12 开始，其软件源配置文件变更为 DEB822 格式，路径为 `/etc/apt/sources.list.d/debian.sources`。一般情况下，将对应文件中 Debian 默认的源地址 `http://deb.debian.org/` 替换为镜像地址即可。

Debian Buster 以上版本默认支持 HTTPS 源。如果遇到无法拉取 HTTPS 源的情况，请先使用 HTTP 源并安装：

```bash
apt install apt-transport-https ca-certificates
```

### **传统格式（**`/etc/apt/sources.list`）

```bash
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware

deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware

deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware

# 以下安全更新软件源包含了官方源与镜像站配置，如有需要可自行修改注释切换
deb https://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
# deb-src https://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
```

### **DEB822 格式（**`/etc/apt/sources.list.d/debian.sources`

```
Types: deb
URIs: https://mirrors.tuna.tsinghua.edu.cn/debian
Suites: bookworm bookworm-updates bookworm-backports
Components: main contrib non-free non-free-firmware
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg

# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
# Types: deb-src
# URIs: https://mirrors.tuna.tsinghua.edu.cn/debian
# Suites: bookworm bookworm-updates bookworm-backports
# Components: main contrib non-free non-free-firmware
# Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg

# 以下安全更新软件源包含了官方源与镜像站配置，如有需要可自行修改注释切换
Types: deb
URIs: https://security.debian.org/debian-security
Suites: bookworm-security
Components: main contrib non-free non-free-firmware
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg

# Types: deb-src
# URIs: https://security.debian.org/debian-security
# Suites: bookworm-security
# Components: main contrib non-free non-free-firmware
# Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
```

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
