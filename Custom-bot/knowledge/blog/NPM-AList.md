# 解决使用NPM反代AList无法播放视频的问题

> 标题：解决使用NPM反代AList无法播放视频的问题
> 分类：反代与网络
> 标签：无
> 原文：https://www.xinz.fun/archives/NPM-AList

> **导读**：这篇记录「解决使用NPM反代AList无法播放视频的问题」的排查与处理过程。先说明问题现象，再给出配置或命令，最后补充验证方法；遇到相似报错时可按顺序对照。
>
> 适合正在折腾反代与网络的读者。执行前建议先备份原配置，并在测试环境验证。

2024年1月4日 320点热度 2人点赞 0条评论

> AList是一款非常好用存储的文件列表程序，可以方便地挂载本地存储和各种第三方网盘，在NAS圈几乎可以算是人手一份的必备工具了。不出意外，笔者的NAS上也跑了一个；出意外的是，笔者千载难逢在网页上打算看一个视频。。。却发现播放不了！这不能忍吧。

### 1️⃣ 背景

1、笔者是使用的Nginx Proxy Manager(NPM)来反代的AList，正常打开Web界面是没有问题的：
![配图](https://www.xinz.fun/upload/65956c5a7eb89.jpg)![配图](/upload/659572ac77058.jpg)
2、当时打开一个视频或音乐时，完全不能播放，一直在转圈圈：
![配图](/upload/6595706c57618-aixc.jpg)

3、请出 F12 大法，果然发现了蹊跷，注意看剪头指向的地方，笔者反代的端口是 998，但是播放视频时的加载链接自动把端口 998 去掉了，自然就加载不到视频啦。
![配图](https://www.xinz.fun/upload/659570f36c0f9.jpg)

### 2️⃣ 解决

前面通过F12找到了无法播放的原因——反代丢端口，那我们让反代不丢端口自然就解决这个问题了。

1、打开NPM的Alist代理配置，切换到`Advanced`
![配图](/upload/659572ac77058-gjcs.jpg)

2、将下面的代码粘贴到`Custom Nginx Configuration`中，再点击`Save`保存即可

```nginx
location / {
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto $scheme;
  proxy_set_header Host $http_host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header Range $http_range;
  proxy_set_header If-Range $http_if_range;
  proxy_redirect off;
  proxy_pass http://192.168.31.91:5244;
  client_max_body_size 20000m;
}
```

> 注意 proxy\_pass 后面的 IP 和端口改成你自己的 Alist 的 IP 和端口

3、现在重新刷新网页就可以愉快地观看视频啦
![配图](/upload/65957d7e7a699.jpg)

原文链接:[解决使用NPM反代AList无法播放视频的问题 - 胡萝虎的博客 (huluohu.com)](https://www.huluohu.com/posts/927/)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
