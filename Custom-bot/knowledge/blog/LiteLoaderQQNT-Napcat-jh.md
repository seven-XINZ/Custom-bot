# 【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件

> 标题：【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件
> 分类：机器人Bot
> 标签：docker、Linux
> 原文：https://www.xinz.fun/archives/LiteLoaderQQNT-Napcat-jh

> **导读**：这篇围绕「【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾机器人Bot的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 前言
2. 大致说明
3. 特别感谢
4. 创建文件和拉取镜像
5. VNC连接

## 前言

[TTS适配海豚Ai TTS-Online](https://www.ttson.cn/?source=falPMO) 使用文字转语音推荐

**本文由落幕所写我转载修改部分**

**这是一个新版本的NCQQ，结合了LiteLoaderQQNT，并在内加了自动同意好友和禁用QQNT更新，使用了Napcat插件来扩展api。不同于NTQQ版本的docker，NTQQ版本的是用了LLonebot插件，这个NCQQ使用的是Napcat插件虽然总体来说大同小异，根据插件作者的不同打包的不同的版本。**

## 大致说明

**这个NCQQ是有图形化页面的，而非官方的无头版本（无图形化页面更轻量），所以对配置要求还是有一些的，如果你有图形化查看消息和管理的需求，NCQQ可能是你的选择。如果你在乎的是轻量化可以下发的作者项目内找到docker项目，使用无头版本**

## 特别感谢

**感谢雪佬开发和维护，Napcat项目地址：**[**https://github.com/NapNeko/NapCatQQ**](https://github.com/NapNeko/NapCatQQ)

## 创建文件和拉取镜像
### 连接服务器创建文件夹

1. **首先我们连接我的服务器，不管你是本地服务器还是云服务器，用**`ssh工具`进行连接。这里我使用的是`FinalShell工具`连接的本地服务器进行`演示`
   [![file](https://lmu5.com/wp-content/uploads/2024/08/20240815212136415883.webp "【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 96")](https://lmu5.com/wp-content/uploads/2024/08/20240815212136415883.webp)
2. **然后我们输入命令进行创建，你可以看到在**`root目录`下创建了一个`ncqq`的文件夹（如果你打算多挂几个QQ那`换不同名字`即可）：

   ```bash
   mkdir -p ncqq
   ```

   [![file](https://lmu5.com/wp-content/uploads/2024/08/20240815212406389729.webp "【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 97")](https://lmu5.com/wp-content/uploads/2024/08/20240815212406389729.webp)

### 拉取镜像

**上面我们**`创建了文件夹`，下面就是`拉取镜像并挂载目录`等操作了。我来解释一下下面的命令大概的意思:`name`后面的`ncqq`意思就是容器的`名字`，看你自己，可以是任何其他的，`别冲突`就可以。然后`-v /root/ncqq/`这个就是让你上面`创建文件夹的路径`（如果你多号，自行更改即可）。然后是下面一堆的端口，我们只看`：前面`的不要管`：后面`的，第一个`5900`就是`VNC的端口`，如果你有其他的VNC项目部署的，那你可能要改成其他的。`3000端口`是`http用的`，一般来说用不到，所以也可以不加没所谓。`6099端口`就是`webui端口`，意思就是如果你有`穿透`或者`公网`，直接就可以把`端口`转出去，做到在外面都能`修改配置`。
```
docker run -d  --restart=always --name ncqq -v /root/ncqq/:/opt/QQ/resources/app/LiteLoaderQQNT/plugins/NapCat.Framework/config/ -p 5900:5900 -p 3000:3000 -p 6099:6099  luomubiji/ncqq:latest
```

[![file](https://lmu5.com/wp-content/uploads/2024/08/20240815213445242021.webp "【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 98")](https://lmu5.com/wp-content/uploads/2024/08/20240815213445242021.webp)

## VNC连接

1. **拉取完毕后我们就可以用**`vnc工具`进行连接了。（`本站官方群有提供各类的vnc工具`）这里还是用`1Remote工具`来演示。我们点击右上角的`+`号选择`添加`
   [![file](https://lmu5.com/wp-content/uploads/2024/08/20240815213908362095.webp "【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 99")](https://lmu5.com/wp-content/uploads/2024/08/20240815213908362095.webp)
2. **我们选择上面的**`vnc选项`，然后设置`名称`，往下拉找到`连接的地址`那一栏，输入你的`NCQQ`搭建所在的`IP或者域名`。
   [![file](https://lmu5.com/wp-content/uploads/2024/08/20240815214240132545.webp "【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 100")](https://lmu5.com/wp-content/uploads/2024/08/20240815214240132545.webp)

   密码默认是vncpasswd
3. **下拉输入密码一般默认是**`vncpasswd`，如果你打算更改可以参考下面的文章更改，其实内网的话就没必要了

1. [![file](https://lmu5.com/wp-content/uploads/2024/08/20240815214414335635.webp "【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 102")](https://lmu5.com/wp-content/uploads/2024/08/20240815214414335635.webp)
2. **添加后我们在**`全部`里找到刚才添加的VNC项目，双击连接即可
   [![file](https://lmu5.com/wp-content/uploads/2024/08/20240815214608235409.webp "【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 103")](https://lmu5.com/wp-content/uploads/2024/08/20240815214608235409.webp)
3. **出来的**`二维码`用你要当机器人的`QQ号扫码登录`即可。手机上出现`下次登录无需手机确认`打勾，登录！如果你出现`卡住`，`点不了`或者`扫码后退出了VNC连接`，`重连`即可。
   [![file](https://lmu5.com/wp-content/uploads/2024/08/20240815214900461698.webp "【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 104")](https://lmu5.com/wp-content/uploads/2024/08/20240815214900461698.webp)
4. **登录完毕后我们需要一些小小的设置，点击**`左下角`进入`设置`，在通用找到`软件更新`，让他变灰色就行了，`蓝色就是同意`，`灰色就是拒绝`。
   [![file](https://lmu5.com/wp-content/uploads/2024/08/20240815215104727984.webp "【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 105")](https://lmu5.com/wp-content/uploads/2024/08/20240815215104727984.webp)
5. **权限设置这里看你个人意愿，**`登录设置`这里，我们把两个都变成蓝色（`同意`）
   [![file](https://lmu5.com/wp-content/uploads/2024/08/20240815215215863468.webp "【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 106")](https://lmu5.com/wp-content/uploads/2024/08/20240815215215863468.webp)
6. **最后找到我们的插件**`Napcat`，打开，点击`打开配置页面`。
   [![file](https://lmu5.com/wp-content/uploads/2024/08/20240815215355806813.webp "【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 107")](https://lmu5.com/wp-content/uploads/2024/08/20240815215355806813.webp)
   [![file](https://lmu5.com/wp-content/uploads/2024/08/20240815215425981134.webp "【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 108")](https://lmu5.com/wp-content/uploads/2024/08/20240815215425981134.webp)
7. **到这里其实已经OK了，剩下的就是看你怎么玩了**

下面两篇文章可结合本文使用 可视化配置对接

[QChatGPT＋NapCat-Docker 部署运行-鑫仔博客 (xinz.fun)](https://www.xinz.fun/archives/1723789956916)

[无界bncr安装使用及开发适配-鑫仔博客 (xinz.fun)](https://www.xinz.fun/archives/1717170773466)

原文地址:[落幕屋 - 【NCQQ】Docker版本NCQQ结合了LiteLoaderQQNT与Napcat等插件 (lmu5.com)](https://lmu5.com/ncqq.html)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
