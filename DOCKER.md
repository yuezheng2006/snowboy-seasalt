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

## 前后端架构说明

### 一体化架构

本项目是**前后端一体部署**，所有服务运行在同一个 Docker 容器中：

```
Docker 容器 (端口 8000)
├── 后端服务 (Quart/Python)
│   ├── Web UI 路由 (/)
│   ├── RESTful API (/generate, /delete)
│   └── 静态资源服务 (/css, /js, /img)
└── 前端文件
    ├── HTML 模板
    ├── JavaScript (原生 + WaveSurfer.js)
    └── CSS (Bootstrap + FontAwesome)
```

### 前端访问

#### Web UI 界面
```bash
# 浏览器访问
http://localhost:8000
# 或
http://localhost:8000/index.html
```

**功能：**
- 麦克风录音界面
- 实时音频波形显示
- 3段语音录制
- 在线生成 .pmdl 模型
- 直接下载模型文件

**支持的浏览器：**
- Chrome/Chromium ✅ (推荐)
- Microsoft Edge ✅
- Firefox ✅
- Safari ⚠️ (可能需要额外配置)

#### 静态资源路由
```
/css/*          - 样式文件 (Bootstrap)
/js/*           - JavaScript 文件 (WaveSurfer.js)
/img/*          - 图片资源
/webfonts/*     - 字体文件 (FontAwesome)
```

### RESTful API 访问

#### 1. 生成模型 API

**端点：** `POST /generate`

**请求格式：** `multipart/form-data`

**必需参数：**
- `modelName` - 模型名称（字符串）
- `example1` - 第 1 段音频文件
- `example2` - 第 2 段音频文件  
- `example3` - 第 3 段音频文件

**可选参数：**
- `lang` - 语言代码（`en` 或 `zh`，默认 `en`）
- `noTrim` - 是否跳过静音裁剪（`true`/`false`，默认 `false`）

**返回：** 二进制 `.pmdl` 文件

**示例：**

```bash
# 基础用法
curl -X POST http://localhost:8000/generate \
  -F "modelName=my-wakeword" \
  -F "example1=@voice1.wav" \
  -F "example2=@voice2.wav" \
  -F "example3=@voice3.wav" \
  -o my-wakeword.pmdl

# 中文唤醒词
curl -X POST http://localhost:8000/generate \
  -F "modelName=nihao-xiaozhi" \
  -F "lang=zh" \
  -F "example1=@sample1.wav" \
  -F "example2=@sample2.wav" \
  -F "example3=@sample3.wav" \
  -o nihao-xiaozhi.pmdl

# 不裁剪静音
curl -X POST "http://localhost:8000/generate?noTrim=true" \
  -F "modelName=test" \
  -F "example1=@ex1.wav" \
  -F "example2=@ex2.wav" \
  -F "example3=@ex3.wav" \
  -o test.pmdl

# 使用 Python requests
import requests

files = {
    'example1': open('voice1.wav', 'rb'),
    'example2': open('voice2.wav', 'rb'),
    'example3': open('voice3.wav', 'rb'),
}
data = {'modelName': 'my-wakeword', 'lang': 'zh'}

response = requests.post('http://localhost:8000/generate', 
                        files=files, data=data)

with open('my-wakeword.pmdl', 'wb') as f:
    f.write(response.content)
```

#### 2. 删除临时文件 API

**端点：** `POST /delete`

**参数：**
- `modelName` - 要删除的模型名称（URL 参数）

**示例：**
```bash
curl -X POST "http://localhost:8000/delete?modelName=my-wakeword"
```

### 音频要求

**支持的格式：**
- WAV, MP3, OGG, WebM, FLAC 等（任何 ffmpeg 支持的格式）

**自动处理：**
- 转换为 16kHz 采样率
- 转换为 16-bit 深度
- 转换为单声道 (Mono)
- 自动裁剪静音（可选）

**推荐规格：**
- 采样率：16kHz
- 位深度：16-bit
- 声道：单声道
- 时长：2-5 秒

### 端口映射说明

```bash
docker run -p [主机端口]:[容器端口] rhasspy/snowboy-seasalt
                ↓              ↓
              本地访问      容器内部服务
              
# 默认映射
-p 8000:8000
访问: http://localhost:8000

# 自定义映射
-p 9000:8000
访问: http://localhost:9000
```

### 局域网/远程访问

#### 获取访问地址

```bash
# macOS - 获取本机 IP
ipconfig getifaddr en0
# 输出: 192.168.1.100

# Linux
hostname -I | awk '{print $1}'
# 输出: 192.168.1.100

# Windows
ipconfig | findstr IPv4
# 输出: 192.168.1.100
```

#### 访问方式

```bash
# 同一局域网内的其他设备访问
http://192.168.1.100:8000        # Web UI
http://192.168.1.100:8000/generate  # API
```

### 完整示例

#### Web UI 流程
```
1. 打开浏览器 → http://localhost:8000
2. 点击 "Enable Microphone" → 允许权限
3. 点击 "Record" → 录制第 1 段
4. 重复步骤 3 → 录制第 2、3 段
5. 输入模型名 → "my-wakeword"
6. 点击 "Submit" → 等待处理
7. 点击 "Save Model" → 下载 my-wakeword.pmdl
```

#### API 批量处理流程
```bash
#!/bin/bash
# 批量生成多个唤醒词模型

models=(
  "wakeword1:voice1a.wav:voice1b.wav:voice1c.wav"
  "wakeword2:voice2a.wav:voice2b.wav:voice2c.wav"
)

for model_data in "${models[@]}"; do
  IFS=':' read -r name f1 f2 f3 <<< "$model_data"
  
  curl -X POST http://localhost:8000/generate \
    -F "modelName=$name" \
    -F "example1=@$f1" \
    -F "example2=@$f2" \
    -F "example3=@$f3" \
    -o "${name}.pmdl"
  
  echo "✓ Generated: ${name}.pmdl"
done
```

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
- macOS: 系统偏好设置 → 安全性与隐私 → 麦克风

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

