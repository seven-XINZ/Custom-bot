# 自建京东库sign接口

> 标题：自建京东库sign接口
> 分类：面板与工具
> 标签：docker、Linux、nas、群晖
> 原文：https://www.xinz.fun/archives/zi-jian-jing-dong-ku-signjie-kou

> **导读**：这篇围绕「自建京东库sign接口」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾面板与工具的读者。执行前建议先备份原配置，并在测试环境验证。

创建容器

```bash
docker run -dit \
  --name official \
  --restart always \
  --hostname official \
  -p 9527:80 \
  qninq/signapi:latest
```

运行完:<http://:9527/jd/sign> 就是本地sign接口
KR库自定义SIGN接口变量： export JD\_SIGN\_KRAPI="http://:9527/jd/sign"
奥特曼只需填写[http://ip:9527](http://:9527/jd/sign)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
