# docker容器命令

> 标题：docker容器命令
> 分类：Docker容器
> 标签：docker、Linux、nas、群晖
> 说明：这是一篇未公开文章，内容仅进入本地知识库。

> **导读**：这篇围绕「docker容器命令」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾Docker容器的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 设置开机启动
2. Docker容器无法启动后,如何修改里面的配置文件
3. 进入容器交互控制台
4. 查看日志
5. 进入容器命令行
6. 删除容器
7. 删除所有不使用的镜像
8. 从容器拷贝文件到宿主机
9. 更新容器镜像
10. 永久定时更新所有容器、镜像：

## 设置开机启动

```bash
docker  update  --restart=always 容器名称
```

## Docker容器无法启动后,如何修改里面的配置文件

```bash
docker cp [容器id]：docker容器中配置文件路径  主机路径
例如：
docker cp mysql:/etc/mysql/my.cnf /home/my.cnf
这样就能把容器中的文件拿到本地来，然后进行修改之后呢，再通过该命名上传到容器中去。
例如：
docker cp 主机文件路径 容器id：docker容器中配置文件路径
docker cp /home/my.cnf mysql:/etc/mysql/my.cnf
```

之后我们重启容器就可以了。

## 进入容器交互控制台

```
#进入
docker attach 容器名
# 退出交互控制台
Ctrl+p Ctrl+q
```

## 查看日志

```bash
docker logs 容器名
```

## 进入容器命令行

```bash
docker exec -it 容器名 /bin/sh
```

## 删除容器

```bash
docker stop 容器名/id & docker rm 容器名/id
```

## 删除所有不使用的镜像

```bash
docker image prune --force --all 或者 docker image prune -f -a
```

## 从容器拷贝文件到宿主机

```bash
docker cp 容器名:容器目录 宿主机目录
```

## 更新容器镜像

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower -cR 容器名
```

## 永久定时更新所有容器、镜像：

```bash
docker run -d --name watchtower -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower -cR -i 容器名 -s "0 0 2  *" --rolling-restart
```

、

常用命令结束

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
