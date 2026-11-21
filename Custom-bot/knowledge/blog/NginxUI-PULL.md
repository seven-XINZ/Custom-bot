# 反向代理新选择Nginx UI安装使用教程

> 标题：反向代理新选择Nginx UI安装使用教程
> 分类：反代与网络
> 标签：docker、Linux、v2ray、nas、群晖、https、ubuntu
> 原文：https://www.xinz.fun/archives/NginxUI-PULL

> **导读**：这篇是「反向代理新选择Nginx UI安装使用教程」的实操教程。下文按「前言」「一、安装」「一、1 通过Docker Compose安装」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾反代与网络的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 前言
2. 一、安装
3. 一、1 通过Docker Compose安装
4. docker命令安装
5. 一、2 通过自动化脚本安装
6. 二、使用
7. 二、1 初始化配置
8. 配图
9. 二、3 申请泛域名证书
10. 二、4 配置反向代理
11. 三、自定义优化（可选）
12. 三、1、nginx.conf配置文件优化
13. 以及其余 1 个小节

## 前言

Nginx UI 是一个全新的 Nginx 网络管理界面，旨在简化 Nginx 服务器的管理和配置。它提供实时服务器统计数据、ChatGPT 助手、一键部署、Let's Encrypt 证书的自动续签以及用户友好的网站配置编辑工具。此外，Nginx UI 还提供了在线访问 Nginx 日志、配置文件的自动测试和重载、网络终端、深色模式和自适应网页设计等功能。Nginx UI 采用 Go 和 Vue 构建，确保在管理 Nginx 服务器时提供无缝高效的体验。

> 官网：https://nginxui.com/zh\_CN/
>
> 项目地址：https://github.com/0xJacky/nginx-ui

本教程仅针对家庭NAS用户做个简单配置使用教程。

## 一、安装
## 一、1 通过Docker Compose安装

创建docker-compose.yaml文件

```yaml
0102030405060708091011121314151617version: '3.3'
services:
    nginx-ui:
        stdin_open: true
        tty: true
        container_name: nginx-ui
        restart: always
        environment:
            - TZ=Asia/Shanghai
        volumes:
            - '/opt/docker/nginx-ui/nginx:/etc/nginx'
            - '/opt/docker/nginx-ui/ui:/etc/nginx-ui'
            - '/opt/docker/nginx-ui/logs:/var/log/nginx'
            - '/opt/docker/nginx-ui/www:/var/www'
        ports:
            - 8080:80
            - 8443:443
        image: 'uozi/nginx-ui:latest'
```

启动容器

```bash
docker compose up -d
```

## docker命令安装

```bash
docker run -dit \
  --name=nginx-ui \
  --restart=always \
  -e TZ=Asia/Shanghai \
  -v /mnt/user/appdata/nginx:/etc/nginx \
  -v /mnt/user/appdata/nginx-ui:/etc/nginx-ui \
  -v /var/www:/var/www \
  -p 80:80 -p 443:443 \
  uozi/nginx-ui:latest
```

在这个示例中，容器的80端口和443端口分别映射到主机的8080端口和8443端口。 您需要访问`http://<your_server_ip>:8080`来访问 Nginx UI。通过docker方式安装的nginx-ui自带nginx，可以直接使用。

## 一、2 通过自动化脚本安装

此 shell 脚本仅适用于 Linux 系统。如果您使用的是其他操作系统，请参考官网快速入门指南进行手动安装或使用 Docker。

```bash
bash <(curl -L -s https://mirror.ghproxy.com/https://raw.githubusercontent.com/0xJacky/nginx-ui/master/install.sh) install -r https://mirror.ghproxy.com/
```

一键安装脚本默认设置的监听端口为 9000，HTTP Challenge 端口默认为 9180。如果有端口冲突，请手动修改 `/usr/local/etc/nginx-ui/app.ini`， 并使用 `systemctl restart nginx-ui` 重启 Nginx UI 服务。更多有关信息，请查看官网配置参考。

## 二、使用
## 二、1 初始化配置

通过`http://<your_server_ip>:8080`来访问 Nginx UI，首次访问，需要填写有效信息自助注册管理账号。

**1、邮箱地址必须真实有效，后面申请SSL证书需要用到。**

**2、用户名和密码自定义，建议使用高强度密码。**

**3、数据库部分保持默认留空。**

## 配图

**2.2 配置申请SSL证书信息**

这里以域名托管在腾讯云DNSpod.cn为例，其他域名托管平台道理一样。

1、打开下面地址，登陆你的域名管理账号创建API访问密钥。

