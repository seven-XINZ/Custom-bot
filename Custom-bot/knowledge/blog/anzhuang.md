# Debian系统最小化安装教程

> 标题：Debian系统最小化安装教程
> 分类：Linux运维
> 标签：debian
> 原文：https://www.xinz.fun/archives/anzhuang

> **导读**：这篇是「Debian系统最小化安装教程」的实操教程。下文按「一、Debian系统安装包下载」「二、选择安装方式（图形界面安装Graphical install）」「三、设置系统默认语言（选英文，避免奇怪bug）」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾Linux运维的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 一、Debian系统安装包下载
2. 二、选择安装方式（图形界面安装Graphical install）
3. 三、设置系统默认语言（选英文，避免奇怪bug）
4. 四、1、设置系统时区（选other-Asia-China）
5. 四、2、选Asia
6. 四、3、选China
7. 五、设置区域语言（选United States en\_US.UTF-8）
8. 六、设置键盘映射(选American English)
9. 七、设置主机名（一般保持默认，有冲突或不喜欢可更换）
10. 八、设置域名（留空）
11. 九、设置管理员密码（root用户）
12. 十、创建新普通用户（用户全名）
13. 以及其余 15 个小节

## 一、Debian系统安装包下载

**1.1进入官网：https://www.debian.org/，点击其他下载链接**

![配图](/upload/AgAABTPCXbaCHmDJBPRJj5-Dle5Bl768.png)

**1.2选择较庞大的完整安装映像，64 位 PC DVD-1 iso**

![配图](/upload/AgAABTPCXbYakB3jC6dLZbP9lJGxIUO1.png)![配图](/upload/AgAABTPCXbZXPdtni3RDiYMI-yB5FpjN.png)![配图](/upload/AgAABTPCXbZXPdtni3RDiYMI-yB5FpjN-xsjd.png)

**因Debian系统在安装过程中需要联网更新安全源，国内访问速度有时候异常缓慢，动则几个小时。故国内用户建议按上面教程下载完整系统镜像包，这样将避免此问题发生，完成系统安装只需要四分钟左右，大大提高系统安装效率。**

**镜像写入工具推荐使用：https://etcher.balena.io/或https://rufus.ie/zh/**

## 二、选择安装方式（图形界面安装Graphical install）

![配图](https://www.xinz.fun/upload/AgAABTPCXbZtsbVAKbpNlZ0A0Xt7JjIo.png)

## 三、设置系统默认语言（选英文，避免奇怪bug）

![配图](https://www.xinz.fun/upload/AgAABTPCXbZsQxP5Xa1BbZesLHL-23F0.png)

## 四、1、设置系统时区（选other-Asia-China）

![配图](/upload/AgAABTPCXbYBPsjamRBC0K_1nIVFdwoI-zlhc.png)

## 四、2、选Asia

![配图](/upload/AgAABTPCXbZXPdtni3RDiYMI-yB5FpjN-niol.png)

## 四、3、选China

![配图](/upload/AgAABTPCXbZ_cY27wC5L55aaPjMx3WuP.png)

## 五、设置区域语言（选United States en\_US.UTF-8）

![配图](/upload/AgAABTPCXbZ_cY27wC5L55aaPjMx3WuP-xdpq.png)

## 六、设置键盘映射(选American English)

![配图](/upload/AgAABTPCXbbGSBavMW5NvpceT4tHeNio.png)

## 七、设置主机名（一般保持默认，有冲突或不喜欢可更换）

![配图](/upload/AgAABTPCXbbKAzqUJKhANL1gupJidxap.png)

## 八、设置域名（留空）

![配图](/upload/AgAABTPCXbYUN2LCdVJHwL9R-BvJR9Ox.png)

## 九、设置管理员密码（root用户）

![配图](/upload/AgAABTPCXbaB5zX8-VxIUodgSNfhUJus.png)

## 十、创建新普通用户（用户全名）

![配图](/upload/AgAABTPCXbbWNljOejFD378SEKfBUb-E-yhhb.png)

## 11、新用户账户名称（登陆名称，建议和前面保持一致，避免出现混乱）

![配图](/upload/AgAABTPCXbYyZmmMSAZN-LIdxMBQ2wb4.png)

## 12、设置新用户密码（建议使用复杂密码）

![配图](/upload/AgAABTPCXbZX18M611xB3YpVC3k0RwRH.png)

## 13、进行系统盘磁盘分区（选Guided-use entire disk使用整个磁盘）

![配图](/upload/AgAABTPCXbabWE236-dOhbh31b-liEU0.png)

## 14、选择系统磁盘

![配图](/upload/AgAABTPCXbZk_wFGccNKpLjtS3AwvE_2.png)

## 15、选择分区方案（选All files in one partition将所有文件放在同一个分区）

![配图](/upload/AgAABTPCXba0kBQZM3VO1LM9mdhzd0IL.png)

## 16、完成分区操作并将修改写入磁盘（Finish partitioning and write changes to disk）

![配图](/upload/AgAABTPCXbZV_yv9kQhBDZEKafSJCC4T.png)

## 17、再次确认写入磁盘（Yes）

![配图](/upload/AgAABTPCXbbyhogPOmdDI6Ix8EkivafG.png)

## 18、是否需要扫描额外安装介质（选No）

![配图](/upload/AgAABTPCXbbxeb6W7K1M6pcYrKJ-pKsC.png)

## 19、是否需要使用网络镜像站点（选No）

![配图](/upload/AgAABTPCXbZM14lV_tlL6JFdD1F1WnHn.png)

## 20、是否要参加软件包流行度调查（选No）

![配图](/upload/AgAABTPCXbakTb50BCNEsayE63EQGF6V.png)

## 21、选择要安装的软件（建议只选最后两项）

![配图](/upload/AgAABTPCXbaLD-6az21MaZv4m5DRsZqh.png)

## 22、系统正在安装中

![配图](/upload/AgAABTPCXbazLKzqWq9D15Fl23LqdRlm.png)

## 23、系统已完成安装，点击Continue重启

![配图](/upload/AgAABTPCXbaJN_KF3spI9oEBk1oi7Cv2.png)

## 24、安装完成后用root账户登陆系统，输入命令查询IP地址（去路由器管理后台看也可）

```
ip addr
```

![配图](/upload/AgAABTPCXba6beuxsIxGwqui8BvM1Olh.png)

## 视频教程

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
