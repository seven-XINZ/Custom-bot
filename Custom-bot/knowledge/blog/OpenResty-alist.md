# OpenResty修复alist上传下载文件过大报错

> 标题：OpenResty修复alist上传下载文件过大报错
> 分类：反代与网络
> 标签：alist
> 原文：https://www.xinz.fun/archives/OpenResty-alist

> **导读**：这篇记录「OpenResty修复alist上传下载文件过大报错」的排查与处理过程。先说明问题现象，再给出配置或命令，最后补充验证方法；遇到相似报错时可按顺序对照。
>
> 适合正在折腾反代与网络的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 前情提要
2. 一、打开1panel管理面板找到网站进去
3. 二、选中自己的alist域名 点击后方的配置
4. 三、进入配置点击配置文件
5. 四、更改前先看好我打码地方的配置自己保存好等会儿需要使用
6. 五、保留好你原本的配置万一有问题好还原 备份好后直接改好下方代码替换原来的代码
7. 示例配置代码
8. 配置说明

## 前情提要

**如果alist上传报错请按照下方步骤操作**

## 一、打开1panel管理面板找到网站进去

![配图](/upload/image-kvwp.png)

## 二、选中自己的alist域名 点击后方的配置

![配图](/upload/image-imlo.png)

## 三、进入配置点击配置文件

![配图](/upload/image-riyp.png)

## 四、更改前先看好我打码地方的配置自己保存好等会儿需要使用

![配图](/upload/image-czeh.png)

## 五、保留好你原本的配置万一有问题好还原 备份好后直接改好下方代码替换原来的代码

**自己的域名**

![配图](/upload/image-nkej.png)

自己的域名路径

![配图](/upload/image-tgkk.png)

![配图](/upload/image-xqhl.png)

```
 server_name 自己的域名;
```

```
access_log /www/sites/自己的域名/log/access.log main; 
    error_log /www/sites/自己的域名/log/error.log;
```

```
 ssl_certificate /www/sites/自己的证书地址/ssl/fullchain.pem; 
    ssl_certificate_key /www/sites/自己的证书地址/ssl/privkey.pem;
```

**改好复制代码替换正常来讲无需更改其他**

## 示例配置代码

> **注意**：下面的配置请先看懂再替换，改之前务必备份原文件。

```nginx
server {
    listen 8080; 
    listen [::]:8080; 
    listen 4443 ssl http2; 
    listen [::]:4443 ssl http2; 
    server_name 自己的域名; 
    index index.php index.html index.htm default.php default.htm default.html; 

    client_max_body_size 0;  # 不限制上传大小

    proxy_set_header Host $host; 
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; 
    proxy_set_header X-Forwarded-Host $server_name; 
    proxy_set_header X-Real-IP $remote_addr; 
    proxy_http_version 1.1; 
    proxy_set_header Upgrade $http_upgrade; 
    proxy_set_header Connection $http_connection; 

    access_log /www/sites/自己的域名/log/access.log main; 
    error_log /www/sites/自己的域名/log/error.log; 

    location ^~ /.well-known/acme-challenge {
        allow all; 
        root /usr/share/nginx/html; 
    }

    include /www/sites/al.xinz.fun/proxy/*.conf; 

    if ($scheme = http) {
        return 301 https://$host$request_uri; 
    }

    ssl_certificate /www/sites/自己的证书地址/ssl/fullchain.pem; 
    ssl_certificate_key /www/sites/自己的证书地址/ssl/privkey.pem; 
    ssl_protocols TLSv1.3 TLSv1.2 TLSv1.1 TLSv1; 
    ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256:!aNULL:!eNULL:!EXPORT:!DSS:!DES:!RC4:!3DES:!MD5:!PSK:!KRB5:!SRP:!CAMELLIA:!SEED; 
    ssl_prefer_server_ciphers on; 
    ssl_session_cache shared:SSL:10m; 
    ssl_session_timeout 10m; 
    error_page 497 https://$host$request_uri; 
    proxy_set_header X-Forwarded-Proto https; 
    add_header Strict-Transport-Security "max-age=31536000"; 

    location ~ .*\.(js|css|png|jpg|jpeg|gif|ico|bmp|swf|eot|svg|ttf|woff|woff2)$ {
        expires 30d; 
        log_not_found off; 
        valid_referers none al.xinz.fun; 
        if ($invalid_referer) {
            return 404; 
            access_log off; 
        }
    }

    # 代理缓冲设置
    proxy_buffer_size 128k;
    proxy_buffers 4 256k;
    proxy_busy_buffers_size 256k;
    
    # 设置临时文件写入大小
    proxy_temp_file_write_size 512k;  # 设置为大于256k
}
```

