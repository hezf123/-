@echo off
chcp 65001 > nul
title 乔创驾校管理系统 V4.0

echo.
echo 正在启动乔创驾校管理系统...
echo.

REM 设置环境变量
set DJANGO_SETTINGS_MODULE=drive_school.settings
set PYTHONPATH=.

REM 启动程序
"乔创驾校管理系统_V4.exe"

echo.
echo 系统已启动！
echo 请访问：http://127.0.0.1:8000/admin/
echo 用户名：admin
echo 密码：admin123
echo.
pause