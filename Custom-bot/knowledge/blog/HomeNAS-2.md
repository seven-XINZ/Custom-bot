# 基于Ubuntu搭建HomeNAS 续章

> 标题：基于Ubuntu搭建HomeNAS 续章
> 分类：Linux运维
> 标签：docker、Linux、v2ray、nas、群晖
> 原文：https://www.xinz.fun/archives/HomeNAS-2

> **导读**：这篇是「基于Ubuntu搭建HomeNAS 续章」的实操教程。下文按「基于Ubuntu搭建HomeNAS（五、安全防护）」「切换到pam.d目录，备份远文件」「使用vi编辑器编辑sshd文件」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾Linux运维的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 基于Ubuntu搭建HomeNAS（五、安全防护）
2. 切换到pam.d目录，备份远文件
3. 使用vi编辑器编辑sshd文件
4. 添加pam\_access模块
5. 切换到配置文件目录，备份原文件
6. 编辑配置文件
7. 在文件最后添加一行,只允许用户kim通过192.168.0.90地址登录
8. 基于Ubuntu搭建HomeNAS（六、存储管理）
9. 基于Ubuntu搭建HomeNAS（七、Docker服务）

## 基于Ubuntu搭建HomeNAS（五、安全防护）

安全的概念：

1、收紧安全措施有可能达到使系统无法使用的程度。安全性与便利性需要得到平衡。诀窍在于建立一个安全且有用的系统。

2、最大的威胁是（并且一直都会是）用户。

3、最小权限原则：系统的每一部分应该只能访问到它确实需要的东西，除此之外的则不可以。

4、纵深防御：多个独立的层次能带来更好的安全性。当一层防护被攻破时，另一层应该能够阻止攻击。

5、保持一点点的偏执和多疑。如果有件事看起来太好了，不像是真的，那可能确实如此。

6、永远无法令系统 100% 安全，除非把机器从网络上断开，关掉电源，锁进保险柜，用混凝土封住并不再使用它。

7、为失败做好准备。预先为安全措施被攻破的情况制定可供执行的计划。

本章节主要内容参考自Debian安全指南和Arch Linux安全。

Debian安全指南：<https://www.debian.org/doc/manuals/securing-debian-manual/ch04s11.zh-cn.html>

Arch Linux安全：<https://wiki.archlinuxcn.org/wiki/%E5%AE%89%E5%85%A8>

执行下列操作前，先给系统用户做个检查。检查是否存在空口令和root权限的账号，确认是否存在异常账号，确认UID为零的账号只有root账号。

操作步骤：

查看root权限账号，使用命令：

```
awk -F: '($3==0)' /etc/passwd                            //查看UID为零的账号。
```

查看空口令账号，使用命令：

```
awk -F: '($2=="")' /etc/shadow                            //查看空口令账号。
```

加固空口令账号，使用命令：

```
passwd <用户名>                                           //为空口令账号设定密码。
```

**5.1 配置高强度密码策略**

为了确保系统的安全性，建议设置的口令复杂度策略为：口令最小长度不小于8，至少包含大写字母、小写字母、数字和特殊字符中的三种。

安装 PAM 的 cracklib 模块，cracklib 能提供额外的密码检查能力。

```bash
sudo apt install libpam-cracklib
```

修改文件“/etc/pam.d/common-password”。 一旦修改，策略会马上生效。

```bash
sudo vim /etc/pam.d/common-password
```

找到文件中的以下内容：

```
password requisite pam_cracklib.so retry=3 minlen=8 difok=3
```

添加参数“minlen”、“dcredit”、“ucredit”、“lcredit”、“ocredit”。如果文件中已有这些参数，直接修改参数值即可，参数说明如表1所示。

示例：

```
password requisite pam_cracklib.so retry=3 minlen=9 dcredit=-1 ucredit=-1 lcredit=-1 ocredit=-1 difok=3
```

**5.2 用户连续登陆失败锁定**

在3次登录尝试失败后账户将被锁定至少15分钟，或者由管理员将其解锁。

在/etc/pam.d/common-auth中添加如下绿色字体内容，必须按下面顺序添加，命令：

```bash
sudo vim /etc/pam.d/common-auth
```

插入内容：