## 配置说明

```nginx
server {
    listen 8080;  # 监听 8080 端口（HTTP）
    listen [::]:8080;  # 监听 IPv6 的 8080 端口
    listen 4443 ssl http2;  # 监听 4443 端口（HTTPS，支持 HTTP/2）
    listen [::]:4443 ssl http2;  # 监听 IPv6 的 4443 端口（HTTPS，支持 HTTP/2）
    
    server_name 自己的域名;  # 设置服务器的域名（替换为您的域名）
    
    index index.php index.html index.htm default.php default.htm default.html;  # 默认文档列表

    client_max_body_size 0;  # 不限制上传文件的大小

    # 设置转发头部，确保代理请求中的信息
    proxy_set_header Host $host;  # 将主机头设置为请求中的主机
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  # 添加客户端 IP 到转发头
    proxy_set_header X-Forwarded-Host $server_name;  # 设置转发的主机头
    proxy_set_header X-Real-IP $remote_addr;  # 将真实 IP 设置为远程地址
    proxy_http_version 1.1;  # 设置代理使用的 HTTP 版本
    proxy_set_header Upgrade $http_upgrade;  # 支持 WebSocket 升级
    proxy_set_header Connection $http_connection;  # 设置连接头

    access_log /www/sites/自己的域名/log/access.log main;  # 设置访问日志路径
    error_log /www/sites/自己的域名/log/error.log;  # 设置错误日志路径

    location ^~ /.well-known/acme-challenge {
        allow all;  # 允许所有访问
        root /usr/share/nginx/html;  # 设置根目录以处理 Let's Encrypt 验证
    }

    include /www/sites/al.xinz.fun/proxy/*.conf;  # 引入其他配置文件

    if ($scheme = http) {
        return 301 https://$host$request_uri;  # 强制 HTTP 重定向到 HTTPS
    }

    ssl_certificate /www/sites/自己的证书地址/ssl/fullchain.pem;  # SSL 证书路径
    ssl_certificate_key /www/sites/自己的证书地址/ssl/privkey.pem;  # SSL 证书密钥路径
    ssl_protocols TLSv1.3 TLSv1.2 TLSv1.1 TLSv1;  # 启用的 SSL/TLS 协议
    ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256:!aNULL:!eNULL:!EXPORT:!DSS:!DES:!RC4:!3DES:!MD5:!PSK:!KRB5:!SRP:!CAMELLIA:!SEED;  # SSL 加密套件
    ssl_prefer_server_ciphers on;  # 优先使用服务器的加密套件
    ssl_session_cache shared:SSL:10m;  # SSL 会话缓存设置
    ssl_session_timeout 10m;  # SSL 会话超时时间
    error_page 497 https://$host$request_uri;  # 处理 HTTP to HTTPS 的错误页面
    proxy_set_header X-Forwarded-Proto https;  # 设置转发协议为 HTTPS
    add_header Strict-Transport-Security "max-age=31536000";  # 启用 HSTS，设置最大生存时间为一年

    location ~ .*\.(js|css|png|jpg|jpeg|gif|ico|bmp|swf|eot|svg|ttf|woff|woff2)$ {
        expires 30d;  # 设置静态文件的过期时间为 30 天
        log_not_found off;  # 关闭未找到文件的日志
        valid_referers none al.xinz.fun;  # 允许的引荐来源
        if ($invalid_referer) {
            return 404;  # 如果来源无效，返回 404
            access_log off;  # 关闭访问日志
        }
    }

    # 代理缓冲设置
    proxy_buffer_size 128k;  # 设置单个缓冲区的大小
    proxy_buffers 4 256k;  # 设置缓冲区的数量和大小
    proxy_busy_buffers_size 256k;  # 设置繁忙缓冲区的大小
    
    # 设置临时文件写入大小
    proxy_temp_file_write_size 512k;  # 设置为大于256k，以满足配置要求
}
```

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
