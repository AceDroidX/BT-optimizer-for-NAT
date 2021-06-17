# BT-optimizer-for-NAT
让没有公网ip的用户(FullCone)也能享受BT/PT下载！

README在写了.png

Client:
docker-compose.yml:
```yaml
version: "3.8"
services:
  bt-opt:
    build: ./bt-opt
    environment:
     - TZ=Asia/Shanghai
     - internal_port=50000
     - api_host=127.0.0.1
     - api_port=8081
     - proxy_port=8080
     - remote_enable=true
     - remote_url=https://api.example.com
     - remote_name=default
     - http_rewrite=example.com
```