```
.
.
.
# here are the per-package modules (the "Primary" block)
auth    required pam_faillock.so preauth audit silent deny=3 fail_interval=900 unlock_time=900 even_deny_root root_unlock_time=900
auth	[success=1 default=ignore]	pam_unix.so nullok
# here's the fallback if no module succeeds
# BEGIN ANSIBLE MANAGED BLOCK
auth    [default=die] pam_faillock.so authfail audit deny=3 fail_interval=900 unlock_time=900 even_deny_root root_unlock_time=900
auth    sufficient pam_faillock.so authsucc audit deny=3 fail_interval=900 unlock_time=900 even_deny_root root_unlock_time=900
auth	requisite			pam_deny.so
.
.
.
```

参数解析：

```ini
audit                     //如果用户不存在，则把该用户名记录到系统日志中。
Silent                   //不打印信息性的消息
deny=3                  //用户连续认证失败次数超过3则锁定
fail_interval=900     //间隔时间的长度，在这个时间段内连续的
unlock_time=900      //锁定后n秒后，访问将被重新启用，在没有设置faillock的情况下，不会重新启用。
even_deny_root      //Root账户和普通账户一样可以被锁定。
root_unlock_time=900   //在root账户被锁定后, 允许在n秒后访问该账户。
参数解析来源/etc/security/faillock.conf文件
```

上述参数可以按需添加，如需全部添加，可以参考下面格式：

示例：

```
auth    required pam_faillock.so preauth audit silent deny=3 fail_interval=900 unlock_time=900 even_deny_root root_unlock_time=900
```

接着编辑/etc/pam.d/common-account，命令：

```bash
sudo vim /etc/pam.d/common-account
```

在文件末尾插入内容：

```
# end of pam-auth-update config
account    required pam_faillock.so
```

常用操作命令：

查看所有用户的尝试失败登录次数

```bash
sudo faillock
```

主要看faillock命令，显示的valid值，v表示有效，i表示无效。

查看指定用户(test用户)

```bash
sudo faillock --user test
```

解锁指定用户账户(test用户)

```bash
sudo faillock --user test --reset
```

解锁所有用户

```bash
sudo faillock --reset
```

重启系统也能解锁所有用户。

**5.3 禁止root用户密码登陆**

建议是通过Cockpit Web管理面板禁止root用户密码登陆，平时保持其处于禁用状态，如有需要时可以很方便就通过此处开启，用完即随手关闭。

通过Cockpit Web管理面板-账户-root用户-选项-禁用交互式密码，打上勾表示禁止root用户使用密码登陆。

**5.4 限制指定用户外网登陆**

使用pam\_access模块来限制ssh登录源,ssh服务使用的服务名为sshd,pam\_access模块使用的配置文件路径为/etc/security/access.conf

在ssh服务中添加pam\_access模块

## 切换到pam.d目录，备份远文件

```bash
cd /etc/pam.d && sudo cp sshd sshd.old
```

## 使用vi编辑器编辑sshd文件

```bash
sudo vi sshd
```

## 添加pam\_access模块

```
account  required  pam_access.so
```

在pam配置文件中添加限制条目，条目的格式如下：

+/-:users:origins

+/- :+号表示授权访问，-号表示拒绝访问

users :users表示限制的用户或用户组，多个用户或组时使用空格分隔

origins:origins表示来源，可以是本地主机名、ip地址/段，域名，有几个特殊关键词：ALL表示所有，LOCAL表示本地，EXCEPT表示除了

当有多条规则时，执行的顺寻是自上而下

## 切换到配置文件目录，备份原文件

```bash
cd /etc/security && sudo cp access.conf access.conf.old
```

## 编辑配置文件

```bash
sudo vi access.conf
```

## 在文件最后添加一行,只允许用户kim通过192.168.0.90地址登录

```
+:kim:192.168.0.90

-:kim:ALL
```

**5.5 限制指定用户夜间登陆**

pam\_time模块用来限制cockpit登录的时间，cockpit服务使用的服务名为cockpit,pam\_time模块使用的配置文件路径为/etc/security/time.conf,在需要对服务器进行维护的时候，或者是在特定时间禁止用户登录服务器。

1、在cockpit服务中添加pam\_time模块，打开文件：

```bash
sudo vim /etc/pam.d/cockpit
```

添加pam\_time模块：

```
#%PAM-1.0
auth       required     pam_sepermit.so
auth       substack     common-auth
auth       optional     pam_ssh_add.so
# Limit login time
account    required     pam_time.so
.
.
.
```

2、在pam配置文件中添加限制条目，条目的格式如下：

