@echo off
chcp 65001 > nul
title 乔创驾校管理系统 V2.0
color 0A

echo.
echo ================================================
echo        乔创驾校学员管理系统 V2.0
echo        持久化数据版本
echo ================================================
echo.

echo [系统信息]
echo - 版本：V2.0 (2024年12月更新)
echo - 特点：数据永久保存，重启不丢失
echo - 功能：学员管理、资金记录、教练结算
echo.

echo [启动选项]
echo 1. 启动主程序 (推荐)
echo 2. 打开数据目录
echo 3. 查看使用说明
echo 4. 备份数据库
echo 5. 退出系统
echo.

set /p choice=请选择 (1-5): 

if "%choice%"=="5" exit
if "%choice%"=="4" goto backup
if "%choice%"=="3" goto help
if "%choice%"=="2" goto open_data
if "%choice%"=="1" goto start_program

:start_program
echo.
echo 正在启动系统，请稍候...
echo.

REM 检查程序文件是否存在
if exist "乔创驾校管理系统_V2.exe" (
    echo [OK] 找到单文件版本，正在启动...
    start "" "乔创驾校管理系统_V2.exe"
    goto show_info
)

if exist "乔创驾校管理系统_V2\乔创驾校管理系统_V2.exe" (
    echo [OK] 找到文件夹版本，正在启动...
    cd "乔创驾校管理系统_V2"
    start "" "乔创驾校管理系统_V2.exe"
    cd ..
    goto show_info
)

echo [ERROR] 错误：未找到程序文件！
echo.
echo 当前目录文件列表：
dir *.exe
echo.
pause
exit

:show_info
echo.
echo ================================================
echo        系统启动中...
echo ================================================
echo.
echo 请等待浏览器自动打开
echo 如果未自动打开，请手动访问：
echo http://127.0.0.1:8000/admin/
echo.
echo 首次登录信息：
echo 用户名：admin
echo 密码：admin123
echo.
echo 数据存储位置：
echo 主数据库：本文件夹\data\db.sqlite3
echo 自动备份：本文件夹\backup\
echo.
echo 重要提示：
echo 1. 首次登录后请立即修改密码！
echo 2. 不要删除 data 和 backup 文件夹
echo 3. 定期检查备份文件
echo ================================================
echo.

timeout /t 15 /nobreak > nul

echo 如果系统未启动，请尝试：
echo 1. 右键以管理员身份运行本程序
echo 2. 直接运行程序文件
echo 3. 检查防火墙设置
echo.
echo 技术支持：请查看"联系方式.txt"
echo.
pause
goto :eof

:open_data
echo.
echo 正在打开数据目录...
if not exist "data" mkdir data
if not exist "backup" mkdir backup
explorer "data"
explorer "backup"
echo [OK] 数据目录已打开
echo.
pause
goto :eof

:help
if exist "使用说明.txt" (
    start "" "使用说明.txt"
) else (
    echo.
    echo 使用说明：
    echo 1. 双击运行 start.bat
    echo 2. 选择"启动主程序"
    echo 3. 等待浏览器打开
    echo 4. 登录管理后台
    echo 5. 开始使用
    echo.
    pause
)
goto :eof

:backup
echo.
echo 数据备份工具
echo =============
echo.

if not exist "data\db.sqlite3" (
    echo [ERROR] 未找到数据库文件！
    pause
    goto :eof
)

if not exist "backup" mkdir backup

set timestamp=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%
copy "data\db.sqlite3" "backup\手动备份_%timestamp%.sqlite3"

echo [OK] 备份完成！
echo 文件：backup\手动备份_%timestamp%.sqlite3
echo.
echo 备份文件列表：
dir backup\*.sqlite3 /b
echo.
pause
goto :eof