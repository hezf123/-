"""
乔创驾校管理系统 - 持久化数据版本
数据库保存在程序所在目录的data文件夹中
支持自动备份和数据恢复
"""

import os
import sys
import webbrowser
import threading
import time
import shutil
import sqlite3
from django.core.management import execute_from_command_line

# ==================== 配置部分 ====================
CONFIG = {
    'data_dir_name': 'data',           # 数据目录名
    'backup_dir_name': 'backup',       # 备份目录名
    'initial_db_name': '初始数据库.db', # 初始数据库文件名
    'backup_keep_days': 7,             # 保留最近7天备份
    'auto_backup': True,               # 是否自动备份
}

# ==================== 工具函数 ====================
def get_application_path():
    """获取应用程序路径"""
    if getattr(sys, 'frozen', False):
        # 打包后的exe：返回exe所在目录
        return os.path.dirname(sys.executable)
    else:
        # 开发环境：返回脚本所在目录
        return os.path.dirname(os.path.abspath(__file__))

def ensure_directories():
    """确保所有必要的目录存在"""
    base_dir = get_application_path()
    
    directories = {
        'data': os.path.join(base_dir, CONFIG['data_dir_name']),
        'backup': os.path.join(base_dir, CONFIG['backup_dir_name']),
        'logs': os.path.join(base_dir, 'logs'),
    }
    
    for name, path in directories.items():
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"[目录] 创建 {name} 目录: {path}")
    
    return directories

def get_initial_database_path():
    """获取初始数据库路径"""
    base_dir = get_application_path()
    
    # 1. 先检查程序目录下的初始数据库
    app_dir_db = os.path.join(base_dir, CONFIG['initial_db_name'])
    if os.path.exists(app_dir_db):
        return app_dir_db
    
    # 2. 检查临时目录（打包环境）
    if hasattr(sys, '_MEIPASS'):
        temp_db = os.path.join(sys._MEIPASS, CONFIG['initial_db_name'])
        if os.path.exists(temp_db):
            return temp_db
    
    return None

def initialize_database(target_db_path):
    """初始化数据库"""
    initial_db = get_initial_database_path()
    
    if initial_db and os.path.exists(initial_db):
        # 从初始数据库复制
        shutil.copy2(initial_db, target_db_path)
        print(f"[数据库] 从初始数据库创建: {target_db_path}")
        return True
    else:
        # 创建全新的数据库
        try:
            conn = sqlite3.connect(target_db_path)
            conn.close()
            print(f"[数据库] 创建新的空数据库: {target_db_path}")
            return True
        except Exception as e:
            print(f"[错误] 创建数据库失败: {e}")
            return False

def setup_database():
    """设置数据库路径，确保数据持久化"""
    directories = ensure_directories()
    data_dir = directories['data']
    backup_dir = directories['backup']
    
    # 数据库文件路径
    db_path = os.path.join(data_dir, 'db.sqlite3')
    
    # 检查数据库是否存在
    if not os.path.exists(db_path):
        print(f"[数据库] 未找到现有数据库，正在初始化...")
        if not initialize_database(db_path):
            print(f"[错误] 数据库初始化失败！")
            return None, directories
    
    # 设置环境变量，让Django使用这个数据库
    os.environ['DJANGO_DB_PATH'] = db_path
    os.environ['DJANGO_DATA_DIR'] = data_dir
    os.environ['DJANGO_BACKUP_DIR'] = backup_dir
    
    print(f"[数据库] 使用数据库: {db_path}")
    print(f"[目录] 数据目录: {data_dir}")
    print(f"[目录] 备份目录: {backup_dir}")
    
    return db_path, directories