```
services;devices;users;times
```

services:可以使用的services都包含在/etc/pam.d目录中

devices :可以使用的device有:\*表示所有设备，!ttyp\*表示除虚拟设别外的所有设备，ttyp\*远程登录设备

users :限制的用户或组，使用列表时，各元素之间使用符号|分隔

time :限制的时间，由2段组成，第一段是首字母大写的星期缩写，第二段是时间段

星期缩写：Mo、Tu、We、Th、Fr、Sa、Su

特殊缩写：Wk工作日、Wd周末、Al每周的每天、WdSa周日、WdSu周六、WkMo除周一外的工作日

3、编辑配置文件

```bash
sudo vim /etc/security/time.conf
```

4、在文件末尾添加一行,允许用户root和test在每天凌晨0点到8点外的时间登录

```
cockpit;*;root|test;!A10000-0800
```

**5.7 限制用户同时登陆数量**

在大多数Linux发行版中，有一个叫做limit.conf的文件，你可以定义一个用户或用户组的最大并发SSH会话数量。如果特定用户试图进入系统的次数超过允许的登录次数，他/她将被拒绝访问。

操作步骤，编辑/etc/security/limits.conf文件：

```bash
sudo vim /etc/security/limits.conf
```

在文件末行添加下面内容：

要限制特定用户（例如ostechnix）的并发 SSH 会话数，请在末尾添加以下行：

```
ostechnix  hard    maxlogins   2
```

如果要限制一组用户的连接数，请添加以下行：

```
@mygroup   hard    maxlogins   3
```

将@mygroup替换为您的组名。在这种情况下，mygroup 中的所有用户都不能登录超过3次。

如果要限制系统中所有用户（全局）的 SSH 会话，请改为添加以下行：

```
*  hard    maxlogins   3
```

这里，星号表示全局（即系统中的所有用户）。定义每个用户/组或整个系统的最大会话数后，保存并关闭文件。

如需限制系统中Cockpit Web管理面板用户同时登陆数量，可以按如下配置添加内容：

```bash
sudo vim /etc/pam.d/cockpit
```

插入下列内容（只需要插入绿色字体部分内容，灰色部分为默认自带内容）：

```
#%PAM-1.0
auth       required     pam_sepermit.so
auth       substack     common-auth
auth       optional     pam_ssh_add.so
# Limit login time
account    required     pam_time.so
# Set up user limits from /etc/security/limits.conf.
session    required     pam_limits.so
.
.
.
```

保存后退出即刻生效。

**5.6 限制用户SU**

限制能su到root的用户。操作步骤

使用命令：

```bash
sudo vim /etc/pam.d/su
```

修改配置文件，在配置文件中添加行。例如，只允许sudo组用户su到root，则添加

```
auth required pam_wheel.so group=sudo
```

添加后如下所示：

```
#
# The PAM configuration file for the Shadow `su' service
#
auth required pam_wheel.so group=sudo
# This allows root to su without passwords (normal operation)
auth       sufficient pam_rootok.so
.
.
.
```

**5.8 用户登陆邮件通知告警**

通过 PAM 模块，就可以实现用户登录，root 权限获取时，通过邮件等方式进行通知。以实现，预先知道，预先警惕的目标，降低受影响的范围。以下是通过 PAM 模块实现的邮件通知用户登录的功能。

1、以管理员身份登录虚拟机，并切换成 root 用户。

2、新建脚本，命令：

```bash
sudo vim /etc/pam.d/login-notifiy.sh
```

(该脚本可以存放在任意位置，但是需要将后续的路径指定好即可),内容如下：

```
#!/bin/bash

