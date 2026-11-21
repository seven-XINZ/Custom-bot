# 皎月连一键内网穿透

> 标题：皎月连一键内网穿透
> 分类：代理与穿透
> 标签：nas、群晖、frp、内网穿透、安卓、ubuntu
> 原文：https://www.xinz.fun/archives/jiaoyuelian

> **导读**：这篇围绕「皎月连一键内网穿透」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾代理与穿透的读者。执行前建议先备份原配置，并在测试环境验证。

### P2P** **TCP&UDP

真正的点对点直连内网穿透，即便没有IPV6也 同时提供TCP和UDP两种连接协议
可以适应**两端同时都是对称型NAT**的网络环境， 数据传输采用AES128位加密算法
没有第三方服务器中转数据，更安全、更高效。 可满足更多应用场景

### 性能优异 灵活部署 简易操作

点对点直连 可自由制定端口映射 一键开启直连
速度不受服务器影响 满足各种应用需求 避免繁杂操作
摆脱流量与速度限制

### 使用场景

远程游戏

远程办公

远程维护

## 使用说明

**软件有****组网****和****映射****两种模式**

**一、组网模式**（串流推荐）

**服务端：**

 打开软件并登录，在左侧选择“服务端”

         1.开启“组网模式”开关

         2.输入6-20位页面访问密码（这个作用是限制其他组网进来的客户端访问控制页面）

         3.点击左下方“开启服务”按钮，成功后按钮会变成黄色

