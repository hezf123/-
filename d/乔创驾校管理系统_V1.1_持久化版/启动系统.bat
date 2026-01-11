@echo off
chcp 65001 >nul
title 乔创驾校管理系统 V1.1 - 持久化版

echo.
echo ==============================================
echo   乔创驾校管理系统 V1.1 - 持久化数据版
echo ==============================================
echo.

echo [版本升级说明]
echo - 数据永久保存，重启不丢失
echo - 自动每日备份，防止数据丢失
echo - 支持手动备份恢复
echo - 保持原有所有功能
echo.

echo [数据存储位置]
echo - 主数据库：本文件夹\data\db.sqlite3
echo - 自动备份：本文件夹\backup\（每日自动备份）
echo - 初始数据：初始数据库.db
echo.

echo 正在启动系统...
echo.

REM 优先使用文件夹版本
if exist "驾校管理系统_持久化版\驾校管理系统_持久化版.exe" (
    echo [INFO] 使用文件夹版本
    cd "驾校管理系统_持久化版"
    start "" "驾校管理系统_持久化版.exe"
    cd ..
) else if exist "驾校管理系统_持久化版.exe" (
    echo [INFO] 使用单文件版本
    start "" "驾校管理系统_持久化版.exe"
) else (
    echo [ERROR] 未找到程序文件！
    echo 请检查文件是否存在。
    pause
    exit /b 1
)

echo.
echo ==============================================
echo  系统启动中，请稍候...
echo.
echo  请等待浏览器自动打开
echo  首次登录信息：
echo     网址：http://127.0.0.1:8000/admin/
echo     用户名：admin
echo     密码：admin123
echo.
echo  重要提示：
echo     - 首次登录后请立即修改密码！
echo     - 所有数据已永久保存到本地
echo     - 不要删除 data 和 backup 文件夹
echo ==============================================
echo.

timeout /t 10 /nobreak >nul

echo 如果系统未启动，请尝试：
echo 1. 右键以管理员身份运行本程序
echo 2. 手动运行程序文件
echo 3. 检查防火墙设置
echo.
echo 技术支持：请查看"联系方式.txt"
echo.
pause