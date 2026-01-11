# main.py - 这是程序的入口文件
import os
import sys
import threading
import webbrowser
import time
from django.core.management import execute_from_command_line

def open_browser():
    """程序启动后自动打开浏览器"""
    time.sleep(2)  # 等待Django启动
    webbrowser.open('http://127.0.0.1:8000/admin/')

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    
    # 启动浏览器线程
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # 运行Django服务器
    sys.argv = ['manage.py', 'runserver', '--noreload']
    execute_from_command_line(sys.argv)