# Docker 部署指南

## 安装 Docker

**macOS:** 
```bash
brew install orbstack  # 或 docker
```

**Linux:**
```bash
curl -fsSL https://get.docker.com | sh
```

**Windows:** 下载 [Docker Desktop](https://www.docker.com/products/docker-desktop/)

---

## 快速启动

### 前台运行（开发/测试）
```bash
docker run -it --rm -p 8000:8000 rhasspy/snowboy-seasalt
```

### 后台运行（生产）
```bash
# Docker 17.06+ 
docker run -d --name snowboy -p 8000:8000 --restart unless-stopped rhasspy/snowboy-seasalt

# 或使用多行格式（仅限 Linux/macOS）
docker run -d \
  --name snowboy \
  -p 8000:8000 \
  --restart unless-stopped \
  rhasspy/snowboy-seasalt
```

### Docker Compose
```bash
# Docker Compose v2 (推荐)
docker compose up -d

# Docker Compose v1 (兼容旧版本)
docker-compose up -d
```

**访问：** http://localhost:8000

---

## 容器管理

```bash
docker ps                    # 查看容器
docker logs -f snowboy       # 查看日志
docker stop snowboy          # 停止
docker start snowboy         # 启动
docker restart snowboy       # 重启
docker rm -f snowboy         # 删除
```

---

## 高级配置

### 自定义端口
```bash
docker run -d -p 9000:8000 --name snowboy rhasspy/snowboy-seasalt
```

### 保存模型到本地
```bash
# Linux/macOS
docker run -d -p 8000:8000 -v ~/models:/app/models --name snowboy rhasspy/snowboy-seasalt

# Windows (PowerShell)
docker run -d -p 8000:8000 -v ${PWD}/models:/app/models --name snowboy rhasspy/snowboy-seasalt

# Windows (CMD)
docker run -d -p 8000:8000 -v %cd%/models:/app/models --name snowboy rhasspy/snowboy-seasalt
```

### 资源限制
```bash
# Docker 17.06+
docker run -d -p 8000:8000 --memory=512m --cpus=1.0 --name snowboy rhasspy/snowboy-seasalt
```

---

## HTTP API

```bash
curl -X POST \
  -F modelName=my-wakeword \
  -F example1=@voice1.wav \
  -F example2=@voice2.wav \
  -F example3=@voice3.wav \
  --output my-wakeword.pmdl \
  http://localhost:8000/generate
```

---

## 故障排除

### Docker 未运行
```bash
# macOS
open -a "OrbStack"  # 或 "Docker"

# Windows
# 从开始菜单启动 Docker Desktop

# Linux
sudo systemctl start docker
```

### 端口占用
```bash
# 使用其他端口
docker run -d -p 9000:8000 --name snowboy rhasspy/snowboy-seasalt

# 查看占用进程
# Linux/macOS
lsof -i :8000

# Windows
netstat -ano | findstr :8000

# 停止进程
# Linux/macOS
kill -9 <PID>

# Windows
taskkill /PID <PID> /F
```

### 容器无法启动
```bash
docker logs snowboy          # 查看错误
docker rm -f snowboy         # 删除重建
docker pull rhasspy/snowboy-seasalt  # 重新拉取镜像
```

### 麦克风无法使用
- 使用 Chrome/Edge 浏览器
- 检查浏览器麦克风权限
- 确保访问 localhost（非 IP）

---

## 局域网访问

```bash
# 获取本机 IP
# macOS
ipconfig getifaddr en0

# Linux
hostname -I | awk '{print $1}'

# Windows
ipconfig | findstr IPv4

# 然后访问: http://你的IP:8000
```

---

## 安全建议

### 仅本地访问
```bash
docker run -d -p 127.0.0.1:8000:8000 --name snowboy rhasspy/snowboy-seasalt
```

### 使用反向代理（Nginx）
```nginx
server {
    listen 443 ssl;
    server_name snowboy.example.com;
    
    location / {
        proxy_pass http://localhost:8000;
    }
}
```

