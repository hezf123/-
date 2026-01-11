# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_persistent.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('drive_school', 'drive_school'),
        ('school_manage', 'school_manage'),
        ('初始数据库.db', '.'),
        ('drive_school/settings.py', '.'),
        ('drive_school/urls.py', '.'),
        ('drive_school/wsgi.py', '.'),
        # 添加这行↓↓↓
        ('locale', 'locale'),  # 添加翻译文件
    ],
    hiddenimports=[
        'django',
        'django.core.management',
        'django.core.handlers.wsgi',
        'django.core.handlers.base',
        'django.template.context_processors',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'school_manage',
        'asgiref',
        'sqlparse',
        'tzdata',
        'openpyxl',
        # 导出功能需要的额外模块
        'openpyxl.styles',
        'openpyxl.workbook',
        'openpyxl.writer.excel',
        'openpyxl.cell',
        'openpyxl.utils',
        'openpyxl.worksheet',
        'django.http',
        'django.utils.html',
        # 添加应用的 models 和 admin
        'school_manage.models',
        'school_manage.admin',
        'school_manage.apps',
        # 添加翻译相关
        'django.utils.translation',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='乔创驾校管理系统_V4',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 设置为 False 隐藏控制台窗口
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
    name='乔创驾校管理系统_V4'
)