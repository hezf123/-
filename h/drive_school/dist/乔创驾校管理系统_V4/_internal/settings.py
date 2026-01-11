"""
Django settings for drive_school project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'school_manage',  # 我们的应用
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'drive_school.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'drive_school.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ========== 持久化数据配置 ==========
import os
import sys

def get_database_config():
    """智能获取数据库配置"""
    
    # 优先级1：环境变量指定的路径
    env_db_path = os.environ.get('DJANGO_DB_PATH')
    if env_db_path:
        db_dir = os.path.dirname(env_db_path)
        if os.path.exists(db_dir):
            print(f"[设置] 使用环境变量数据库: {env_db_path}")
            return {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': env_db_path,
                    'OPTIONS': {
                        'timeout': 30,
                    }
                }
            }
    
    # 优先级2：打包环境
    if getattr(sys, 'frozen', False):
        # exe所在目录的data文件夹
        app_dir = os.path.dirname(sys.executable)
        default_db = os.path.join(app_dir, 'data', 'db.sqlite3')
        
        # 确保目录存在
        os.makedirs(os.path.dirname(default_db), exist_ok=True)
        
        print(f"[设置] 使用打包环境数据库: {default_db}")
        return {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': default_db,
                'OPTIONS': {
                    'timeout': 30,
                }
            }
        }
    
    # 优先级3：开发环境
    return DATABASES

# 覆盖DATABASES配置
DATABASES = get_database_config()