> 创建API访问密钥地址：
>
> https://console.cloud.tencent.com/cam/capi

2、登陆后点击API密钥管理——新建密钥

![配图](https://halo.cckyun.cn:49101/upload/image-uvav.png)

3、拿个小本子记录好这个`SecretId`和`Secretkey`信息，只显示一次的。

![配图](https://halo.cckyun.cn:49101/upload/image-snli.png)

4、回到Nginx-UI管理界面，点击证书——DNS凭证——添加——选择DNS 提供商（Tencent Cloud DNS）——填写刚刚创建的`SecretId`和`Secretkey`信息，其余部分内容不懂则保持默认留空，下滑到底部点击确定保存。

![配图](https://halo.cckyun.cn:49101/upload/image-msfg.png)

## 二、3 申请泛域名证书

如果您不需要申请泛域名证书，请跳过此步骤。

在Nginx-UI面板，点击证书——证书列表——签发通配符证书——填写你的域名——ACME 用户（System Initial User）——DNS 提供商（Tencent Cloud DNS）——DNS凭证（在2.2节创建的）

![配图](https://halo.cckyun.cn:49101/upload/image-qpzd.png)

信息填写完成后，点击下一步程序将开始泛域名证书申请操作。

![配图](https://halo.cckyun.cn:49101/upload/image-epim.png)

## 二、4 配置反向代理

1、点击网站管理——添加站点——配置名称（可以任意设置，方便管理就行）——输入`server_name`（你的域名）——然后点击下一步。只需要填写配置名称和`server_name`，其他地方保存默认。

![配图](https://halo.cckyun.cn:49101/upload/image-exvm.png)

2、点击启用TLS

![配图](https://halo.cckyun.cn:49101/upload/image-uwgi.png)

3、然后删除server1，因为server1是http，这里我们不需要。

![配图](https://halo.cckyun.cn:49101/upload/image-fgfe.png)

3、选择SSL证书

如果你使用的是泛域名证书，点击更改证书，然后选择前面提前申请好的泛域名证书就可以了。

![配图](https://halo.cckyun.cn:49101/upload/image-zlzq.png)

如果不使用泛域名证书，则点击启用 Let's Encrypt 对网站进行加密。

![配图](https://halo.cckyun.cn:49101/upload/image-sply.png)

在弹出的获取证书界面选择你的DNS凭证，点击下一步就可以了。

![配图](https://halo.cckyun.cn:49101/upload/image-kcya.png)

4、证书配置完成后，在配置项下滑找到反向代理配置，点击查看

![配图](https://halo.cckyun.cn:49101/upload/image-odyk.png)

下滑找到`Locations`，点击展开内容。修改下面两项内容：

`client_max_body_size`这项设置作用是限制上传到服务器的文件大小，如果反代的服务是文件存储服务，比如群晖的DSM，那么这项值就建议设置大一点，或者设置为0m，0表示不限制。如果反代的服务不需要上传任何文件到服务器的，比如emby影视服务，则可以设置小一点，设置16m。所以日常建议就是在两个值之间设置，0m或16m。

```
client_max_body_size 1000m;
```

`proxy_pass`填写需要反代的服务地址。比如emby影视服务，这里就设置为`proxy_pass http://127.0.0.1:8096/;`

```nginx
proxy_pass http://127.0.0.1:9000/;
```

![配图](https://halo.cckyun.cn:49101/upload/image-pbti.png)

其余选项保持默认，修改完成后点击添加即可完成反向代理设置，之后点击下一步，完成全部设置。

![配图](https://halo.cckyun.cn:49101/upload/image-vonn.png)

至此你已经成功设置一个服务的反向代理操作。只需要配置好第一个服务，后面需要增加反代其他服务，可以直接通过站点列表复制反代配置，然后修改被反代服务的内网地址就可以了。

![配图](https://halo.cckyun.cn:49101/upload/image-rnfv.png)

## 三、自定义优化（可选）

因知识水平有限，自定义优化配置只代表个人观点，仅供参考。如有更好的优化意见，欢迎反馈。

自定义优化配置主要侧重安全防护，能提高一点点安全性吧。

## 三、1、nginx.conf配置文件优化

此部分无需修改任何内容，直接复制粘贴替换原有的`nginx.conf`配置内容即可。替换前记得先备份原始配置文件，防止出错需要回退。

**nginx.conf配置文件**

```
001002003004005006007008009010011012013014015016017018019020021022023024025026027028029030031032033034035036037038039040041042043044045046047048049050051052053054055056057058059060061062063064065066067068069070071072073074075076077078079080081082083084085086087088089090091092093094095096097098099100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158159160161162163164165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197# 设置Nginx工作进程的用户为nginx
user nginx;

# 定义错误日志文件路径，日志级别为notice
error_log /var/log/nginx/error.log notice;
# 定义本地错误日志文件路径，日志级别为notice
error_log /var/log/nginx/error.local.log notice;

# 设置保存Nginx进程ID的文件路径
pid /run/nginx.pid;

# 设置工作进程数量为自动，根据CPU核心数动态调整
worker_processes auto;

# 设置每个工作进程的最大打开文件数为65535
worker_rlimit_nofile 65535;

events {
    # 启用multi_accept，允许一个事件循环中同时接受多个新连接
    multi_accept on;
    
    # 设置每个工作进程的最大并发连接数为1024
    worker_connections 1024;
}

http {
    # 设置默认字符集为UTF-8
    charset utf-8;

    # 启用sendfile系统调用，提高文件传输效率
    sendfile on;

    # 启用TCP_NOPUSH选项，减少网络包的发送数量
    tcp_nopush on;

    # 启用TCP_NODELAY选项，避免Nagle算法延迟小数据包的发送
    tcp_nodelay on;

    # 隐藏Nginx版本信息，增强安全性
    server_tokens off;

    # 禁用记录404错误日志
    log_not_found off;

    # 设置MIME类型哈希表的最大大小为2048
    types_hash_max_size 2048;

    # 设置MIME类型哈希表的桶大小为64
    types_hash_bucket_size 64;

    # 禁用代理请求缓冲
    proxy_request_buffering off;

    # 禁用FastCGI请求缓冲
    fastcgi_request_buffering off;

    # 禁用SCGI请求缓冲
    scgi_request_buffering off;

    # 禁用代理响应缓冲
    proxy_buffering off;

    # 禁用FastCGI响应缓冲
    fastcgi_buffering off;

    # 禁用SCGI响应缓冲
    scgi_buffering off;

    # 设置DNS解析超时时间为5秒
    resolver_timeout 5s;

    # 设置客户端请求头的超时时间为10秒
    client_header_timeout 10s;

    # 设置客户端请求体的超时时间为60秒
    client_body_timeout 60s;

    # 设置响应发送超时时间为60秒
    send_timeout 60s;

    # 设置长连接超时时间，65秒后断开客户端，20秒后断开代理服务器
    keepalive_timeout 65s 20s;

    # 设置客户端请求体的最大大小为16MB
    client_max_body_size 16m;

    # 设置服务器名称哈希表的最大大小为8192
    server_names_hash_max_size 8192;

    # 设置服务器名称哈希表的桶大小为128
    server_names_hash_bucket_size 128;

    # 包含MIME类型定义文件
    include /etc/nginx/mime.types;

    # 设置默认的MIME类型为application/octet-stream
    default_type application/octet-stream;

    # 定义日志格式为main
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                     '$status $body_bytes_sent "$http_referer" '
                     '"$http_user_agent" "$http_x_forwarded_for"';

    # 定义访问日志文件路径，使用main格式
    access_log /var/log/nginx/access.log main;

    # 定义本地访问日志文件路径，使用main格式
    access_log /var/log/nginx/access.local.log main;

    # 设置SSL会话超时时间为3600秒
    ssl_session_timeout 3600s;

    # 设置SSL会话缓存大小为1MB
    ssl_session_cache shared:SSL:1m;

    # 禁用SSL会话票据
    ssl_session_tickets off;

    # 设置获取真实客户端IP的头部字段为X-Forwarded-For
    real_ip_header X-Forwarded-For;

    # 启用递归解析X-Forwarded-For头部，获取最后一个IP
    real_ip_recursive on;

    # 设置信任的IP地址来源为127.0.0.1
    set_real_ip_from 127.0.0.1;

    # 仅启用TLS 1.2和TLS 1.3协议
    ssl_protocols TLSv1.2 TLSv1.3;

    # 设置SSL加密套件
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:
                 ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:
                 ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:
                 DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;

    # 启用SSL证书OCSP Stapling
    ssl_stapling on;

    # 启用OCSP响应验证
    ssl_stapling_verify on;

    # 默认情况下，设置Connection头部为upgrade
    map $http_upgrade $connection_upgrade {
        default upgrade;
        # 如果没有升级请求，则关闭连接
        "" close;
    }

    # 对IPv4地址设置X-Forwarded-For头部格式
    map $remote_addr $proxy_forwarded_elem {
        ~^[0-9.]+$ "for=$remote_addr";
        # 对IPv6地址设置X-Forwarded-For头部格式
        ~^[0-9A-Fa-f:.]+$ "for=\"[$remote_addr]\"";
        # 默认设置X-Forwarded-For头部为unknown
        default "for=unknown";
    }

    # 根据现有Forwarded头部内容添加自定义Forwarded头部信息
    map $http_forwarded $proxy_add_forwarded {
        "~^(,[ \\t]*)*([!#$%&'*+.^_`|~0-9A-Za-z-]+=([!#$%&'*+.^_`|~0-9A-Za-z-]+|\"([\\t \\x21\\x23-\\x5B\\x5D-\\x7E\\x80-\\xFF]|\\\\[\\t \\x21-\\x7E\\x80-\\xFF])*\"))?(;([!#$%&'*+.^_`|~0-9A-Za-z-]+=([!#$%&'*+.^_`|~0-9A-Za-z-]+|\"([\\t \\x21\\x23-\\x5B\\x5D-\\x7E\\x80-\\xFF]|\\\\[\\t \\x21-\\x7E\\x80-\\xFF])*\"))?)*([ \\t]*,([ \\t]*([!#$%&'*+.^_`|~0-9A-Za-z-]+=([!#$%&'*+.^_`|~0-9A-Za-z-]+|\"([\\t \\x21\\x23-\\x5B\\x5D-\\x7E\\x80-\\xFF]|\\\\[\\t \\x21-\\x7E\\x80-\\xFF])*\"))?(;([!#$%&'*+.^_`|~0-9A-Za-z-]+=([!#$%&'*+.^_`|~0-9A-Za-z-]+|\"([\\t \\x21\\x23-\\x5B\\x5D-\\x7E\\x80-\\xFF]|\\\\[\\t \\x21-\\x7E\\x80-\\xFF])*\"))?)*)?)*$" "$http_forwarded, $proxy_forwarded_elem";
        # 默认情况下仅使用proxy_forwarded_elem
        default "$proxy_forwarded_elem";
    }

    # 禁用对MSIE 6浏览器的Gzip压缩
    gzip_disable "msie6";

    # 设置启用Gzip压缩的最小响应体大小为1000字节
    gzip_min_length 1000;

    # 定义启用Gzip压缩的MIME类型
    gzip_types text/plain text/css text/xml application/json application/javascript application/rss+xml application/atom+xml image/svg+xml;

    # 启用Vary: Accept-Encoding头部，以便根据客户端支持情况发送Gzip压缩内容
    gzip_vary on;

    # 启用静态Gzip压缩文件支持
    gzip_static on;

    # 设置打开文件缓存，最多缓存1000个文件，60秒不活动后移除缓存
    open_file_cache max=1000 inactive=60s;

    # 设置缓存文件的有效期为3秒
    open_file_cache_valid 3s;

    # 设置文件至少被使用2次才会被缓存
    open_file_cache_min_uses 2;

    # 缓存打开文件时发生的错误
    open_file_cache_errors on;

    # 包含conf.d目录下的所有配置文件
    include /etc/nginx/conf.d/*.conf;

    # 包含sites-enabled目录下的所有配置文件
    include /etc/nginx/sites-enabled/*;
}
```

点击配置管理——找到`nginx.conf`，点击修改，复制粘贴替换原有的配置内容即可。

## 配图3.2、server模块配置优化

使用此`server`模块配置内容替换原有的，需要修改的地方有以下四个位置。

1、修改`server_name`，`server_name`是定义你外网访问域名的设置。

```
01    # 定义服务器名称为jellyfin.baidu.com
    server_name jellyfin.baidu.com;
```

2、修改SSL证书文件路径。证书可以通过面板的基本模式——修改证书进行路径设置。

```
010203    # 指定SSL证书文件路径
    ssl_certificate /etc/nginx/ssl/*.baidu.com_2048/fullchain.cer;
    # 指定SSL证书密钥文件路径
    ssl_certificate_key /etc/nginx/ssl/*.baidu.com_2048/private.key;
```

![配图](https://halo.cckyun.cn:49101/upload/image-esbz.png)

还可以在面板的证书——证书列表——选中需要查询的证书——点击修改——下滑即可找到证书路径。

![配图](https://halo.cckyun.cn:49101/upload/image-yetg.png)

3、设置客户端请求体的最大大小。client\_max\_body\_size的作用前面2.4小节已经描述过，如果你还是无法判断该设置多少，就先保持默认，如果后续访问出现问题，再调整为0即可。

```
01        # 设置客户端请求体的最大大小为16MB
        client_max_body_size 16m;
```

4、设置内网需要反向代理的服务地址。比如需要反代Emby服务，就修改IP地址为Emby的，如下所示。其他服务也是如此。

```nginx
01        # 设置内网需要反向代理的服务地址
        proxy_pass http://192.168.8.11:8096/;
```

5、其他部分内容无需修改，完成保持默认值即可。

**server模块配置文件**

```nginx
0102030405060708091011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980818283848586878889909192939495server {
    # 监听443端口，启用SSL
    listen 443 ssl;
    # 监听IPv6地址的443端口，启用SSL
    listen [::]:443 ssl;
    # 定义服务器名称为jellyfin.baidu.com
    server_name jellyfin.baidu.com;
    # 指定SSL证书文件路径
    ssl_certificate /etc/nginx/ssl/*.baidu.com_2048/fullchain.cer;
    # 指定SSL证书密钥文件路径
    ssl_certificate_key /etc/nginx/ssl/*.baidu.com_2048/private.key;
    
    # 允许无效的HTTP头部
    ignore_invalid_headers off;

    # 添加严格传输安全头部，启用子域名，缓存期限为1年
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # 添加XSS保护头部，启用阻止模式
    add_header X-XSS-Protection "1; mode=block" always;
    
    # 添加内容类型选项头部，防止MIME类型嗅探
    add_header X-Content-Type-Options "nosniff" always;
    
    # 添加引用者策略头部，设置为在降级时不发送引荐来源
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # 添加内容安全策略头部，限制资源加载来源
    add_header Content-Security-Policy "default-src 'self' http: https: ws: wss: data: blob: 'unsafe-inline'; frame-ancestors 'self';" always;
    
    # 添加权限策略头部，禁用兴趣小组（如FLoC）
    add_header Permissions-Policy "interest-cohort=()" always;
    
    # 添加X-Frame-Options头部，防止点击劫持，设置为同源
    add_header X-Frame-Options "SAMEORIGIN";

    location /.well-known/acme-challenge {
        # 设置Host头部为请求的主机名
        proxy_set_header Host $host;
        # 设置X-Real-IP头部为客户端的真实IP地址
        proxy_set_header X-Real-IP $remote_addr;
        # 设置X-Forwarded-For头部为客户端的真实IP和端口
        proxy_set_header X-Forwarded-For $remote_addr:$remote_port;
        # 将请求代理到本地127.0.0.1:9180
        proxy_pass http://127.0.0.1:9180;
    }

    location ~ ((^|/)\.|^.*\.yml$|^/sites/.*/private/|^/sites/[^/]+/[^/]*settings.*\.php$) {
        # 匹配隐藏文件、YAML文件、私有目录、以及某些PHP文件，返回444状态码
        return 444;
    }

    location ~ ^/sites/[^/]+/files/.*\.php$ {
        # 匹配特定目录下的PHP文件，返回444状态码
        return 444;
    }

    location ~ /vendor/.*\.php$ {
        # 匹配vendor目录下的PHP文件，返回444状态码
        return 444;
    }

    location ~* /(images|cache|media|logs|tmp)/.*\.(gz|tar|bzip2|7z|php|php5|php7|log|error|py|pl|kid|love|cgi|shtml|phps|pht|jsp|asp|sh|bash)$ {
        # 匹配特定目录下的危险文件类型，返回444状态码
        return 444;
    }

    location / {
        # 检查请求的Host头部是否与服务器名称匹配，如果不匹配则返回404状态码
        if ($host != $server_name) {
            return 404;
        }

        # 设置代理使用的HTTP版本为1.1
        proxy_http_version 1.1;
        # 设置Upgrade头部为客户端请求的Upgrade头部
        proxy_set_header Upgrade $http_upgrade;
        # 设置Connection头部为客户端请求的Connection头部
        proxy_set_header Connection $connection_upgrade;
        # 设置客户端请求体的最大大小为16MB
        client_max_body_size 16m;
        # 禁用代理重定向
        proxy_redirect off;
        # 设置Host头部为请求的主机名
        proxy_set_header Host $host;
        # 设置X-Real-IP头部为客户端的真实IP地址
        proxy_set_header X-Real-IP $remote_addr;
        # 设置X-Forwarded-For头部为客户端的转发链
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        # 设置X-Forwarded-Proto头部为请求的协议（HTTP或HTTPS）
        proxy_set_header X-Forwarded-Proto $scheme;
        # 设置内网需要反向代理的服务地址
        proxy_pass http://192.168.8.11:8096/;
    }
}
```

教程到此结束。

本文转载自:[东方末明](点击链接加入群聊【DIY NAS_2群(Debian/群晖/unRaid/PVE/Esxi)】：https://qm.qq.com/q/9b0JARPuH6)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
