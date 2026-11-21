# 简单使用docker-compose部署Grafana和Prometheus环境

> 标题：简单使用docker-compose部署Grafana和Prometheus环境
> 分类：Linux运维
> 标签：无
> 原文：https://www.xinz.fun/archives/Gf-Pth

> **导读**：这篇是「简单使用docker-compose部署Grafana和Prometheus环境」的实操教程。下文按「安装docker和docker-compose」「目录结构」「docker compose及环境变量配置」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾Linux运维的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 安装docker和docker-compose
2. 目录结构
3. docker compose及环境变量配置
4. NGINX 反代
5. 配置prometheus.yml文件
6. 添加Prometheus数据源以及import面板
7. 开启匿名访问
8. Alertmanager 规则
9. 参考资料

![1699761893981.png](https://img1.imgtp.com/2023/11/12/LNYRmkaw.png)

1699761893981.png

此帖使用 docker compose 来 Grafana 和 Prometheus 环境。为什么用 docker compose 来部署，因为使用 1 个 `docker-compose.yml` 文件就可以配置应用程序的所有服务，可移植性高，单个主机上可形成多个隔离环境防止不同服务和项目互相干扰等等

只是进行简单入门安装部署 Grafana 和 Prometheus，帮助大家实现 1 个高级探针的梦想。网上教程很多，此帖内容可以仅作为参考。后续更多更难的个性化配置不写，因为实在是太多了，有兴趣可以直接看官网 doc

这帖子是我随便写写的，没有认真去排版什么的，有错误或不详之处尽量提出

## 安装docker和docker-compose

看看官网安装就行，不复杂。或者用其他的脚本安装 docker, docker engine, docker compose 也行

[Install Docker Engine | Docker Documentation](https://www.nodeseek.com/jump?to=https%3A%2F%2Fdocs.docker.com%2Fengine%2Finstall%2F)

[Install Docker Engine on Debian | Docker Documentation](https://www.nodeseek.com/jump?to=https%3A%2F%2Fdocs.docker.com%2Fengine%2Finstall%2Fdebian%2F)

[Install Docker Engine on Ubuntu | Docker Documentation](https://www.nodeseek.com/jump?to=https%3A%2F%2Fdocs.docker.com%2Fengine%2Finstall%2Fubuntu%2F)

## 目录结构

docker-compose.yml 目录下的当前结构参考，`.env` 是环境变量文件，`grafana.ini` 是 grafana 的配置文件

plaintext

```
010203040506070809101112.
├── docker-compose.yml
├── .env
├── grafana
│   ├── conf
│   │   └── grafana.ini
│   └── provisioning
│       ├── dashboards
│       └── datasources
│           └── datasource.yml
└── prometheus
    └── prometheus.yml
```

我的是这样

plaintext

```
010203040506070809101112131415161718192021222324.
├── alertmanager
│   └── config
│       └── alertmanager.yml
├── docker-compose.yml
├── flush
├── grafana
│   ├── conf
│   │   └── grafana.ini
│   └── provisioning
│       ├── dashboards
│       │   ├── default.yaml
│       │   └── node_exporter_full.json
│       └── datasources
│           └── datasource.yml
├── loki
├── mosquitto
│   └── mosquitto.conf
└── prometheus
    ├── node.json
    ├── prometheus.yml
    ├── rules
    │   └── alert_rule.yml
    └── web.yml
```

## docker compose及环境变量配置

基础 `docker-compose.yml` 配置差不多就这样写，可根据自己需要减少或增加 service

yaml

```yaml
010203040506070809101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869version: "3.8"

volumes:
  prometheus_data: {}
  grafana_data: {}

networks:
  monitoring:

services:
  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    restart: unless-stopped
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - "--path.procfs=/host/proc"
      - "--path.rootfs=/rootfs"
      - "--path.sysfs=/host/sys"
      - "--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)"
    ports:
      - "9100:9100"
    networks:
      - monitoring

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--web.console.libraries=/etc/prometheus/console_libraries"
      - "--web.console.templates=/etc/prometheus/consoles"
      - "--web.enable-lifecycle"
      - "--web.enable-admin-api"
    ports:
      - "9090:9090"
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/provisioning/datasources:/etc/grafana/provisioning/datasources
      - ./grafana/conf/grafana.ini:/etc/grafana/grafana.ini
    environment:
      - GF_SECURITY_ADMIN_USER=${GRAFANA_ADMIN_USER}
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD}
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_SMTP_ENABLED=true
      - GF_SMTP_HOST=${GF_SMTP_HOST}
      - GF_SMTP_USER=${GF_SMTP_USER}
      - GF_SMTP_PASSWORD=${GF_SMTP_PASSWORD}
      - GF_SMTP_FROM_ADDRESS=${GF_SMTP_FROM_ADDRESS}  
    restart: unless-stopped
    ports:
      - "3000:3000"
    networks:
      - monitoring
```

这是我目前使用的 `docker-compose.yml`

yaml

```yaml
001002003004005006007008009010011012013014015016017018019020021022023024025026027028029030031032033034035036037038039040041042043044045046047048049050051052053054055056057058059060061062063064065066067068069070071072073074075076077078079080081082083084085086087088089090091092093094095096097098099100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158159160161162163164165166167168169version: "3.8"

volumes:
  prometheus_data: {}
  grafana_data: {}
  alertmanager_data: {}
  promtail_data: {}
  loki_data: {}
  mosquitto_data: {}
  mosquitto_log: {}

networks:
  monitoring:

services:
  watchtower:
    image: containrrr/watchtower:latest
    environment:
      - WATCHTOWER_LABEL_ENABLE=true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    labels:
      com.centurylinklabs.watchtower.enable: "true"

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    restart: unless-stopped
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - "--path.procfs=/host/proc"
      - "--path.rootfs=/rootfs"
      - "--path.sysfs=/host/sys"
      - "--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)"
    ports:
      - "9100:9100"
    networks:
      - monitoring
    labels:
      com.centurylinklabs.watchtower.enable: "true"

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--web.console.libraries=/etc/prometheus/console_libraries"
      - "--web.console.templates=/etc/prometheus/consoles"
      - "--web.enable-lifecycle"
      - "--web.enable-admin-api"
    ports:
      - "9110:9090"
    networks:
      - monitoring
    labels:
      com.centurylinklabs.watchtower.enable: "true"

  cadvisor:
    image: gcr.io/cadvisor/cadvisor-arm64:v0.47.2
    container_name: cadvisor
    privileged: true
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    restart: unless-stopped
    devices:
      - /dev/kmsg
    ports:
      - "8080:8080"
    networks:
      - monitoring
    labels:
      com.centurylinklabs.watchtower.enable: "true"

  mosquitto:
    image: eclipse-mosquitto:latest
    container_name: mosquitto
    restart: always
    ports:
      - "1883:1883"
    networks:
      - monitoring
    volumes:
      - ./mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - mosquitto_data:/mosquitto/data
      - mosquitto_data:/mosquitto/log
    labels:
      com.centurylinklabs.watchtower.enable: "true"

  loki:
    image: grafana/loki:latest
    container_name: loki
    volumes:
      - loki_data:/data
    restart: unless-stopped
    ports:
      - "3100:3100"
    command:
      - "-config.file=/etc/loki/local-config.yaml"
    networks:
      - monitoring
    labels:
      com.centurylinklabs.watchtower.enable: "true"

  promtail:
    image: grafana/promtail:latest
    container_name: promtail
    volumes:
      - /var/log:/var/log
      - promtail_data:/data
    command:
      - "-config.file=/etc/promtail/config.yml"
    networks:
      - monitoring
    labels:
      com.centurylinklabs.watchtower.enable: "true"

  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    volumes:
      - ./alertmanager/config:/config
      - alertmanager_data:/data
      - alertmanager_data:/alertmanager
    command:
      - "--config.file=/config/alertmanager.yml"
    restart: always
    ports:
      - "9093:9093"
    networks:
      - monitoring
    labels:
      com.centurylinklabs.watchtower.enable: "true"

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/provisioning/datasources:/etc/grafana/provisioning/datasources
      - ./grafana/conf/grafana.ini:/etc/grafana/grafana.ini
    environment:
      - GF_SECURITY_ADMIN_USER=${GRAFANA_ADMIN_USER}
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD}
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_SMTP_ENABLED=true
      - GF_SMTP_HOST=${GF_SMTP_HOST}
      - GF_SMTP_USER=${GF_SMTP_USER}
      - GF_SMTP_PASSWORD=${GF_SMTP_PASSWORD}
      - GF_SMTP_FROM_ADDRESS=${GF_SMTP_FROM_ADDRESS}  
    restart: unless-stopped
    ports:
      - "3000:3000"
    networks:
      - monitoring
    labels:
      com.centurylinklabs.watchtower.enable: "true"
```

配置.env环境变量

plaintext

```ini
010203040506070809GRAFANA_ADMIN_USER=your-name
GRAFANA_ADMIN_PASSWORD=your-passwd
GRAFANA_DOMAIN=status.microcharon.dev

#Grafana SMTP示例
GF_SMTP_HOST=smtp.outlook.com:587
GF_SMTP_USER=no-reply@microcharon.dev
GF_SMTP_PASSWORD=your-passwd
GF_SMTP_FROM_ADDRESS=no-reply@microcharon.dev
```

最后用 `docker compose up -d` 在 `docker-compose.yml` 当前目录启动就行。由于默认 Grafana 监听 3000 端口，所以访问 3000 端口即可访问到 Grafana WebUI 界面

## NGINX 反代

其中一定要注意添加 `proxy_set_header` 参数，否则登录会 `origin not allowed`

[After update to 8.3.5: 'Origin not allowed' behind proxy - Grafana / Configuration - Grafana Labs Community Forums](https://www.nodeseek.com/jump?to=https%3A%2F%2Fcommunity.grafana.com%2Ft%2Fafter-update-to-8-3-5-origin-not-allowed-behind-proxy%2F60598)

NGINX

```nginx
01020304050607        location / {
            proxy_pass http://127.0.0.1:3000;
            proxy_redirect off;
            proxy_set_header Host status.microcharon.dev;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
```

### 二进制安装配置node exporter

node exporter 部署在服务监控特定的主机上，主要是暴露 metrics 给 Prometheus。建议直接用二进制安装就行

下面是我前些日子写的 1 个简单 script，主要放在我的 ARM 和 amd64 主机上，默认监听 9100 端口，使用前记得添加执行权限。仅作参考，如果有误可以在下方提出我好修改

bash

```ini
0102030405060708091011121314151617181920212223242526272829303132333435363738394041#!/bin/bash

VER=$(curl -s https://api.github.com/repos/prometheus/node_exporter/releases/latest | grep tag_name | cut -d '"' -f 4 | sed 's/v//')

ARCH=$(uname -m)
TYPE=""

if [ "$ARCH" == "x86_64" ]; then
  TYPE="amd64"
elif [ "$ARCH" == "arm5l" ]; then
  TYPE="armv5"
elif [ "$ARCH" == "armv6l" ]; then
  TYPE="armv6"
elif [ "$ARCH" == "armv7l" ]; then
  TYPE="armv7"
elif [ "$ARCH" == "aarch64" ]; then
  TYPE="arm64"
fi

wget https://github.com/prometheus/node_exporter/releases/download/v${VER}/node_exporter-${VER}.linux-${TYPE}.tar.gz

tar -zxvf node_exporter*.tar.gz && cp ./node_exporter-${VER}.linux-${TYPE}/node_exporter /usr/local/bin

rm node_exporter*.tar.gz node_exporter*/* && rmdir node_exporter-${VER}.linux-${TYPE}

cat > /etc/systemd/system/node_exporter.service << "EOF"
[Unit]
Description=node_exporter
Documentation=https://github.com/prometheus/node_exporter
 
[Service]
ExecStart=/usr/local/bin/node_exporter  --web.listen-address=:9100
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable node_exporter
systemctl start node_exporter
```

安装好 node\_exporter 后访问 9100 端口，在 metrics 路径下可以看到相关常用指标。部分不常用/敏感的指标需要自己另行开启，此处不说

如果担心泄露主机指标信息，可以通过防火墙限制 IP 访问或采用其它高位端口防止，此处不细究

## 配置prometheus.yml文件

实际上配置很复杂，这里给个参考例子，配置好了可以重启一下 prometheus 或者 `curl -X POST http://localhost:9090/-/reload` （前提是启用 --web.enable-lifecycle）

yaml

```
0102030405060708091011121314151617181920212223242526---
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "Node Exporter"
    static_configs:
      - targets: ["<ip-address>:9100"]
        labels:
          instance: layerstack-ubuntu-hkg
      - targets: ["<ip-address>:9100"]
        labels:
          instance: hetzner-ubuntu-fsn

  - job_name: "Cadvisor"
    static_configs:
      - targets: ["cadvisor:8080"]
        labels:
          instance: cadvisor

  - job_name: "Prometheus"
    static_configs:
      - targets: ["prometheus:9090"]
        labels:
          instance: prometheus
```

## 添加Prometheus数据源以及import面板

添加 Promethus 数据源如下，也可以是 `http://localhost:9090`，测试一下保存就行

![1699761948189.png](https://img1.imgtp.com/2023/11/12/nbiRuPep.png)

1699761948189.png

[Dashboards | Grafana Labs](https://www.nodeseek.com/jump?to=https%3A%2F%2Fgrafana.com%2Fgrafana%2Fdashboards%2F)

一般我们直接用别人的模板就行，推荐以下几个

- 16098 (Node Exporter Dashboard 220417 通用Job分组版)
- 1860 (Node Exporter Full)
- 14282 (Cadivisor Exporter)
- 193 (Docker Monitoring)

![1699762192740.png](https://img1.imgtp.com/2023/11/12/eEsmijEi.png)

1699762192740.png

导入模板后添加 Prometheus 数据源即可

## 开启匿名访问

由于我已经提前 `./grafana/conf/grafana.ini:/etc/grafana/grafana.ini` 映射出来了，所以可以直接在宿主机上 edit 就行

寻找 `auth.anonymous` 一行，配置如下。为了防止匿名游客访问我的主要组织，可以先在 web 界面上新建 1 个 organization 如图中的 Guest

然后 restart 一下 Grafana 即可，这样游客访问 Grafana 时就不会访问到你的主要组织

![1699762397115.png](https://img1.imgtp.com/2023/11/12/PK1lVelo.png)

1699762397115.png

![1699762348106.png](https://img1.imgtp.com/2023/11/12/KyEVxar7.png)

1699762348106.png

后续可以在 administration 中设置默认 dashboard，这样游客访问时首先看到的就是你设置的默认 dashboard 了

![1699762441879.png](https://img1.imgtp.com/2023/11/12/ckZ10BNQ.png)

1699762441879.png

这是我给出的例子：[Node Exporter Full - Dashboards - Grafana (microcharon.dev)](https://www.nodeseek.com/jump?to=https%3A%2F%2Fstatus.microcharon.dev%2F)

## Alertmanager 规则

有人要规则，懒得写了，看doc or参考我的也行

### 通知规则 prometheus-grafana/alertmanager/config/alertmanager.yml

yaml

```
010203040506070809101112131415161718192021222324252627282930313233343536373839404142434445464748global:
  resolve_timeout: 5m
  smtp_from: 'Microcharon Status Dev <no-reply@microcharon.dev>'
  smtp_smarthost: 'smtp.outlook.com:587'
  smtp_hello: 'status.microcharon.dev'
  smtp_auth_username: 'no-reply@microcharon.dev'
  smtp_auth_password: 'your-passwd'
  smtp_require_tls: true

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'telegram'
  routes:
  - match:
     severity: page
    receiver: 'telegram-and-email'

receivers:
- name: 'webhook'
  webhook_configs:
  - url: 'http://127.0.0.1:5001/'

- name: 'telegram'
  telegram_configs:
  - bot_token: 'your-bot-token'
    chat_id: 00000000 (replace it [int])
    parse_mode: 'HTML'

- name: 'email'
  email_configs:
  - to: 'admin@microcharon.dev'

- name: 'telegram-and-email'
  telegram_configs:
  - bot_token: 'your-bot-token'
    chat_id: 00000000 (replace it [int])
    parse_mode: 'HTML'
  email_configs:
  - send_resolved: true
    to: 'admin@microcharon.dev'
      # from: 'Microcharon Status Dev <no-reply@microcharon.dev>'
      # smarthost: 'smtp.outlook.com:587'
      # auth_username: 'no-reply@microcharon.dev'
      # auth_password: '{password}'
      # require_tls: true
```

### prometheus 报警规则 prometheus-grafana/prometheus/rules/alert\_rule.yml

yaml

```
01020304050607080910111213141516171819202122232425262728293031groups:
- name: alertmanager
  rules:

  # Alert for any instance that is unreachable for >5 minutes.
  - alert: InstanceDown
    expr: up == 0
    for: 5m
    labels:
      severity: page
    annotations:
      summary: "Instance {{ $labels.instance }} down"
      description: "{{ $labels.instance }} of job {{ $labels.job }} has been down for more than 5 minutes."

  # Alert for any instance that has a median request latency >1s.
  - alert: APIHighRequestLatency
    expr: api_http_request_latencies_second{quantile="0.5"} > 1
    for: 10m
    annotations:
      summary: "High request latency on {{ $labels.instance }}"
      description: "{{ $labels.instance }} has a median request latency above 1s (current value: {{ $value }}s)"

  # Alert for any instance that CPU usage above 80% for >5 minutes.
  - alert: HighCPUUsage
    expr: 100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High CPU usage on {{ $labels.instance }}"
      description: "{{ $labels.instance }} has CPU usage above 80% (current value: {{ $value }}%)"
```

## 参考资料

[Configure Grafana | Grafana documentation](https://www.nodeseek.com/jump?to=https%3A%2F%2Fgrafana.com%2Fdocs%2Fgrafana%2Flatest%2Fsetup-grafana%2Fconfigure-grafana%2F%23using-environment-variables)

[Dashboards | Grafana Labs](https://www.nodeseek.com/jump?to=https%3A%2F%2Fgrafana.com%2Fgrafana%2Fdashboards%2F)

[[Prometheus] 學習筆記 - Monitoring Overview | 小信豬的原始部落 (godleon.github.io)](https://www.nodeseek.com/jump?to=https%3A%2F%2Fgodleon.github.io%2Fblog%2FPrometheus%2FPrometheus-LearningNotes-Monitoring%2F)

[Prometheus Grafana - Hetzner Docs](https://www.nodeseek.com/jump?to=https%3A%2F%2Fdocs.hetzner.com%2Fcloud%2Fapps%2Flist%2Fprometheus-grafana%2F)

[After update to 8.3.5: 'Origin not allowed' behind proxy - Grafana / Configuration - Grafana Labs Community Forums](https://www.nodeseek.com/jump?to=https%3A%2F%2Fcommunity.grafana.com%2Ft%2Fafter-update-to-8-3-5-origin-not-allowed-behind-proxy%2F60598)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
