# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_persistent.py'],  # 使用新的入口文件
    pathex=[],
    binaries=[],
    datas=[
        ('myproject', 'myproject'),
        ('driveManageSystem', 'driveManageSystem'),
        ('初始数据库.db', '.'),  # 包含初始数据库
        ('myproject/settings.py', '.'),
        ('myproject/urls.py', '.'),
        ('myproject/wsgi.py', '.'),
    ],
    hiddenimports=[
        # Django核心
        'django',
        'django.core',
        'django.core.management',
        'django.core.handlers',
        'django.core.handlers.wsgi',
        'django.core.handlers.base',
        
        # Django应用
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        
        # 自定义应用
        'driveManageSystem',
        'driveManageSystem.apps',
        
        # 依赖
        'asgiref',
        'sqlparse',
        'tzdata',
        
        # 如果需要Excel导出，添加openpyxl
        # 'openpyxl',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],  # 移除这一行，或者正确指定路径
    excludes=['numpy'],  # 排除numpy避免兼容问题
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='驾校管理系统_持久化版',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 显示控制台查看日志
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='驾校管理系统_持久化版'
)