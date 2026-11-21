# 如何搭建一个短网址平台 — YOURLS

> 标题：如何搭建一个短网址平台 — YOURLS
> 分类：面板与工具
> 标签：无
> 原文：https://www.xinz.fun/archives/如何搭建一个短网址平台 — YOURLS

> **导读**：这篇是「如何搭建一个短网址平台 — YOURLS」的实操教程。下文按「实际步骤」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾面板与工具的读者。执行前建议先备份原配置，并在测试环境验证。

### 效果图：

![配图](https://pic.imgdb.cn/item/64cbc5c91ddac507ccb096e4.jpg)

### 缺点：

适合自用，只能在配置文件中手动添加管理员，无法在前端直接添加。

### 部署方法：
#### 第一步：更新源并安装依赖

**Ubuntu/Debian：**

bash

```bash
010203apt update -y && apt upgrade -y
sudo apt install unzip -y  
sudo apt install git -y
```

**Centos：**

bash

```bash
010203sudo yum update -y && sudo yum upgrade -y
sudo yum install unzip -y
sudo yum install git -y
```

#### 第二步：安装 Apache Web

**Ubuntu/Debian：**

bash

```bash
01sudo apt-get install apache2
```

**Centos：**

bash

```
01sudo yum install httpd -y
```

#### 第三步：安装 MySQL

**Ubuntu**

bash

```bash
01sudo apt-get install mysql-server
```

**Debian：**

bash

```bash
01sudo apt-get install mariadb-server
```

**Centos：**

bash

```
0102sudo yum install mysql-server -y
sudo systemctl start mysqld
```

#### 第四步：安装PHP及所需拓展

**Ubuntu/Debian：**

bash

```bash
01sudo apt-get install php php-mysql libapache2-mod-php php-cli
```

**Centos：**

bash

```
0102sudo yum install php php-mysql php-cli
sudo systemctl restart httpd
```

#### 第五步：配置数据库

1. 进入 MySQL

bash

```
01mysql -u root -p
```

输入密码为root密码
2. 创建数据库

bash

```
01CREATE DATABASE yourls;
```

3. 创建用户并授权

bash

```
0102CREATE USER 'yourls_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON yourls.* TO 'yourls_user'@'localhost';
```

4. 重启并退出

bash

```
0102FLUSH PRIVILEGES;
EXIT;
```

#### 第六步：下载源代码并解压

bash

```
0102wget https://github.com/YOURLS/YOURLS/archive/refs/tags/1.9.2.zip
unzip 1.9.2.zip
```

#### 第七步：配置YOURLS

1. 复制示例配置文件：

bash

```
01cp YOURLS-1.9.2/user/config-sample.php YOURLS-1.9.2/user/config.php
```

2. 打开配置文件并进行修改：

bash

```
01nano YOURLS-1.9.2/user/config.php
```

**对以下内容必须进行修改：**

1. 数据库用户名：

php

```
01define( 'YOURLS_DB_USER', 'yourls_user' );
```

2. 数据库密码：

php

```
01define( 'YOURLS_DB_PASS', 'password' );
```

3. 数据库名：

php

```
01define( 'YOURLS_DB_NAME', 'yourls' );
```

4. COOKIEKEY（在http://[yourls.org/cookie中生成）：](http://yourls.org/cookie中生成）：)

php

```
01define( 'YOURLS_COOKIEKEY', 'modify this text with something random' );
```

5. 管理员用户名及密码（若不进行修改管理员用户名即为username，密码即为password，可在此处添加多个用户进行管理）：

php

```
0102030405$yourls_user_passwords = [
    'username' => 'password',
    // 'username2' => 'password2',
    // You can have one or more 'login'=>'password' lines
];
```

6. 访问网址（记得将这个网址解析到主机IP）：

php

```
01define( 'YOURLS_SITE', 'http://example.com' );
```

**对以下内容选择性进行修改：**

1. 是否允许公众使用（填true为不允许，false为允许）：

php

```
01define( 'YOURLS_PRIVATE', true );
```

2. 是否允许多个短链接指向同一个长链接（举例，[允许后访问a.com/1和a.com/2同时都会跳转b.com，可以分析每个短链接的数据，在多平台推广的时候很有用](http://允许后访问a.com/1和a.com/2同时都会跳转b.com，可以分析每个短链接的数据，在多平台推广的时候很有用) ）

php

```
01define( 'YOURLS_UNIQUE_URLS', true );
```

3. 是否更改语言（默认为英文，改为中文版本则填写'zh\_CN'，后续要进行进一步配置）：

php

```
01define( 'YOURLS_LANG', '' );
```

4. 排除哪些敏感词汇（包含填写的敏感词的长地址不会被缩短）：

php

```
010203$yourls_reserved_URL = [
    'porn', 'faggot', 'sex', 'nigger', 'fuck', 'cunt', 'dick',
];
```

#### 第八步：安装语言包（未更改语言可直接跳过）

php

```
01git clone https://github.com/ZvonimirSun/YOURLS-zh_CN.git && mv YOURLS-zh_CN/* /root/YOURLS-1.9.2/user/languages/ && rm -rf YOURLS-zh_CN
```

#### 第九步：配置并重启 Apache

bash

```
010203sudo mv /root/YOURLS-1.9.2/* /var/www/html/
sudo chown -R www-data:www-data /var/www/html/
sudo systemctl restart apache2
```

### 结语：

欢迎在评论区留下配置好的短链接，比比看能短到什么地步

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
