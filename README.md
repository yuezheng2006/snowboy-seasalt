# Snowboy Personal Wake Word Recorder

基于 Web 的个人唤醒词录制工具，可生成 Snowboy 的 `.pmdl` 模型文件。

项目基于 [snowboy](https://github.com/Kitt-AI/snowboy) 和 [seasalt-ai](https://github.com/seasalt-ai/snowboy)

---

## 🚀 快速开始

### Docker 部署（推荐）

```bash
docker run -it --rm -p 8000:8000 rhasspy/snowboy-seasalt
```

访问：http://localhost:8000

**详细：** [DOCKER.md](DOCKER.md)

---

### 本地运行

**注意：** Python 3.13 不兼容，需要 Python 3.11/3.12

```bash
./start.sh  # macOS/Linux
```

---

## 系统要求

- **推荐：** Docker（跨平台）
- **本地运行：** Python 3.11/3.12 + ffmpeg
- **浏览器：** Chrome/Edge

## 使用说明

1. 启用麦克风
2. 录制 3 段相同的唤醒词
3. 输入模型名称，提交
4. 下载 `.pmdl` 文件

![截图](screenshot.png)

## HTTP API

```bash
curl -X POST \
    -F modelName=my-wakeword \
    -F example1=@ex1.wav \
    -F example2=@ex2.wav \
    -F example3=@ex3.wav \
    --output my-wakeword.pmdl \
    http://localhost:8000/generate
```

**参数：**
- `modelName` - 模型名称（必需）
- `example1/2/3` - 音频文件（至少 3 个）
- `lang` - 语言（`en`/`zh`，默认 `en`）
