#!/usr/bin/env bash
# macOS 和 Linux 启动脚本

set -e

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
}

# 检查 Python 3
check_python() {
    print_info "检查 Python 版本..."
    if ! command -v python3 &> /dev/null; then
        print_error "未找到 Python 3"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python 版本: $PYTHON_VERSION"
}

# 检查 ffmpeg
check_ffmpeg() {
    print_info "检查 ffmpeg..."
    if ! command -v ffmpeg &> /dev/null; then
        print_warning "未安装 ffmpeg"
        if [[ "$OSTYPE" == "darwin"* ]]; then
            print_info "安装方法: brew install ffmpeg"
        else
            print_info "安装方法: sudo apt-get install ffmpeg"
        fi
        read -p "是否继续？(y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_success "ffmpeg 已安装"
    fi
}

# 创建虚拟环境
setup_venv() {
    if [ ! -d ".venv" ]; then
        print_info "创建虚拟环境..."
        python3 -m venv .venv
        print_success "虚拟环境创建成功"
    else
        print_success "虚拟环境已存在"
    fi
    
    # 激活虚拟环境
    source .venv/bin/activate
    print_success "虚拟环境已激活"
}

# 安装依赖
install_deps() {
    print_info "检查依赖包..."
    
    # 升级 pip
    python -m pip install --upgrade pip -q
    
    # 检查关键包是否已安装
    if python -c "import quart" 2>/dev/null && python -c "import hypercorn" 2>/dev/null; then
        print_success "依赖包已安装"
    else
        print_info "安装依赖包..."
        pip install -r requirements.txt
        print_success "依赖包安装完成"
    fi
}

# 启动服务器
start_server() {
    print_header "启动 Snowboy Web 服务器"
    print_info "访问地址: http://localhost:8000"
    print_info "按 Ctrl+C 停止服务器"
    echo ""
    
    # 设置 PYTHONPATH
    export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
    
    # 启动服务器
    python -m web --host 0.0.0.0 --port 8000 "$@"
}

# 主流程
main() {
    print_header "Snowboy Personal Wake Word Recorder"
    
    check_python
    check_ffmpeg
    setup_venv
    install_deps
    start_server "$@"
}

# 运行
main "$@"

