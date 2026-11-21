# Docker部署“dailyhot”

> 标题：Docker部署“dailyhot”
> 分类：面板与工具
> 标签：docker
> 原文：https://www.xinz.fun/archives/dailyhot

> **导读**：这篇是「Docker部署“dailyhot”」的实操教程。下文按「介绍」「Docker部署」「最后」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾面板与工具的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 介绍
2. Docker部署
3. 最后

## 介绍

一个聚合了中文热门站点数据的项目， 不出户，知天下！

该项目分两部分：今日热榜API及前端页面

示例站点：<https://hot.imsyy.top/>

GitHub地址-API：[imsyy/DailyHotApi: 今日热榜 API，一个聚合热门数据的 API 接口](https://www.nodeseek.com/jump?to=https%3A%2F%2Fgithub.com%2Fimsyy%2FDailyHotApi)

GitHub地址-前端：[imsyy/DailyHot: DailyHot 今日热榜前端页面](https://www.nodeseek.com/jump?to=https%3A%2F%2Fgithub.com%2Fimsyy%2FDailyHot)

docker镜像-API：[liwangsheng/dailyhot-api - Docker Image | Docker Hub](https://www.nodeseek.com/jump?to=https%3A%2F%2Fhub.docker.com%2Fr%2Fliwangsheng%2Fdailyhot-api)

docker镜像-前端：[liwangsheng/dailyhot-web - Docker Image | Docker Hub](https://www.nodeseek.com/jump?to=https%3A%2F%2Fhub.docker.com%2Fr%2Fliwangsheng%2Fdailyhot-web)

## Docker部署

看到好玩的项目，第一件事就是打包成docker镜像😋

x64架构可跳过构建阶段直接使用我的镜像

### 构建镜像
#### API镜像

```
0102030405# 拉取代码
git clone https://github.com/imsyy/DailyHotApi.git

# 进入目录
cd DailyHotApi/
```

编辑Dockerfile，如下：

```
010203040506070809FROM alpine

WORKDIR /app

COPY . .

RUN apk update && apk add nodejs npm && npm install

CMD ["npm","start"]
```

```
0102# 构建镜像
docker build -t dailyhot-api .
```

#### 前端镜像

```
0102030405060708# 拉取代码
git clone https://github.com/imsyy/DailyHot.git

# 进入目录
cd DailyHot/

# 编辑start.sh脚本
vim start.sh
```

要将API 地址及备案号作为环境变量传入打包好的静态资产并构建镜像需要写一个脚本，内容如下：

```
0102030405060708#!/bin/ash

# 替换 API 地址及备案号
find '/app' -name '*.js' -exec sed -i -e 's,http://localhost:6688,'"$API"',g' {} \;
find '/app' -name '*.js' -exec sed -i -e 's,豫ICP备2022018134号-1,'"$ICP"',g' {} \;

# # 启动 httpd 服务器
httpd -f -p 80 -h /app
```

```
0102# 添加执行权限
chmod +x start.sh
```

编辑Dockerfile：

```dockerfile
01020304050607080910111213141516171819202122232425FROM node:16-alpine

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

RUN npm run build

FROM busybox:1.35.0-uclibc

WORKDIR /app

COPY --from=0 /app/dist .

COPY --from=0 /app/start.sh .

ENV API="https://api-hot.imsyy.top"

ENV ICP="豫ICP备2022018134号-1"

CMD ["/app/start.sh"]
```

```
0102# 构建镜像
docker build -t dailyhot-web .
```

### 运行
#### API容器

```
010203040506docker run -d \
    --name dailyhot-api \
    --restart always \
    -p 6688:6688 \
    -e ALLOWED_DOMAIN="https://hot.imsyy.top" \  # 可选，指定允许的前端域名
    liwangsheng/dailyhot-api
```

访问 ip:6688即可看到api服务

##### 前端容器

```
01020304050607docker run -d \
    --name dailyhot-web \
    -p 6677:80 \
    -e API="https://hot-api.bbit.fun" \
    -e ICP="没有备案捏" \
    --restart always \
    liwangsheng/dailyhot-web
```

修改刚刚搭建的api地址以及备案号，访问ip:6677即可看到热榜

## 最后

如果有问题或需要改进的地方请评论回复我😇

如果觉得文章对你有用，请随意赞赏

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
