# Nginx日志监控-Grafana+Loki+Promtail

> 标题：Nginx日志监控-Grafana+Loki+Promtail
> 分类：反代与网络
> 标签：docker、Linux、群晖、https、ubuntu
> 原文：https://www.xinz.fun/archives/Nginx-Grafana+Loki+Promtail

> **导读**：这篇围绕「Nginx日志监控-Grafana+Loki+Promtail」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾反代与网络的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 一、前言
2. 二、效果展示
3. 三、部署教程
4. 三、1 安装Nginx、GeoIP2
5. 三、2 下载IP地址定位数据库
6. 三、3 安装Nginx图形化管理工具——Nginx-UI
7. 三、4 配置nginx.conf日志格式
8. 三、5 安装Grafana+Loki+Promtail
9. 三、6 添加Nginx日志可视化仪表板
10. 四、进阶操作，自定义调整仪表板
11. 四、1 仪表板汉化
12. 四、2 新增城市访问记录查询模块
13. 以及其余 1 个小节

## 一、前言

以图形化方式展示通过Nginx反向代理服务访问我们服务器的客户端来源，便于直观判断服务器有没有被不速之客光顾过，也利于我们对自己部署的外网访问服务进行掌控。

## 二、效果展示

![配图](https://halo.cckyun.cn:49101/upload/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE(42)%20%E6%8B%B7%E8%B4%9D.png)

## 三、部署教程

本教程基于Debian 12系统编写，属于《基于Debian搭建HomeNAS》系列教程，其他系统可参考部署思路，不一定适用。

## 三、1 安装Nginx、GeoIP2

1、执行Nginx、GeoIP2安装命令：

```bash
apt install -y nginx libmaxminddb0 libmaxminddb-dev mmdb-bin libnginx-mod-http-geoip2
```

![配图](https://halo.cckyun.cn:49101/upload/image-mpyi.png)

2、验证是否已成功安装，执行命令：

```
01nginx -v
nginx -V 2>&1 | grep -o with-http_geoip_module
```

3、返回成功结果：

```
01nginx version: nginx/1.22.1
with-http_geoip_module
```

![配图](https://halo.cckyun.cn:49101/upload/image-zxhy.png)

## 三、2 下载IP地址定位数据库

1、GeoLite2是一个免费的IP地址定位数据库,用户可以免费地使用其中的数据。下载IP地址定位数据库文件需要登陆官网进行下载，没有账号的朋友需要先行注册账号。

> GeoLite2官网：
>
> https://www.maxmind.com/
>
> GeoLite2注册地址：
>
> https://www.maxmind.com/en/geolite2/signup
>
> 注册教程：
>
> http://modsecurity.cn/practice/post/15.html

2、登陆官网后，点击右下角的“Download Databases”

![配图](https://halo.cckyun.cn:49101/upload/image-jmqk.png)

3、下拉找到“GeoLite2 City”，点击“Download ZIP”下载。

![配图](https://halo.cckyun.cn:49101/upload/image-oarn.png)

4、将下载好的数据库文件压缩包解压，解压后得到“GeoLite2-City.mmdb”文件

![配图](https://halo.cckyun.cn:49101/upload/image-vobx.png)

5、将“GeoLite2-City.mmdb”文件上传至刚刚安装Nginx的服务器，存放在“/usr/share/GeoIP/”路径下。

![配图](https://halo.cckyun.cn:49101/upload/image-nzny.png)

6、验证地理数据库是否已生效，验证IP地址可以填写自己网络的IP地址。

```
mmdblookup --file /usr/share/GeoIP/GeoLite2-City.mmdb --ip 47.103.24.173
```

成功返回IP地址信息

![配图](https://halo.cckyun.cn:49101/upload/image-tyxg.png)

## 三、3 安装Nginx图形化管理工具——Nginx-UI

Nginx UI 是一个全新的 Nginx 网络管理界面，旨在简化 Nginx 服务器的管理和配置。它提供实时服务器统计数据、ChatGPT 助手、一键部署、Let's Encrypt 证书的自动续签以及用户友好的网站配置编辑工具。此外，Nginx UI 还提供了在线访问 Nginx 日志、配置文件的自动测试和重载、网络终端、深色模式和自适应网页设计等功能。Nginx UI 采用 Go 和 Vue 构建，确保在管理 Nginx 服务器时提供无缝高效的体验。

> 项目地址：https://github.com/0xJacky/nginx-ui/blob/dev/README-zh\_CN.md
>
> 项目官网：https://nginxui.com/zh\_CN/

1、一键安装脚本命令：

```bash
bash <(curl -L -s https://mirror.ghproxy.com/https://raw.githubusercontent.com/0xJacky/nginx-ui/master/install.sh) install -r https://mirror.ghproxy.com/
```

2、修改Nginx-UI默认端口

一键安装脚本默认设置的监听端口为 9000，HTTP Challenge 端口默认为 9180。如果有端口冲突，请手动修改 `/usr/local/etc/nginx-ui/app.ini` 配置文件， 并使用 `systemctl restart nginx-ui` 重启 Nginx UI 服务。没有端口冲突问题，则直接跳过此步骤。

![配图](https://halo.cckyun.cn:49101/upload/image-laab.png)

3、登陆使用Nginx-UI

第一次运行 Nginx UI 时，请在浏览器中访问 `http://<your_server_ip>:<listen_port>/install` 完成后续配置。邮箱地址必须真实有效，后期自动续签SSL证书需要用到。用户名及密码自定义，数据库项留空。

![配图](https://halo.cckyun.cn:49101/upload/image-baom.png)

## 三、4 配置nginx.conf日志格式

1、备份nginx.conf原始文件

```
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
```

2、修改nginx.conf文件日志格式

```
001002003004005006007008009010011012013014015016017018019020021022023024025026027028029030031032033034035036037038039040041042043044045046047048049050051052053054055056057058059060061062063064065066067068069070071072073074075076077078079080081082083084085086087088089090091092093094095096097098099100101102103104105106107108109110111112113114115116117118119120121122123124125126127128user www-data;
worker_processes auto;
pid /run/nginx.pid;
error_log /var/log/nginx/error.log;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 768;
    # multi_accept on;
}

http {

    ##
    # Basic Settings
    ##
    sendfile on;
    tcp_nopush on;
    types_hash_max_size 2048;
    # server_tokens off;

    # server_names_hash_bucket_size 64;
    # server_name_in_redirect off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ##
    # SSL Settings
    ##
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
    ssl_prefer_server_ciphers on;

    ##
    # Logging Settings start
    ##
    log_format json_analytics escape=json '{'
    '"msec": "$msec", '
    '"connection": "$connection", '
    '"connection_requests": "$connection_requests", '
    '"pid": "$pid", '
    '"request_id": "$request_id", '
    '"request_length": "$request_length", '
    '"remote_addr": "$remote_addr", '
    '"remote_user": "$remote_user", '
    '"remote_port": "$remote_port", '
    '"time_local": "$time_local", '
    '"time_iso8601": "$time_iso8601", '
    '"request": "$request", '
    '"request_uri": "$request_uri", '
    '"args": "$args", '
    '"status": "$status", '
    '"body_bytes_sent": "$body_bytes_sent", '
    '"bytes_sent": "$bytes_sent", '
    '"http_referer": "$http_referer", '
    '"http_user_agent": "$http_user_agent", '
    '"http_x_forwarded_for": "$http_x_forwarded_for", '
    '"http_host": "$http_host", '
    '"server_name": "$server_name", '
    '"request_time": "$request_time", '
    '"upstream": "$upstream_addr", '
    '"upstream_connect_time": "$upstream_connect_time", '
    '"upstream_header_time": "$upstream_header_time", '
    '"upstream_response_time": "$upstream_response_time", '
    '"upstream_response_length": "$upstream_response_length", '
    '"upstream_cache_status": "$upstream_cache_status", '
    '"ssl_protocol": "$ssl_protocol", '
    '"ssl_cipher": "$ssl_cipher", '
    '"scheme": "$scheme", '
    '"request_method": "$request_method", '
    '"server_protocol": "$server_protocol", '
    '"pipe": "$pipe", '
    '"gzip_ratio": "$gzip_ratio", '
    '"http_cf_ray": "$http_cf_ray",'
    '"geoip_country_code": "$geoip2_data_country_code", '
    '"geoip_country_name": "$geoip2_data_country_name", '
    '"geoip_city_name": "$geoip2_data_city_name"'
    '}';

    access_log /var/log/nginx/access.log json_analytics;

    geoip2 /usr/share/GeoIP/GeoLite2-City.mmdb {
        $geoip2_data_country_code country iso_code; #字符显示国家
        $geoip2_data_city_name city names zh-CN; #中文显示城市名
        $geoip2_data_country_name country names zh-CN; #中文显示国家名    
    }
    ##
    # Logging Settings end
    ##

    ##
    # Gzip Settings
    ##
    gzip on;

    # gzip_vary on;
    # gzip_proxied any;
    # gzip_comp_level 6;
    # gzip_buffers 16 8k;
    # gzip_http_version 1.1;
    # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    ##
    # Virtual Host Configs
    ##
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}

#mail {
#    # See sample authentication script at:
#    # http://wiki.nginx.org/ImapAuthenticateWithApachePhpScript
#
#    # auth_http localhost/auth.php;
#    # pop3_capabilities "TOP" "USER";
#    # imap_capabilities "IMAP4rev1" "UIDPLUS";
#
#    server {
#        listen     localhost:110;
#        protocol   pop3;
#        proxy      on;
#    }
#
#    server {
#        listen     localhost:143;
#        protocol   imap;
#        proxy      on;
#    }
#}
```

此次修改日志内容部分：

![配图](https://halo.cckyun.cn:49101/upload/image-fdwu.png)

## 三、5 安装Grafana+Loki+Promtail

Loki 是一个受Prometheus启发的水平可扩展、高可用性、多租户日志聚合系统。

> 项目地址：
>
> https://github.com/grafana/loki
>
> 项目文档：
>
> https://grafana.com/docs/loki/latest/setup/install/docker/

1、创建loki文件夹

```
01mkdir /opt/docker/loki
cd /opt/docker/loki
```

![配图](https://halo.cckyun.cn:49101/upload/image-ujlc.png)

2、下载loki-config.yaml和promtail-config.yaml

```
01wget https://mirror.ghproxy.com/https://raw.githubusercontent.com/grafana/loki/v3.0.0/cmd/loki/loki-local-config.yaml -O loki-config.yaml
wget https://mirror.ghproxy.com/https://raw.githubusercontent.com/grafana/loki/v3.0.0/clients/cmd/promtail/promtail-docker-config.yaml -O promtail-config.yaml
```

![配图](https://halo.cckyun.cn:49101/upload/image-yule.png)

3、创建docker-compose.yaml配置文件

```bash
vim docker-compose.yaml
```

4、粘贴docker-compose.yaml配置参数，有端口冲突请自行调整。如果你已经部署了grafana，则可以删除部署grafana部分配置，可以使用现有的。

```yaml
010203040506070809101112131415161718192021222324252627282930services:
  loki:
    image: grafana/loki:3.0.0
    container_name: loki
    volumes:
      - /opt/docker/loki:/mnt/config
    ports:
      - "3100:3100"
    command: -config.file=/mnt/config/loki-config.yaml
    restart: unless-stopped

  promtail:
    image: grafana/promtail:3.0.0
    container_name: promtail
    volumes:
      - /opt/docker/loki:/mnt/config
      - /var/log/nginx:/var/log
    depends_on:
      - loki
    command: -config.file=/mnt/config/promtail-config.yaml
    restart: unless-stopped

  grafana:
    image: grafana/grafana
    container_name: grafana
    user: root
    ports:
      - "3000:3000"
    volumes:
      - /opt/docker/loki/grafana:/var/lib/grafana
    restart: unless-stopped
```

5、启动容器

```bash
docker compose up -d
```

![配图](https://halo.cckyun.cn:49101/upload/image-nphn.png)

四、配置Grafana面板

1、浏览器打开`http://IP:3000`，访问Grafana。默认用户名及密码均为`admin`。

![配图](https://halo.cckyun.cn:49101/upload/image-fbfs.png)

2、登陆后提示设置新密码，自行设置任意数值密码。

![配图](https://halo.cckyun.cn:49101/upload/image-egsf.png)

3、设置Grafana面板为中文语言

点击右上角头像——选择Profile

![配图](https://halo.cckyun.cn:49101/upload/image-jhjt.png)

找到Language——选择中文（简体）——点击Save保存设置。

![配图](https://halo.cckyun.cn:49101/upload/image-zkyd.png)

## 三、6 添加Nginx日志可视化仪表板

1、添加loki数据源

点击连接——添加新连接——找到Loki

![配图](https://halo.cckyun.cn:49101/upload/image-nggb.png)

然后点击右上角“Add new data source”添加新的数据源

![配图](https://halo.cckyun.cn:49101/upload/image-tftb.png)

输入Loki的服务地址，格式为`http://IP:3100`，其他部分保存默认。

![配图](https://halo.cckyun.cn:49101/upload/image-xmpd.png)

然后下滑到最底部点击“Save & test”。

![配图](https://halo.cckyun.cn:49101/upload/image-math.png)

2、添加Nginx日志可视化仪表板

> 打开Loki NGINX Service Mesh - JSON version仪表板地址
> https://grafana.com/grafana/dashboards/12559-loki-nginx-service-mesh-json-version/

下滑页面找到Revisions，点击右侧`Download`下载第13项配置。（最新的第14项配置已经更新了数据源，与此次教程不匹配，无法使用。）

![配图](https://halo.cckyun.cn:49101/upload/image-adfx.png)

3、添加下载好的仪表板配置文件

点击仪表板——新建——导入

![配图](https://halo.cckyun.cn:49101/upload/image-xszk.png)

点击上传仪表板JSON文件

![配图](https://halo.cckyun.cn:49101/upload/image-smrt.png)

选择刚刚下载的仪表板配置文件上传。

![配图](https://halo.cckyun.cn:49101/upload/image-iegp.png)

点击Import导入配置。

![配图](https://halo.cckyun.cn:49101/upload/image-efkf.png)

至此仪表板配置完成。

![配图](https://halo.cckyun.cn:49101/upload/image-fpuk.png)

教程至此算是结束了，仪表板已经能成功展示Nginx日志的信息。如果需要将仪表板进行一些调整，比如翻译成中文，做一些自定义调整，请继续往下看。

## 四、进阶操作，自定义调整仪表板
## 四、1 仪表板汉化

选中你需要汉化的模块，点击右上角三个点——选择编辑

![配图](https://halo.cckyun.cn:49101/upload/image-gqfb.png)

在右侧编辑栏找到`Title`，然后输入该项目对应的中文名称，点击`Save`保存。其他模块的名称以此类推修改。

![配图](https://halo.cckyun.cn:49101/upload/image-wtxx.png)

## 四、2 新增城市访问记录查询模块

仪表板下滑找到`Top 10 visitor IPs`模块，然后复制一个新的模块出来进行修改。

![配图](https://halo.cckyun.cn:49101/upload/image-oufe.png)

修改`geoip_country_code`为`geoip_city_name`，其他部分保持默认。修改后完整参数如下：

```
topk(10, sum by (remote_addr, geoip_city_name) (count_over_time({$label_name=~"$label_value", job=~"$job", instance=~"$instance"} | json |  __error__="" [15m])))
```

然后修改左下角的`Options——Type`值为`Instant`。

![配图](https://halo.cckyun.cn:49101/upload/image-lgmy.png)

切换至Transform data选项，将小标题翻译成中文。

![配图](https://halo.cckyun.cn:49101/upload/image-lrrw.png)

修改完成后，点击右上角的`Save`保存设置。至此已成功添加城市访问记录查询模块。

![配图](https://halo.cckyun.cn:49101/upload/image-ozng.png)

更多自定义选项以此类推自行摸索，或进Debian HomeNAS的QQ群交流。

## 结语

至此部署教程已经结束，创作不易，转载请注明出处。

转载至:东方未明

DIY NAS\_1群 874649129

DIY NAS\_2群 772356359

DIY NAS\_3群 339169752

祝大家玩机愉快！
