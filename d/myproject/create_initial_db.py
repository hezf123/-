# create_initial_db.py - 创建初始数据库
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from driveManageSystem.models import Coach

def create_initial_database():
    """创建初始数据库"""
    print("正在创建初始数据库...")
    
    # 1. 确保迁移
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'migrate'])
    
    # 2. 创建管理员账户
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✓ 创建管理员: admin/admin123")
    else:
        print("✓ 管理员已存在")
    
    # 3. 创建示例教练（可选）
    if not Coach.objects.exists():
        Coach.objects.create(name='张教练', phone='13800138000')
        Coach.objects.create(name='李教练', phone='13900139000')
        print("✓ 创建示例教练数据")
    
    # 4. 保存为初始数据库
    import shutil
    from django.conf import settings
    
    source_db = settings.DATABASES['default']['NAME']
    target_db = '初始数据库.db'
    
    shutil.copy2(source_db, target_db)
    print(f"✓ 初始数据库已保存为: {target_db}")
    print(f"  文件大小: {os.path.getsize(target_db) / 1024:.1f} KB")
    
    return target_db

if __name__ == '__main__':
    create_initial_database()
    input("\n按任意键退出...")