[ "$PAM_TYPE" = "open_session" ] || exit 0
{
echo "User: $PAM_USER"
echo "Ruser: $PAM_RUSER"
echo "Rhost: $PAM_RHOST"
echo "Service: $PAM_SERVICE"
echo "TTY: $PAM_TTY"
echo "Date: `date`"
echo "Server: `uname -a`"
} | mail -s "`hostname -s` $PAM_SERVICE login: $PAM_USER" user@yourdomain.com
```

[脚本中的user@yourdomain.com](mailto:脚本中的user@yourdomain.com)修改为你要接收通知的邮箱地址。

3、编辑文件

```bash
sudo vim /etc/pam.d/common-session
```

4、在文件最后追加一行：

```
session optional pam_exec.so debug /bin/bash /etc/pam.d/login-notifiy.sh
```

5、保存并退出。

至此，每一个用户登录都会发邮件通知给收件人，内容包括用户名以及登录的 IP 地址信息。如果遇到陌生 IP，那么就要注意，该主机是否正在遭受攻击。

注意：来源教程原文上脚本名称前后不一致，会导致脚本执行出错，如是按来源教程操作，记得修改脚本名称，使其前后名称一致。

**5.9 超时自动注销活动状态**

设置系统登录后，连接超时时间，增强安全性。操作步骤，使用命令：

```bash
sudo vim /etc/profile
```

修改配置文件，在文件末行添加下列内容：

```ini
# 超时自动退出
TMOUT=180
```

即超时时间为三分钟。

**5.10 记录所有用户的登录和操作日志**

通过脚本代码实现记录所有用户的登录操作日志，防止出现安全事件后无据可查。

操作步骤

```bash
sudo vim /etc/profile
```

打开配置文件，在配置文件末行输入以下内容：

```
# 记录所有用户的登录和操作日志
history
 USER=`whoami`
 USER_IP=`who -u am i 2>/dev/null| awk '{print $NF}'|sed -e 's/[()]//g'`
 if [ "$USER_IP" = "" ]; then
 USER_IP=`hostname`
 fi
 if [ ! -d /var/log/history ]; then
 mkdir /var/log/history
 chmod 777 /var/log/history
 fi
 if [ ! -d /var/log/history/${LOGNAME} ]; then
 mkdir /var/log/history/${LOGNAME}
 chmod 300 /var/log/history/${LOGNAME}
 fi
 export HISTSIZE=4096
 DT=`date +"%Y%m%d_%H:%M:%S"`
 export HISTFILE="/var/log/history/${LOGNAME}/${USER}@${USER_IP}_$DT"
 chmod 600 /var/log/history/${LOGNAME}/*history* 2>/dev/null
```

运行命令加载配置生效：

```
source /etc/profile
```

注意：/var/log/history 是记录日志的存放位置，可以自定义。

通过上述步骤，可以在 /var/log/history 目录下以每个用户为名新建一个文件夹，每次用户退出后都会产生以用户名、登录IP、时间的日志文件，包含此用户本次的所有操作（root用户除外）。

**5.11 禁止SSH服务开机自启动**

为了系统的安全起见，建议SSH服务在有需要用的时候通过Cockpit Web面板开启，平常则处于关闭状态。开启路径：Cockpit-服务-ssh.service-启动

关闭ssh服务开机自动启动，命令：

```bash
sudo systemctl disable ssh
```

常用操作：

```
设置开机自动启动ssh服务，命令：
sudo systemctl enable ssh

单次开启ssh，命令：
sudo systemctl start ssh

单次关闭ssh，命令：
sudo systemctl stop ssh
```

**5.11 安装防火墙**

推荐使用firewalld防火墙的理由是，Cockpit Web管理面板搭配firewalld防火墙可以提供一个可视化的防火墙管理界面，对新手友好。

Ubuntu 22.04 已UFW默认安装。最好只使用一个防火墙。所以禁用 UFW：

```bash
sudo ufw disable
```

然后更新系统包：

```bash
sudo apt update
```

下一步是从apt存储库安装firewalld

```bash
sudo apt -y install firewalld
```

检查运行状态

```bash
sudo systemctl status firewalld
```

在终端输出的内容中将看到：

```
Active: active (running)
```

安装完成之后默认启动运行，需关闭之后进入cockpit配置规则。

关闭firewalld

```bash
sudo systemctl stop firewalld
```

登陆cockpit-网络-防火墙-打开防火墙-添加新区-信任级别- public，允许的地址-整个子网

**5.12 安装自动封锁软件**

第 1 步 — 安装 Fail2ban

Fail2ban 在 Ubuntu 的软件存储库中可用。首先以非根用户身份运行以下命令来更新您的软件包列表并安装 Fail2ban：

```bash
sudo apt update
sudo apt install fail2ban -y
```

Fail2ban 安装后会自动设置后台服务。但是，默认情况下它是禁用的，因为它的某些默认设置可能会导致不良影响。您可以使用以下systemctl命令验证这一点：

```bash
systemctl status fail2ban.service
```

终端中输出的内容：

```
● fail2ban.service - Fail2Ban Service
     Loaded: loaded (/lib/systemd/system/fail2ban.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2022-11-22 09:03:07 CST; 1min 5s ago
       Docs: man:fail2ban(1)
   Main PID: 52196 (fail2ban-server)
      Tasks: 5 (limit: 4534)
     Memory: 12.9M
        CPU: 166ms
     CGroup: /system.slice/fail2ban.service
             └─52196 /usr/bin/python3 /usr/bin/fail2ban-server -xf start
```

第 2 步 – 配置 Fail2ban

Fail2Ban的配置文件：/etc/fail2ban/

Fail2Ban的安装目录：/usr/share/fail2ban/

Fail2Ban日志文件：/var/log/fail2ban.log

达到阈值之后的执行Fail2Ban的动作的配置文件：/etc/fail2ban/action.d/

包含Fail2Ban所有的过滤规则：/etc/fail2ban/filter.d/

fail2ban 服务将其配置文件保存在该/etc/fail2ban目录中。在本教程中，您将创建jail.local. 你可以通过复制来做到这一点jail.conf：

```bash
sudo cp /etc/fail2ban/jail.{conf,local}
```

现在您可以开始进行配置更改。vim在或您喜欢的文本编辑器中打开文件：

```bash
sudo vim /etc/fail2ban/jail.local
```

当您滚动文件时，本教程将查看您可能想要更新的一些选项。位于文件顶部附近部分下的设置[DEFAULT]将应用于 Fail2ban 支持的所有服务。在文件的其他地方，有用于[sshd]和用于其他服务的标头，其中包含将在默认设置之上应用的特定于服务的设置。

```ini
#全局设置
[DEFAULT]

#此参数标识应被禁止系统忽略的 IP 地址。默认情况下，这只是设置为忽略来自机器本身的流量，这样您就不会填写自己的日志或将自己锁定。
ignoreip = 127.0.0.1/8 ::1

#此参数设置禁令的长度，以秒为单位。默认值为-1，表示将永久禁止IP地址，设置值为1h，则禁止1小时。
bantime  = -1

#此参数设置 Fail2ban 在查找重复失败的身份验证尝试时将关注的窗口。默认设置为 1d ，这意味着软件将统计最近 1 天内的失败尝试次数。
findtime  = 1d

#这设置了在禁止之前在窗口内允许的失败尝试次数。
maxretry = 5

#此条目指定 Fail2ban 将如何监视日志文件。设置auto意味着 fail2ban 将尝试pyinotify, 然后gamin, 然后基于可用的轮询算法。inotify是一个内置的 Linux 内核功能，用于跟踪文件何时被访问，并且是Fail2ban 使用pyinotify的 Python 接口。
backend = auto

#这定义了是否使用反向 DNS 来帮助实施禁令。将此设置为“否”将禁止 IP 本身而不是其域主机名。该warn设置将尝试查找主机名并以这种方式禁止，但会记录活动以供审查。
usedns = warn

#如果将您的操作配置为邮件警报，这是接收通知邮件的地址。
destemail = root@localhost

#发送者邮件地址
sender = root@<fq-hostname>

#这是用于发送通知电子邮件的邮件传输代理。
mta = mail

#“action_”之后的“mw”告诉 Fail2ban 向您发送电子邮件。“mwl”也附加了日志。
action = %(action_mw)s

#这是实施 IP 禁令时将丢弃的流量类型。这也是发送到新 iptables 链的流量类型。
protocol = tcp

##这里banaction必须用firewallcmd-ipset,这是fiewalll支持的关键，如果是用Iptables请不要这样填写
banaction = firewallcmd-ipset

[SSH]

enabled     = true
port        = ssh
filter      = sshd
logpath     = /var/log/auth.log
```

不要忘记在每次配置更改后重新启动 Fail2ban 服务。重启命令：

```bash
sudo systemctl restart fail2ban
```

常用命令：

```
#启动
systemctl start fail2ban

#停止
systemctl stop fail2ban

#开机启动
systemctl enable fail2ban

#查看被ban IP，其中sshd为名称
fail2ban-client status sshd

#删除被ban IP
fail2ban-client set sshd unbanip 192.168.111.111

#查看日志
tail /var/log/fail2ban.log
```

设置邮件通知告警

配置中文邮件格式（可选项，默认为英文）：

```bash
sudo cp /etc/fail2ban/action.d/mail-whois.{conf,local}
```

然后编辑mail-whois.local文件，

```bash
sudo vim /etc/fail2ban/action.d/mail-whois.local
```

替换成下面的内容：

```ini
# Fail2Ban configuration file
#
# Author: Cyril Jaquier
#
#

[INCLUDES]

before = mail-whois-common.conf

[Definition]

# bypass ban/unban for restored tickets
norestored = 1

# Option:  actionstart
# Notes.:  command executed on demand at the first ban (or at the start of Fail2Ban if actionstart_on_demand is set to false).
# Values:  CMD
#
actionstart = printf %%b "你好！\n
              Fail2ban监视<name> 服务已成功启动。\n
              敬请注意！\n
              Fail2Ban"|mail -s "[Fail2Ban] <name>: 在 <fq-hostname> 服务器上启动" <dest>

# Option:  actionstop
# Notes.:  command executed at the stop of jail (or at the end of Fail2Ban)
# Values:  CMD
#
actionstop = printf %%b "你好！\n
             Fail2ban监视<name> 服务已被停止。\n
             敬请注意！\n
             Fail2Ban"|mail -s "[Fail2Ban] <name>: 在 <fq-hostname> 服务器上停止" <dest>

# Option:  actioncheck
# Notes.:  command executed once before each actionban command
# Values:  CMD
#
actioncheck =

# Option:  actionban
# Notes.:  command executed when banning an IP. Take care that the
#          command is executed with Fail2Ban user rights.
# Tags:    See jail.conf(5) man page
# Values:  CMD
#
actionban = printf %%b "警告!!!\n
            攻击者IP：<ip>\n
            被攻击机器名：`uname -n` \n
            被攻击机器IP：`/bin/curl ifconfig.co` \n
            攻击服务：<name> \n
            攻击次数：<failures> 次 \n
            攻击方法：暴力破解，尝试弱口令.\n
            该IP：<ip>已经被Fail2Ban加入防火墙黑名单,屏蔽时间<bantime>秒.\n\n
            以下是攻击者 <ip>信息 :\n
            `/bin/curl https://ip.useragentinfo.com/json?ip=<ip>`\n\n
            Fail2Ban邮件提醒\n\n "|/bin/mailx -s "<fq-hostname>服务器:<name>服务疑似遭到<ip>暴力攻击。" <dest>

# Option:  actionunban
# Notes.:  command executed when unbanning an IP. Take care that the
#          command is executed with Fail2Ban user rights.
# Tags:    See jail.conf(5) man page
# Values:  CMD
#
actionunban =

[Init]

# Default name of the chain
#
name = default

# Destination/Addressee of the mail
#
dest = root
```

说明

通过curl [ifconfig.co](http://ifconfig.co)获取服务器的外网IP地址，方便知道哪台机报出来的告警。

通过curl <https://ip.useragentinfo.com/json?ip> =<ip> 查询获取攻击者的IP信息。

不要忘记在每次配置更改后重新启动 Fail2ban 服务。重启命令：

```bash
sudo systemctl restart fail2ban
```

配置完成后效果：

![配图](/upload/a6758ce2a99897a4482416882cdf4adf7999245d.png@!web-article-pic-dvpc.webp)

![配图](/upload/399ff6b8eb6de2ffe4be863bd8b35f1870a18265.png@1256w_846h_!web-article-pic.webp)

服务被攻击通知

**5.14 安装病毒防护软件**

ClamAV 是一个开源的防病毒软件，可用于检测木马，病毒，恶意软件和其他恶意威胁。适用于 Linux、macOS 和 Windows 平台。

参考：<https://blog.csdn.net/zhongxj183/article/details/128346651?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EAD_ESQUERY%7Eyljh-1-128346651-blog-126953787.pc_relevant_3mothn_strategy_and_data_recovery&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EAD_ESQUERY%7Eyljh-1-128346651-blog-126953787.pc_relevant_3mothn_strategy_and_data_recovery&utm_relevant_index=2>

官网：<http://www.clamav.net/>

## 基于Ubuntu搭建HomeNAS（六、存储管理）

**6.1 硬盘管理**

通过Cockpit Web管理面板进行管理。

**6.2 软Raid管理**

通过Cockpit Web管理面板进行管理。

**6.3 硬盘自动休眠**

hdparm

参考：<https://manpages.ubuntu.com/manpages/jammy/man8/hdparm.8.html>

**6.4 硬盘健康监测**

SMART是现代硬盘驱动器中的一个系统，旨在报告可能表明即将发生故障的情况。smartmontools是一个免费的软件包，可以监控 SMART 属性并运行硬盘自检。

安装smartmontools：

```bash
sudo apt install smartmontools
```

检查驱动器的SMART功能

要确保您的驱动器支持 SMART，请键入：

```bash
sudo smartctl -i /dev/sda
```

其中 /dev/sda 是你的硬盘。这将为您提供有关驱动器的简要信息。最后两行可能如下所示：

```
SMART support is: Available - device has SMART capability.

SMART support is: Enabled
```

启用SMART

如果您的驱动器未启用 SMART，您可以通过键入以下内容来启用它：

```bash
sudo smartctl -s on /dev/sda
```

检查硬盘整体健康状况

```bash
sudo smartctl -H /dev/sda
```

此命令应返回：

```
=== START OF READ SMART DATA SECTION ===

SMART overall-health self-assessment test result: PASSED
```

如果它没有返回 PASSED，您应该立即备份所有数据。您的硬盘驱动器可能出现故障。

测试驱动器

您可以在安装驱动器时运行任何类型的测试，尽管性能可能会有所下降。可以在驱动器上进行三种类型的测试：

短

扩展（长）

传输

要查找执行每个测试所需时间的估计值，请键入：

```bash
sudo smartctl -c /dev/sda
```

最有用的测试是扩展测试（长）。您可以通过键入以下内容来启动测试：

```bash
sudo smartctl -t long /dev/sda
```

结果

您可以通过键入以下内容来查看驱动器的测试统计信息：

```bash
sudo smartctl -l selftest /dev/sda
```

要显示 IDE 驱动器的详细 SMART 信息，请键入：

```bash
sudo smartctl -a /dev/sda
```

要显示 SATA 驱动器的详细 SMART 信息，请键入：

```bash
sudo smartctl -a -d ata /dev/sda
```

注意：这也适用于通过 SCSI 堆栈运行并显示为 /dev/sdX 的新内核中的 IDE 驱动器

部分字段的含义

```
=== START OF READ SMART DATA SECTION ===
SMART Attributes Data Structure revision number: 16
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME
  1 Raw_Read_Error_Rate     读取错误率
  3 Spin_Up_Time            起转时间
  4 Start_Stop_Count        启动停止次数
  5 Reallocated_Sector_Ct   重新分配扇区计数
  7 Seek_Error_Rate         寻道错误率
  9 Power_On_Hours          通电时间
 10 Spin_Retry_Count        起转重试次数
 11 Calibration_Retry_Count 重新校准重试次数
 12 Power_Cycle_Count       启动<->关闭循环次数
192 Power-Off_Retract_Count 断电磁头缩回计数
193 Load_Cycle_Count        磁头加载/卸载循环计数
194 Temperature_Celsius     温度
196 Reallocated_Event_Count 在分配扇区物理位置事件计数（与坏道无关）
197 Current_Pending_Sector  当前等待中扇区数（状态存疑/不稳定-等待后续判断）
198 Offline_Uncorrectable   无法修正的扇区总数
199 UDMA_CRC_Error_Count    UltraDMA CRC错误计数
200 Multi_Zone_Error_Rate   写入错误率
```

使用示例：

```
# 监测硬盘1
/dev/sda -o on -S on  -H -l error -l selftest -f -s (O/../../1/2|S/../../../4|L/../../2/5) -I 194 -W 4,45,55 -R 5 -m yourname@qq.com -M exec /usr/share/smartmontools/smartd-runner
# 监测硬盘2
/dev/sdb -o on -S on  -H -l error -l selftest -f -s (O/../../1/2|S/../../../4|L/../../2/5) -I 194 -W 4,45,55 -R 5 -m yourname@qq.com -M exec /usr/share/smartmontools/smartd-runner
# 测试邮件通知
/dev/sda -o on -S on  -H -l error -l selftest -f -s (O/../../1/2|S/../../../4|L/../../2/5) -I 194 -W 4,45,55 -R 5 -m yourname@qq.com -M test
```

上述例子来源于/etc/smartd.conf，以下内容为文件原文：

```
# 第一个 ATA/SATA 或 SCSI/SAS 磁盘。 监控所有属性，启用
# 自动在线数据收集，自动属性自动保存，并
# 每天凌晨 2-3 点开始短的自检，长的自检
# 周六凌晨3-4点之间。
#/dev/sda -a -o on -S on -s (S/./././02|L/././6/03)

# 监控SMART状态、ATA错误日志、自检日志，并跟踪
# 所有属性的变化，除了属性 194
#/dev/sdb -H -l error -l selftest -t -I 194

# 监控所有属性，除了正常化的温度（通常是194）。
# 但跟踪温度变化 >= 4 摄氏度，报告温度
# >= 45 摄氏度和 Reallocated_Sector_Ct (5) 原始值的变化。
# 在SMART故障或温度>=55摄氏度时发送邮件。
#/dev/sdc -a -I 194 -W 4,45,55 -R 5 -m admin@example.com
```

如需可视化的SMART数值界面，请在Docker容器中部署Scrutiny，该容器可以提供可视化界面。Scrutiny需搭配smartmontools工具才能正常使用，安装完smartmontools之后，无需按照上面的复杂操作配置smartmontools即可搭配Scrutiny使用，上面的smartmontools各类配置操作，仅是适用于无需可视化界面情况下的。

Scrutiny 是一种硬盘驱动器运行状况仪表板和监控解决方案，将制造商提供的 SMART 指标与实际故障率相结合。用于 smartd SMART 监控的 WebUI

项目地址：<https://github.com/AnalogJ/scrutiny>

安装教程：<https://www.tauceti.blog/posts/easy-hard-disk-health-monitoring-with-scrutiny-and-smart/>

安装教程：<https://blog.csdn.net/wbsu2004/article/details/124095004>

![配图](/upload/01692bab779884aea86f5deb01bfb566f5e053ca.png@1256w_634h_!web-article-pic.webp) Scrutiny

**6.5 安装联合文件系统**

mergerfs是一个联合文件系统，旨在简化跨众多商品存储设备的文件存储和管理。它类似于mhddfs、unionfs和aufs。

项目地址：<https://github.com/trapexit/mergerfs>

## 基于Ubuntu搭建HomeNAS（七、Docker服务）

**7.1 安装Docker**

在新主机上首次安装 Docker Engine 之前，您需要设置 Docker 存储库。之后，您可以从存储库安装和更新 Docker。（推荐通过存储库安装，方便后期版本升级。）

A、设置存储库

1.更新apt包索引并安装包以允许apt通过 HTTPS 使用存储库：

```bash
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

2.添加 Docker 的官方 GPG 密钥：

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

3.使用以下命令设置存储库：

```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

B、安装 Docker 引擎

1.更新apt包索引：

```bash
sudo apt-get update
```

2.安装 Docker Engine、containerd 和 Docker Compose。

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

3.hello-world通过运行镜像验证 Docker Engine 安装是否成功 ：

```bash
sudo docker run hello-world
```

查看Docker版本命令：

```bash
docker version
```

查看Docker Compose版本命令：

```bash
docker compose version
```

**7.2 容器管理**

Portainer是一个可视化的容器镜像的图形管理工具，利用Portainer可以轻松构建，管理和维护Docker环境。 而且完全免费，基于容器化的安装方式，方便高效部署。

请将路径/srv/volume\_1/data/docker/portainer替换为您的，此路径存储Portainer配置文件。

```bash
sudo docker run -d -p 8000:8000 -p 9443:9443 -p 9000:9000 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v /srv/volume_1/data/docker/portainer:/data portainer/portainer-ce:latest
```

安装完成后，可以通过打开 Web 浏览器并转到Portainer管理界面：

```
http://localhost:9000或https://localhost:9443
```

**7.3 反向代理**

Nginx Proxy Manager 是用于管理 Nginx 代理主机的 Docker 容器，具有简单、强大的界面。它使您可以轻松地转发到您在家里或其他地方运行的网站，包括免费的 SSL，而无需对 Nginx 或 Letsencrypt 了解太多。

官网：<https://nginxproxymanager.com>

安装教程：<https://blog.csdn.net/wbsu2004/article/details/122533684>

<https://blog.csdn.net/wbsu2004/article/details/126698539?spm=1001.2014.3001.5502>

泛解析说明：<https://cloud.tencent.com/document/product/302/9073>

解决报错 (Bad Gateway on Login)：<https://www.reddit.com/r/nginx/comments/pt352s/comment/hdvucab/>

[章出处:b站 谷玄天](https://www.reddit.com/r/nginx/comments/pt352s/comment/hdvucab/)

原贴：https://space.bilibili.com/381396284

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
