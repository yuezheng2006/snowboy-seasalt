#!/usr/bin/env python3
"""
跨平台启动脚本 - Snowboy Personal Wake Word Recorder
支持 Windows, macOS, Linux
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(msg):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{msg:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_info(msg):
    print(f"{Colors.OKBLUE}ℹ {msg}{Colors.ENDC}")

def print_success(msg):
    print(f"{Colors.OKGREEN}✓ {msg}{Colors.ENDC}")

def print_warning(msg):
    print(f"{Colors.WARNING}⚠ {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.FAIL}✗ {msg}{Colors.ENDC}")

def check_python_version():
    """检查 Python 版本"""
    print_info("检查 Python 版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print_error(f"需要 Python 3.7+，当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    print_success(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    return True

def check_platform():
    """检查操作系统平台"""
    system = platform.system()
    machine = platform.machine()
    print_info(f"操作系统: {system} ({machine})")
    
    if system == "Windows":
        print_warning("⚠️  Windows 系统不支持 Snowboy 原生库")
        print_warning("   请使用以下方式之一:")
        print_warning("   1. Docker: docker run -it -p 8000:8000 rhasspy/snowboy-seasalt")
        print_warning("   2. WSL2: 在 Windows Subsystem for Linux 中运行")
        return False
    elif system == "Darwin":
        print_success("支持 macOS 平台")
        return True
    elif system == "Linux":
        if "x86_64" in machine or "amd64" in machine:
            print_success("支持 Linux x86_64 平台")
            return True
        else:
            print_error(f"不支持的 Linux 架构: {machine}")
            print_warning("仅支持 x86_64/amd64 架构")
            return False
    else:
        print_error(f"不支持的操作系统: {system}")
        return False

def check_ffmpeg():
    """检查 ffmpeg 是否安装"""
    print_info("检查 ffmpeg...")
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print_success(f"ffmpeg 已安装: {version}")
            return True
    except FileNotFoundError:
        pass
    
    print_error("未安装 ffmpeg")
    system = platform.system()
    if system == "Darwin":
        print_info("安装方法: brew install ffmpeg")
    elif system == "Linux":
        print_info("安装方法: sudo apt-get install ffmpeg")
    return False

def setup_virtualenv():
    """创建或激活虚拟环境"""
    project_root = Path(__file__).parent
    venv_path = project_root / ".venv"
    
    if venv_path.exists():
        print_success("虚拟环境已存在")
        return str(venv_path)
    
    print_info("创建虚拟环境...")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print_success("虚拟环境创建成功")
        return str(venv_path)
    except subprocess.CalledProcessError as e:
        print_error(f"创建虚拟环境失败: {e}")
        return None

def install_dependencies(venv_path):
    """安装依赖包"""
    project_root = Path(__file__).parent
    requirements = project_root / "requirements.txt"
    
    if not requirements.exists():
        print_error("找不到 requirements.txt")
        return False
    
    print_info("检查依赖包...")
    
    # 获取 pip 路径
    if platform.system() == "Windows":
        pip_path = Path(venv_path) / "Scripts" / "pip.exe"
    else:
        pip_path = Path(venv_path) / "bin" / "pip"
    
    if not pip_path.exists():
        print_error(f"找不到 pip: {pip_path}")
        return False
    
    # 检查是否需要安装
    try:
        result = subprocess.run(
            [str(pip_path), "list"],
            capture_output=True,
            text=True
        )
        installed = result.stdout
        
        # 简单检查关键包
        if "quart" in installed and "hypercorn" in installed:
            print_success("依赖包已安装")
            return True
    except Exception:
        pass
    
    print_info("安装依赖包（可能需要几分钟）...")
    try:
        subprocess.run(
            [str(pip_path), "install", "-r", str(requirements)],
            check=True
        )
        print_success("依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"安装依赖包失败: {e}")
        return False

def start_server(venv_path, host="0.0.0.0", port=8000):
    """启动 Web 服务器"""
    project_root = Path(__file__).parent
    
    # 获取 Python 路径
    if platform.system() == "Windows":
        python_path = Path(venv_path) / "Scripts" / "python.exe"
    else:
        python_path = Path(venv_path) / "bin" / "python"
    
    print_header("启动服务器")
    print_info(f"地址: http://localhost:{port}")
    print_info("按 Ctrl+C 停止服务器\n")
    
    # 设置环境变量
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)
    
    try:
        subprocess.run(
            [str(python_path), "-m", "web", "--host", host, "--port", str(port)],
            cwd=str(project_root),
            env=env
        )
    except KeyboardInterrupt:
        print_info("\n服务器已停止")
    except Exception as e:
        print_error(f"启动失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print_header("Snowboy Personal Wake Word Recorder - 启动器")
    
    # 检查 Python 版本
    if not check_python_version():
        sys.exit(1)
    
    # 检查平台
    if not check_platform():
        sys.exit(1)
    
    # 检查 ffmpeg
    ffmpeg_ok = check_ffmpeg()
    if not ffmpeg_ok:
        print_warning("没有 ffmpeg 将无法处理音频，请先安装")
        response = input("\n是否继续？(y/n): ").strip().lower()
        if response != 'y':
            sys.exit(1)
    
    # 设置虚拟环境
    venv_path = setup_virtualenv()
    if not venv_path:
        sys.exit(1)
    
    # 安装依赖
    if not install_dependencies(venv_path):
        sys.exit(1)
    
    # 启动服务器
    start_server(venv_path)

if __name__ == "__main__":
    main()

