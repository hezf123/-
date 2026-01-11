@echo off
chcp 65001 >nul
title 乔创驾校管理系统

echo.
echo  乔创驾校学员管理系统 V1.0
echo  ============================
echo.

echo 正在启动系统，请稍候...
echo.

if exist "驾校管理系统\驾校管理系统.exe" (
    cd "驾校管理系统"
    start "" "驾校管理系统.exe"
) else (
    start "" "驾校管理系统.exe"
)

echo.
echo 系统启动中...
echo 请等待浏览器自动打开。
echo.
echo 如果浏览器没有自动打开，请手动访问：
echo http://127.0.0.1:8000/admin/
echo.
echo 首次登录：
echo 用户名：admin
echo 密码：admin123
echo.
echo 按任意键查看详细信息...
pause >nul

echo.
echo 使用说明：
echo 1. 系统启动后，请立即修改管理员密码
echo 2. 先添加教练，再添加学员
echo 3. 所有数据保存在本地
echo 4. 定期备份 data/db.sqlite3 文件
echo.
echo 技术支持：[你的联系方式]
echo.
pause