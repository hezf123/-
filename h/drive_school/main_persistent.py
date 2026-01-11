"""
乔创驾校管理系统 - 持久化数据版本 V2.0
数据库保存在程序所在目录的data文件夹中
支持自动备份和数据恢复
"""

import os
import sys
import webbrowser
import threading
import time
import shutil
from django.core.management import execute_from_command_line

# ==================== 配置部分 ====================
CONFIG = {
    'data_dir_name': 'data',
    'backup_dir_name': 'backup',
    'initial_db_name': '初始数据库.db',
    'backup_keep_days': 7,
    'auto_backup': True,
}

def get_application_path():
    """获取应用程序路径"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
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

def setup_database():
    """设置数据库路径，确保数据持久化"""
    directories = ensure_directories()
    data_dir = directories['data']
    
    # 数据库文件路径
    db_path = os.path.join(data_dir, 'db.sqlite3')
    
    # 检查数据库是否存在
    if not os.path.exists(db_path):
        print(f"[数据库] 未找到现有数据库，正在初始化...")
        initial_db = get_initial_database_path()
        if initial_db and os.path.exists(initial_db):
            shutil.copy2(initial_db, db_path)
            print(f"[数据库] 从初始数据库创建: {db_path}")
        else:
            print(f"[数据库] 将创建新数据库")
    
    # 设置环境变量，让Django使用这个数据库
    os.environ['DJANGO_DB_PATH'] = db_path
    
    print(f"[数据库] 使用数据库: {db_path}")
    return db_path, directories

def open_browser():
    """打开浏览器并自动修改页面"""
    time.sleep(3)
    try:
        webbrowser.open('http://127.0.0.1:8000/admin/')
        print(f"[浏览器] 已打开管理后台")
        
        # 让程序等一会儿，确保页面加载
        time.sleep(2)
        
        # 尝试用JavaScript修改（如果浏览器支持的话）
        print(f"[提示] 如需修改按钮文字，请在浏览器控制台运行：")
        print(f"       document.body.innerHTML = document.body.innerHTML.replace(/运行/g, '执行').replace(/过滤器/g, '检索')")
        
    except Exception as e:
        print(f"[警告] {e}")
        print(f"[提示] 请手动访问: http://127.0.0.1:8000/admin/")

def print_welcome():
    """打印欢迎信息"""
    print("=" * 60)
    print("       乔创驾校管理系统 V2.0")
    print("       持久化数据版本")
    print("=" * 60)
    print("特点：")
    print("  ✓ 数据永久保存，重启不丢失")
    print("  ✓ 自动每日备份")
    print("  ✓ 简化收费记录管理")
    print("  ✓ 支持资金记录和结算管理")
    print("=" * 60)

def main():
    """主入口函数"""
    try:
        # 打印欢迎信息
        print_welcome()
        
        # 设置数据库（确保数据持久化）
        db_path, directories = setup_database()
        
        # 设置Django环境
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drive_school.settings')
        
        # 修改settings中的数据库路径
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # 启动浏览器线程
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # 启动Django服务器
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