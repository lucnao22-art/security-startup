# file: config/settings.py

from pathlib import Path
import os
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key' # Thay key của bạn vào đây

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'admin_reorder',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django_bootstrap5',
    
    # Các app của chúng ta
    'backup_restore.apps.BackupRestoreConfig',
    'dashboard.apps.DashboardConfig',
    'accounting.apps.AccountingConfig',
    'inspection.apps.InspectionConfig',
    'inventory.apps.InventoryConfig',
    'operations.apps.OperationsConfig',
    'clients.apps.ClientsConfig',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'vi'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_TZ = True

DATE_FORMAT = 'd/m/Y'
DATE_INPUT_FORMATS = ['%d/%m/%Y']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- CẤU HÌNH GIAO DIỆN ADMIN ---

ADMIN_REORDER = (
    {'app': 'operations', 'label': 'Quản lý Vận hành', 'models': (
        'operations.PhanCongCaTruc',
        'operations.CaLamViec',
        'operations.ChamCong',
        'operations.BaoCaoSuCo',
    )},
     {'app': 'users', 'label': 'Quản lý Nhân sự', 'models': (
        'users.NhanVien',
        'users.PhongBan',
        'users.ChungChi',
        'users.LichSuCongTac',
        'users.CauHinhMaNhanVien',
    )},
    {'app': 'clients', 'label': 'Quản lý Khách hàng & Hợp đồng', 'models': ('clients.KhachHang', 'clients.HopDong', 'clients.MucTieu')},
    {'app': 'inventory', 'label': 'Quản lý Kho & Tài sản'},
    {'app': 'inspection', 'label': 'Thanh tra & Đào tạo'},
    {'app': 'accounting', 'label': 'Kế toán & Tài chính'},
    {'app': 'auth', 'label': 'Xác thực & Ủy quyền', 'models': ('auth.User', 'auth.Group')},
)

JAZZMIN_SETTINGS = {
    "site_title": "A2T Security",
    "site_header": "Hệ thống Quản lý Vận hành",
    "site_brand": "A2T Security",
    "site_logo": None,
    "welcome_sign": "Chào mừng đến với Hệ thống Quản lý Vận hành",
    "copyright": "Công ty Bảo vệ XYZ Ltd",
}

# --- CẤU HÌNH CELERY ---
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_BEAT_SCHEDULE = {
    'escalate-reports-every-5-minutes': {
        'task': 'operations.tasks.check_and_escalate_reports',
        'schedule': crontab(minute='*/5'),
    },
}