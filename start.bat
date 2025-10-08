@echo off
REM Windows 启动脚本（仅用于显示提示信息）
REM Windows 不支持 Snowboy 原生库，请使用 Docker 或 WSL2

setlocal

echo.
echo ========================================================
echo  Snowboy Personal Wake Word Recorder
echo ========================================================
echo.
echo [31m注意: Windows 系统不支持 Snowboy 原生库[0m
echo.
echo 请使用以下方式之一运行:
echo.
echo 1. [36mDocker (推荐)[0m
echo    docker run -it -p 8000:8000 rhasspy/snowboy-seasalt
echo    然后访问: http://localhost:8000
echo.
echo 2. [36mWSL2 (Windows Subsystem for Linux)[0m
echo    - 在 WSL2 中打开项目目录
echo    - 运行: bash start.sh
echo.
echo 3. [36mDocker Compose[0m
echo    docker-compose up
echo.
echo ========================================================
echo.

pause
endlocal

