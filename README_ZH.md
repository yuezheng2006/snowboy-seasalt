# Snowboy 个人唤醒词录制器

> 🎙️ 在浏览器中录制您自己的 Snowboy 唤醒词模型

## 快速开始

### Docker 部署（推荐）

```bash
# 直接运行
docker run -it --rm -p 8000:8000 rhasspy/snowboy-seasalt

# 或使用 Docker Compose
docker compose up -d
```

访问：http://localhost:8000

### 本地运行

```bash
# 安装依赖
pip3 install -r requirements.txt

# 启动服务
python3 start.py
```

**系统要求：** Python 3.7+, ffmpeg, macOS/Linux (x86_64)

## 使用方法

1. **启用麦克风** - 点击"启用麦克风"并允许权限
2. **录制 3 段音频** - 清晰地说出唤醒词，每次 3 秒
3. **输入模型名称** - 使用拼音或英文命名
4. **提交并下载** - 生成 `.pmdl` 模型文件

### 录音技巧

- ✅ 在安静环境录制，保持音量一致
- ✅ 距离麦克风 20-30cm
- ❌ 避免背景噪音和杂音

### 唤醒词建议

- **中文：** 2-4 个字，如 `你好小智`、`打开助手`
- **英文：** 2-3 个词，如 `Hey Jarvis`、`Computer`

## API 使用

```bash
# 生成中文唤醒词模型
curl -X POST http://localhost:8000/generate \
  -F "modelName=nihao-xiaozhi" \
  -F "lang=zh" \
  -F "example1=@voice1.wav" \
  -F "example2=@voice2.wav" \
  -F "example3=@voice3.wav" \
  -o model.pmdl
```

**参数说明：**
- `modelName` - 模型名称（必需）
- `lang` - 语言代码：`zh` 中文，`en` 英文（默认）
- `example1/2/3` - 3 段音频文件（必需）
- `noTrim` - 是否跳过静音裁剪（可选）

## 故障排除

### 麦克风无法启用
- 使用 Chrome/Edge 浏览器
- 检查浏览器麦克风权限
- 访问 `localhost` 而非 IP 地址

### Docker 构建失败
```bash
# 清理缓存重新构建
docker system prune -a
docker build --no-cache -t rhasspy/snowboy-seasalt .
```

### 端口被占用
```bash
# 使用其他端口
docker run -p 9000:8000 rhasspy/snowboy-seasalt
```

## 更多文档

- [English README](README.md)
- [Docker 部署详细指南](DOCKER.md)
- [GitHub Issues](https://github.com/rhasspy/snowboy-seasalt/issues)

## 许可证

MIT License - 基于 [Snowboy](https://github.com/Kitt-AI/snowboy) 和 [Rhasspy](https://rhasspy.readthedocs.io/)
