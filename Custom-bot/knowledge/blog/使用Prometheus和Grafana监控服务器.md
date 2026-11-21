# 使用Prometheus和Grafana监控服务器

> 标题：使用Prometheus和Grafana监控服务器
> 分类：Linux运维
> 标签：Linux
> 原文：https://www.xinz.fun/archives/使用Prometheus和Grafana监控服务器

> **导读**：这篇是「使用Prometheus和Grafana监控服务器」的实操教程。下文按「安装 Prometheus 和 Grafana」「配置 Grafana」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾Linux运维的读者。执行前建议先备份原配置，并在测试环境验证。

本文使用的系统为 Arch Linux 部分包可能在您的系统不存在 / 低版本

## 安装 Prometheus 和 Grafana

```bash
sudo pacman -S prometheus grafana
```

## 配置 Grafana

1) 由于 Prometheus 的默认配置足够监控本机，因此不进行配置，但仍放出配置文件

```
# my global config
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).
 
# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093
 
# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"
 
# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"
 
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
 
    static_configs:
      - targets: ["127.0.0.1:9090"]
```

2) 启动服务

```bash
sudo systemctl enable prometheus grafana --now
```

3) 登陆 Grafana

地址为 :3000 ，默认帐号密码 admin/admin 登陆会有要求设置新密码

4) 添加图表

![配图](https://blog.ilolicon.com/wp-content/uploads/2023/10/image.png)在登陆后点击 ***Add new connection*** 搜索到 ***Prometheus***

![配图](https://blog.ilolicon.com/wp-content/uploads/2023/10/image-1.png)进入后点击 Add new data source ，在 HTTP 栏填入 [***http://127.0.0.1:9090***](http://127.0.0.1:9090) 即 Prometheus 监听地址，在 Other 中更改 HTTP method 从 POST 改为 GET，最后点击 Save & test

![配图](https://blog.ilolicon.com/wp-content/uploads/2023/10/image-2.png)![配图](https://blog.ilolicon.com/wp-content/uploads/2023/10/image-4.png)保存后点击最上方的 Dashboards，从三个中随便选一个导入

![配图](https://blog.ilolicon.com/wp-content/uploads/2023/10/image-5-1024x627.png)

![配图](https://blog.ilolicon.com/wp-content/uploads/2023/10/image-6.png)回到 Dashboards 即可查看监控

![配图](https://blog.ilolicon.com/wp-content/uploads/2023/10/image-7.png)![配图](https://blog.ilolicon.com/wp-content/uploads/2023/10/image-8-1024x378.png)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
