# 群晖docker安装clash，并设置代理

> 标题：群晖docker安装clash，并设置代理
> 分类：代理与穿透
> 标签：docker、clash、v2ray、nas
> 原文：https://www.xinz.fun/archives/搭建clash加ui

> **导读**：这篇是「群晖docker安装clash，并设置代理」的实操教程。下文按「一、下载」「二、运行」「三、增加 clash 配置」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾代理与穿透的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 一、下载
2. 二、运行
3. 三、增加 clash 配置
4. 四、配置 UI 界面（可选）
5. 五、设置代理
6. 五、1 windows
7. 五、2 安卓
8. 五、3 苹果
9. 六、自动更新 clash 配置

## 一、下载

进入 docker ui 界面搜索 **clash** ，选择 **dreamacro/clash** 点击下载。

![配图](/upload/image-zhhc.png)

[**#**](https://zhanghongyun.cn/article/detail/7#%E4%BA%8C%E3%80%81%E8%BF%90%E8%A1%8C)

## 二、运行

然后在映像中启动刚刚下载的镜像。

![配图](/upload/image-mucu.png)

点击下一步

将 **启用自动重新启动勾上**，再次点击下一步。

> 相当于 **NAS** 开机容器也启动，不需要手动重启 **clash 容器** 几乎不占用资源

![配图](/upload/image-oeaq.png)

点击新增端口，把容器内端口和 **NAS（服务器）** 内端口添加映射。

![配图](/upload/image-msqu.png)

按照如图配置端口。

- `7890`：`http`、`https` 端口；
- `7891`：`socks` 端口；
- `9090`：下文配置 UI 界面用到端口。不需要 UI 界面可不配置。

![配图](/upload/image-vcos.png)

添加文件映射，将 **NAS** 配置文件映射到容器内。

![配图](/upload/image-ojoj.png)

**NAS config.yaml** 文件目录按需配置。这里仅供参考。

NAS /docker/clash/config.yaml

容器内 /root/.config/clash/config.yaml

然后点击下一步。

![配图](/upload/image-esfu.png)

点击完成，即可运行 **clash** 容器。

![配图](/upload/image-oqxn.png)

![配图](/upload/image-dofb.png)

> 服务器命令行同理，docker 搜索容器，配置端口、文件映射，docker run 启动即可。

[**#**](https://zhanghongyun.cn/article/detail/7#%E4%B8%89%E3%80%81%E5%A2%9E%E5%8A%A0%20clash%20%E9%85%8D%E7%BD%AE)

## 三、增加 clash 配置

在 clash 客户端点击配置，选中一个配置，右击 **外部编辑** 中打开配置文件。将打开的文件拷贝一份到 NAS 中。（上一步配置文件映射地址 `/docker/clash/config.yaml`）

- 修改 `external-controller` 为 `0.0.0.0:9090` 广播地址
- `allow-lan`: `true` 可以代理局域网

> 最底部给出示例配置文件。

![配图](/upload/image-sfde.png)

![配图](/upload/image-tmkl.png)

然后重启容器，读取配置文件，这时就可以设置代理然后使用了。

![配图](/upload/image-oiwu.png)

[**#**](https://zhanghongyun.cn/article/detail/7#%E5%9B%9B%E3%80%81%E9%85%8D%E7%BD%AE%20UI%20%E7%95%8C%E9%9D%A2%EF%BC%88%E5%8F%AF%E9%80%89%EF%BC%89)

## 四、配置 UI 界面（可选）

步骤跟上面一样。

1. **注册表** 中搜索 `yacd` ，选中 `haishanh/yacd` 下载；
2. **映像** 中启动刚刚下载的镜像；

   1. 配置端口 `9080:80`；
   2. 不需要配置文件映射。
3. 启动镜像后进入 `http://192.168.0.101:9080/` ip 地址根据实际修改。端口号为刚刚配置的映射端口。

![配图](/upload/image-wegg.png)

![配图](/upload/image-lxjv.png)

默认为自动选择路线，每隔一段时间都会自动选择最优路线，有需求也可以选择其他线路。

我这里因为 openai 需要所以选择美国线路。

[**#**](https://zhanghongyun.cn/article/detail/7#%E4%BA%94%E3%80%81%E8%AE%BE%E7%BD%AE%E4%BB%A3%E7%90%86)

## 五、设置代理

[#](https://zhanghongyun.cn/article/detail/7#5.1%20windows)

## 五、1 windows

这里以 Windows 电脑为例（因为没有mac /(ㄒoㄒ)/~~）

![配图](/upload/image-mtbu.png)

点击编辑

![配图](/upload/image-ogvm.png)

修改代理 ip 地址和端口，点击保存即可。

![配图](/upload/image-ftcs.png)

现在就可以愉快的访问 [GitHub](https://github.com/hongyun-robot) 了。

[#](https://zhanghongyun.cn/article/detail/7#5.2%20%E5%AE%89%E5%8D%93)

## 五、2 安卓

> 这里手机系统是 `Color OS V12.1`，其他大同小异。

进入 wifi 设置中将代理改成手动，然后配置代理 ip 地址即可。 一般都是单个 wifi 设置。

![配图](/upload/image-gbbg.png)

[#](https://zhanghongyun.cn/article/detail/7#5.3%20%E8%8B%B9%E6%9E%9C)

## 五、3 苹果

> 这里手机系统是 `IOS 17.1.1`，其他大同小异

进入 wifi 设置中将代理改成手动，然后配置代理 ip 地址即可。

![配图](/upload/image-xyfi.png)

点击存储就可以了。

![配图](/upload/image-vxki.png)

[**#**](https://zhanghongyun.cn/article/detail/7#%E5%85%AD%E3%80%81%E8%87%AA%E5%8A%A8%E6%9B%B4%E6%96%B0%20clash%20%E9%85%8D%E7%BD%AE)

## 六、自动更新 clash 配置

编写定时任务脚本来每日自动更新 clash 配置。

在 `/docker/clash/` 中增加 `auto-reload-clash.sh` 脚本

![配图](/upload/image-qhsg.png)

```bash
shellcopy codewget -O /volume1/docker/clash/config.yaml 'https://你的订阅地址'
sed -i 's/127.0.0.1:9090/0.0.0.0:9090/g' /volume1/docker/clash/config.yaml
sed -i 's/allow-lan: true/allow-lan: true/' /volume1/docker/clash/config.yaml
sed -i 's/interval: 86400 }/interval: 3600 }/' /volume1/docker/clash/config.yaml
curl --location --request PUT 'http://localhost:9090/configs' --header 'Content-Type: application/json' --data-raw '{"path": "/root/.config/clash/config.yaml"}'
```

在这里找到订阅地址

![配图](/upload/image-xlsv.png)

复制这个订阅链接，在脚本中。

> 最新订阅链接需要添加查询参数 `&flag=clash` -- **2024/02/29** 更新

![配图](/upload/image-gxks.png)

然后在 `NAS` 的 控制面板 -> 任务计划

![配图](/upload/image-bdvt.png)

新增 -> 计划的任务 -> 用户定义的脚本

![配图](/upload/image-sszk.png)

修改计划执行时间为每天02:00执行

![配图](/upload/image-lkbs.png)

任务设置 -> 运行命令

`bash /volume1/docker/clash/auto-reload-clash.sh`

点击确定即可。可以右击刚刚创建的任务试运行看看。

至此 **NAS** 配置 clash 代理已全部完成。😋😋😋

> 服务器的将这些可视化界面改成命令即可。

在线web界面
clash-dashboard：[http://clash.razord.top/
yacd-dashboard：http://yacd.haishan.me/](http://clash.razord.top/)

```bash
docker run -d \
  --name clash \
  --restart always \
  --net=host \
  -v $PWD/docker/clash/config.yaml:/root/.config/clash/config.yaml \
 -v $PWD/docker/clash/ui:/ui \
 dreamacro/clash:latest
```

```bash
docker run --name yacd -p 1234:80 -d --rm haishanh/yacd
```

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