![clip_image001.jpg](https://www.natpierce.cn/uploads/ueditor/image/20240122/ed_1705907053686691.jpg "ed_1705907053686691.jpg")

**客户端**（这里以安卓举例）：

         打开软件并登录

         1.在左上方列表中选择一个在线主机（服务端的主机名）

         2.点击下方“连接”按钮，连接成功后按钮会变成黄色（安卓端第一次使用会询问是否授权，选择“是”）

![clip_image003.jpg](https://www.natpierce.cn/uploads/ueditor/image/20240122/ed_1705907104699099.jpg "ed_1705907104699099.jpg")

   3.记住映射列表中的局域网ip【10.6.22.1】 按手机home键将软件后台运行

         4.打开应用软件（例如moonlight），输入虚拟局域网ip【10.6.22.1】建立连接

![clip_image005.jpg](https://www.natpierce.cn/uploads/ueditor/image/20240122/ed_1705907123897554.jpg "ed_1705907123897554.jpg")

**--------------------------------分割线--------------------------------**

**二、映射模式**

**服务端：**

 打开软件并登录，在左侧选择“服务端”

         1.关闭“组网模式”开关

         2.点击右下方“添加端口映射”按钮，这里以windows远程桌面为例添加了两条映射

         3.点击左下方“开启服务”按钮，成功后按钮会变成黄色

![2.png](https://www.natpierce.cn/uploads/ueditor/image/20240327/ed_1711507067808804.png "ed_1711507067808804.png")

**客户端：**

 在另一地点打开软件并登录，在左侧选择“客户端”

    1.在线主机列表中会出现服务端的主机名，选择一个在线主机

    2.点击“连接主机”按钮，连接成功后按钮会变成黄色

![clip_image009.jpg](https://www.natpierce.cn/uploads/ueditor/image/20240122/ed_1705907269755050.jpg "ed_1705907269755050.jpg")

3.打开应用程序（还是以windows远程桌面为例），输入【127.0.0.1:12345】进行连接

         这里127.0.0.1是固定的，12345就是服务端设置的远程端口，中间冒号不要少

![clip_image011.jpg](https://www.natpierce.cn/uploads/ueditor/image/20240122/ed_1705907301889571.jpg "ed_1705907301889571.jpg")

**常见问题**

**一、提示“未能成功建立P2P隧道”**

皎月连创建的P2P连接是点对点直连，中间没有第三方做数据中转，其弊端就是不能确保每次都100%连接成功，但可以通过多次发起连接来提高成功率。对连接成功率产生不良影响的因素如下：

1.连接过程中同时在使用其他P2P下载软件。

2.windows防火墙或其他网络防火墙，也包括路由器的防火墙。

3.互相连接的两端中有任意一端拥有多个出口IP地址（多出现于长城宽带或广电网络等小运营商）。

**二、提示“不支持的网络环境”**

出现该提示是因为当前两端主机都处于比较极端的网络环境，皎月连将不会尝试建立连接，请尝试将任意一端切换为不同的网络环境。如，移动端由数据流量切换为wifi网络，或者在不同的wifi网络中进行切换。

**三、提示“连接被阻断”**

关闭所有防火墙、杀毒软件，或者将程序文件添加白名单，windows自带的Defender杀毒软件也需要将皎月连程序添加到白名单。

**四、安卓连接成功后过段时间自动断开连接**

**首先确保皎月连的服务端没有被防火墙屏蔽**，然后在安卓设备[设置]->[电池]选项中将皎月连设置为允许后台运行。同时要注意不要开启手机的“省电模式”。

**五、软件页面打不开、****windows下双击右下角托盘图标没反应**

可以手动打开浏览器并访问地址:http://localhost:33272/

若不想每次手动操作，可尝试以下步骤：

1.查看浏览器是否支持websocket协议。

2.查看防火墙或杀毒软件是否禁用了websocket连接。

3.建议使用谷歌浏览器作为默认浏览器。

4.程序路径不要包含中文和空格。

**六、无法开机自启动**

1.检查程序路径是否包含中文，若包含请改为全英文且不包含空格的路径。

2.关闭windows的“快速启动”功能。

3.以管理员权限运行程序，在系统右键点击托盘图标，重新开关一次“开机启动”选项。

## 下载地址:

### 二进制文件

**X86\_64**

```
https://natpierce.oss-cn-beijing.aliyuncs.com/linux/natpierce-amd64-v0.357.tar.gz
```

**arm64**

```
https://natpierce.oss-cn-beijing.aliyuncs.com/linux/natpierce-arm64-v0.357.tar.gz
```

**arm32**

```
 https://natpierce.oss-cn-beijing.aliyuncs.com/linux/natpierce-arm32-v0.357.tar.gz
```

**mips**

```
https://natpierce.oss-cn-beijing.aliyuncs.com/linux/natpierce-mips-v0.357.tar.gz
```

### OpenWrt安装包

**x86\_64**

```
https://natpierce.oss-cn-beijing.aliyuncs.com/ipk/natpierce-amd64-v0.357.ipk
```

**arm64**

```
https://natpierce.oss-cn-beijing.aliyuncs.com/ipk/natpierce-arm64-v0.357.ipk
```

**arm32**

```
https://natpierce.oss-cn-beijing.aliyuncs.com/ipk/natpierce-arm32-v0.357.ipk
```

**mips**

```
https://natpierce.oss-cn-beijing.aliyuncs.com/ipk/natpierce-mips-v0.357.ipk
```

一键下载并安装:

```bash
sh -c "$(curl -sSL https://natpierce.oss-cn-beijing.aliyuncs.com/ipk/install.sh)"
```

### Docker镜像

x86\_64

```
https://natpierce.oss-cn-beijing.aliyuncs.com/docker/natpierce-amd64-v0.357.tar
```

**arm64**

```
https://natpierce.oss-cn-beijing.aliyuncs.com/docker/natpierce-arm64-v0.357.tar
```

**arm32**

```
https://natpierce.oss-cn-beijing.aliyuncs.com/docker/natpierce-arm32-v0.357.tar
```

**一键拉取并运行:**

```bash
docker run -it --name natpierce --restart=always --privileged=true --net=host -d natpierce/natpierce:latest
```

**单独拉取镜像:**

```bash
docker pull natpierce/natpierce:latest
```

### 关于我们

　　皎月连一键内网穿透能够实现两点之间的P2P直连内网穿透，并不是通过第三方服务器提供流量中转服务。软件采用了最新的P2P算法，在连接双方都没有公网IP和IPV6的情况下，可满足包括对称型NAT在内的大多数连接需求。因为在数据传输过程中不需要第三方服务器作为中转，所以节约了服务器成本和流量成本，同时又可以提高传输速度。数据在传输过程中采用了加密算法，拥有更高的安全性与私密性。在连接过程中提供了TCP与UDP两种传输协议，更广泛的满足使用需求。皎月连一键内网穿透可应用于家庭摄像头直连、NAS访问、远程控制或远程游戏联机、串流等各种应用场景。

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
