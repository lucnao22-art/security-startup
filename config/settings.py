# file: config/settings.py

from pathlib import Path
import os
import dj_database_url
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-default-secret-key')

# DEBUG will be False in production (on Render), True on your local machine
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []

# Get the hostname from Render's environment variable
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition
INSTALLED_APPS = [
    'core.apps.CoreConfig', # Thêm dòng này
    'import_export',
    'jazzmin',
    'admin_reorder',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'dashboard.apps.DashboardConfig',
    'accounting.apps.AccountingConfig',
    'inspection.apps.InspectionConfig',
    'inventory.apps.InventoryConfig',
    'operations.apps.OperationsConfig',
    'clients.apps.ClientsConfig',
    'users.apps.UsersConfig',
    'backup_restore.apps.BackupRestoreConfig',
    'notifications.apps.NotificationsConfig', # Thêm dòng này
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Thêm Whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True
DATE_FORMAT = 'd/m/Y'
DATE_INPUT_FORMATS = ['%d/%m/%Y']

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CẤU HÌNH GIAO DIỆN ADMIN ---
ADMIN_REORDER = (
    {'app': 'operations', 'label': 'Quản lý Vận hành'},
    {'app': 'users', 'label': 'Quản lý Nhân sự', 'models': ('users.NhanVien', 'users.PhongBan', 'users.ChungChi', 'users.LichSuCongTac', 'users.CauHinhMaNhanVien')},
    {'app': 'clients', 'label': 'Quản lý Khách hàng & Hợp đồng'},
    {'app': 'inventory', 'label': 'Quản lý Kho & Tài sản'},
    {'app': 'inspection', 'label': 'Thanh tra & Đào tạo'},
    {'app': 'accounting', 'label': 'Kế toán & Tài chính'},
    {'app': 'auth', 'label': 'Xác thực & Ủy quyền', 'models': ('auth.User', 'auth.Group')},
)

JAZZMIN_SETTINGS = {
    "site_title": "Bảo vệ XYZ",
    "site_header": "Bảo vệ XYZ",
    "site_brand": "Bảo vệ XYZ",
    "welcome_sign": "Chào mừng đến với Hệ thống Quản lý Vận hành",
    "copyright": "Bảo vệ XYZ Ltd",
    "topmenu_links": [
        {"name": "Trang chủ",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Xếp lịch", "url": "operations:xep-lich", "permissions": ["auth.view_user"]},
    ],
    "show_ui_builder": True, # Cho phép tùy chỉnh giao diện trực tiếp
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
}

# --- CẤU HÌNH CELERY ---
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_BEAT_SCHEDULE = {
    'escalate-reports-every-5-minutes': {
        'task': 'operations.tasks.check_and_escalate_reports',
        'schedule': crontab(minute='*/5'),
    },
    'check-certs-daily': {
        'task': 'operations.tasks.check_expired_certificates',
        'schedule': crontab(hour=8, minute=0), # Chạy vào 8h sáng mỗi ngày
    },
    'check-shifts-daily': {
        'task': 'operations.tasks.check_unassigned_shifts',
        'schedule': crontab(hour=17, minute=0), # Chạy vào 5h chiều mỗi ngày
    },
      'check-contracts-daily': {
        'task': 'notifications.tasks.check_expiring_contracts',
        'schedule': crontab(hour=8, minute=30), # Chạy vào 8h30 sáng mỗi ngày
    },
}