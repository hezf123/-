@echo off
chcp 65001 >nul
title 数据备份与恢复工具

echo.
echo    ╔══════════════════════════════════════════╗
echo    ║        数据备份与恢复工具               ║
echo    ╚══════════════════════════════════════════╝
echo.

:menu
echo [1] 立即备份数据库
echo [2] 恢复数据库
echo [3] 查看备份列表
echo [4] 手动清理备份
echo [5] 返回主程序
echo [6] 退出
echo.

choice /c 123456 /n /m "请选择: "

if errorlevel 6 goto :exit
if errorlevel 5 goto :return_main
if errorlevel 4 goto :cleanup
if errorlevel 3 goto :list
if errorlevel 2 goto :restore
if errorlevel 1 goto :backup

:backup
set timestamp=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%
if exist "data\db.sqlite3" (
    copy "data\db.sqlite3" "backup\manual_%timestamp%.sqlite3"
    echo ✓ 手动备份完成: backup\manual_%timestamp%.sqlite3
) else (
    echo ✗ 未找到数据库文件
)
pause
goto :menu

:restore
echo.
echo 可用备份文件：
dir backup\*.sqlite3 /b
echo.
set /p filename="请输入要恢复的文件名: "
if exist "backup\%filename%" (
    copy "data\db.sqlite3" "data\db.sqlite3.bak" 2>nul
    copy "backup\%filename%" "data\db.sqlite3"
    echo ✓ 恢复完成
) else (
    echo ✗ 文件不存在
)
pause
goto :menu

:list
echo.
echo 备份文件列表：
echo.
dir backup\*.sqlite3
echo.
pause
goto :menu

:cleanup
echo.
echo 删除几天前的备份？
echo [1] 删除7天前
echo [2] 删除30天前
echo [3] 删除所有
echo [4] 返回
echo.
choice /c 1234 /n /m "请选择: "
if errorlevel 4 goto :menu
if errorlevel 3 goto :delete_all
if errorlevel 2 goto :delete_30
if errorlevel 1 goto :delete_7

:delete_7
forfiles /p "backup" /m *.sqlite3 /d -7 /c "cmd /c del @path"
echo ✓ 已删除7天前的备份
pause
goto :menu

:delete_30
forfiles /p "backup" /m *.sqlite3 /d -30 /c "cmd /c del @path"
echo ✓ 已删除30天前的备份
pause
goto :menu

:delete_all
del backup\*.sqlite3
echo ✓ 已删除所有备份
pause
goto :menu

:return_main
start "" "启动.bat"
exit

:exit
exit