def perform_auto_backup(db_path, backup_dir):
    """执行自动备份"""
    if not CONFIG['auto_backup'] or not os.path.exists(db_path):
        return
    
    try:
        import datetime
        today = datetime.date.today().strftime('%Y%m%d')
        backup_file = os.path.join(backup_dir, f'backup_{today}.sqlite3')
        
        # 如果今天还没有备份
        if not os.path.exists(backup_file):
            shutil.copy2(db_path, backup_file)
            print(f"[备份] 创建每日备份: {backup_file}")
            
            # 清理旧备份
            cleanup_old_backups(backup_dir)
    except Exception as e:
        print(f"[警告] 自动备份失败: {e}")

def cleanup_old_backups(backup_dir):
    """清理旧备份文件"""
    try:
        import datetime
        backup_files = []
        
        # 收集所有备份文件
        for filename in os.listdir(backup_dir):
            if filename.startswith('backup_') and filename.endswith('.sqlite3'):
                filepath = os.path.join(backup_dir, filename)
                backup_files.append((filepath, os.path.getctime(filepath)))
        
        # 按创建时间排序
        backup_files.sort(key=lambda x: x[1])
        
        # 删除超过保留天数的旧备份
        keep_count = CONFIG['backup_keep_days']
        if len(backup_files) > keep_count:
            for filepath, _ in backup_files[:-keep_count]:
                os.remove(filepath)
                print(f"[清理] 删除旧备份: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"[警告] 清理备份失败: {e}")

def create_backup_tool():
    """创建备份工具脚本"""
    base_dir = get_application_path()
    tool_path = os.path.join(base_dir, '数据备份工具.bat')
    
    tool_content = '''@echo off
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
'''
    
    with open(tool_path, 'w', encoding='utf-8') as f:
        f.write(tool_content)
    
    print(f"[工具] 创建备份工具: {tool_path}")
    return tool_path

# ==================== 主函数 ====================
def open_browser():
    """打开浏览器"""
    time.sleep(4)  # 给Django更多启动时间
    try:
        webbrowser.open('http://127.0.0.1:8000/admin/')
        print(f"[浏览器] 已尝试打开管理后台")
    except Exception as e:
        print(f"[警告] 打开浏览器失败: {e}")
        print(f"[提示] 请手动访问: http://127.0.0.1:8000/admin/")

def print_welcome():
    """打印欢迎信息"""
    print("=" * 60)
    print("       乔创驾校管理系统 - 持久化数据版本 V1.1")
    print("=" * 60)
    print("特点：")
    print("  ✓ 数据永久保存，重启不丢失")
    print("  ✓ 自动每日备份")
    print("  ✓ 支持手动备份恢复")
    print("  ✓ 兼容原有所有功能")
    print("=" * 60)

def main():
    """主入口函数"""
    try:
        # 打印欢迎信息
        print_welcome()
        
        # 1. 设置数据库（确保数据持久化）
        db_info = setup_database()
        if not db_info:
            print("[错误] 数据库设置失败，程序退出")
            input("按任意键退出...")
            return
        
        db_path, directories = db_info
        
        # 2. 执行自动备份
        if CONFIG['auto_backup']:
            perform_auto_backup(db_path, directories['backup'])
        
        # 3. 创建备份工具
        create_backup_tool()
        
        # 4. 设置Django环境
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
        
        # 5. 启动浏览器线程
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # 6. 启动Django服务器
        print("\n" + "=" * 60)
        print("[系统] 正在启动Django服务器...")
        print("[提示] 按 Ctrl+C 停止服务器")
        print("=" * 60 + "\n")
        
        # 使用0.0.0.0而不是127.0.0.1，兼容性更好
        sys.argv = ['manage.py', 'runserver', '0.0.0.0:8000', '--noreload']
        
        execute_from_command_line(sys.argv)
        
    except KeyboardInterrupt:
        print("\n[系统] 收到停止信号，正在关闭...")
    except Exception as e:
        print(f"\n[错误] 程序运行异常: {e}")
        import traceback
        traceback.print_exc()
        input("\n按任意键退出...")

if __name__ == '__main__':
    main()