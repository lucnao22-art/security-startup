# file: config/settings.py

from pathlib import Path
from decouple import config
import os

# ==============================================================================
# 1. CẤU HÌNH CƠ BẢN & BẢO MẬT
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = []
RENDER_HOSTNAME = config("RENDER_EXTERNAL_HOSTNAME", default=None)

if RENDER_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_HOSTNAME)
else:
    ALLOWED_HOSTS.extend(["localhost", "127.0.0.1"])

# ==============================================================================
# 2. CẤU HÌNH CÁC ỨNG DỤNG (APPS)
# ==============================================================================
INSTALLED_APPS = [
    'jazzmin',
    'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'import_export',
    'admin_reorder',
    'tailwind',
    'theme',
    'main.apps.MainConfig',
    'users.apps.UsersConfig',
    'dashboard.apps.DashboardConfig',
    'clients.apps.ClientsConfig',
    'operations.apps.OperationsConfig',
    'inspection.apps.InspectionConfig',
    'inventory.apps.InventoryConfig',
    'accounting.apps.AccountingConfig',
    'notifications.apps.NotificationsConfig',
    'backup_restore.apps.BackupRestoreConfig',
    'workflow.apps.WorkflowConfig',
    'reports.apps.ReportsConfig',
]

# ==============================================================================
# 3. CẤU HÌNH MIDDLEWARE
# ==============================================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
]

# ==============================================================================
# 4. CẤU HÌNH URLS, WSGI, ASGI
# ==============================================================================
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================================================================
# 5. CẤU HÌNH TEMPLATES
# ==============================================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "main.context_processors.company_info",
            ],
        },
    },
]

# ==============================================================================
# 6. CẤU HÌNH DATABASE
# ==============================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ==============================================================================
# 7. CẤU HÌNH XÁC THỰC & MẬT KHẨU
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LOGIN_URL = "main:homepage"
LOGIN_REDIRECT_URL = "/hub/"
LOGOUT_REDIRECT_URL = "/"

# ==============================================================================
# 8. CẤU HÌNH QUỐC TẾ HÓA (I18N) & ĐỊNH DẠNG
# ==============================================================================
LANGUAGE_CODE = "vi"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / 'locale']

# ==============================================================================
# 9. CẤU HÌNH STATIC & MEDIA FILES
# ==============================================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ==============================================================================
# 10. CẤU HÌNH CÁC DỊCH VỤ BÊN NGOÀI
# ==============================================================================
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    },
}
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ["127.0.0.1"]
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

# ==============================================================================
# 11. CẤU HÌNH GIAO DIỆN ADMIN (JAZZMIN)
# ==============================================================================
JAZZMIN_SETTINGS = {
    "site_title": "Security Corp Admin",
    "site_header": "SECURITY CORP",
    "site_brand": "SECURITY CORP",
    "welcome_sign": "Chào mừng đến với Hệ thống Quản lý An ninh",
    "copyright": "Security Corp Ltd",
    "theme": "darkly",
    
    "topmenu_links": [
        {"name": "Trang chính",  "url": "/hub/", "permissions": ["auth.view_user"]},
        {"app": "operations"},
        {"app": "clients"},
        {"app": "users"},
        {"app": "workflow"},
    ],
    
    # --- SỬ DỤNG custom_links CỦA JAZZMIN ĐỂ TẠO MENU BÁO CÁO ---
    "custom_links": {
        "reports": [
            {
                "name": "BCC Cá nhân",
                "url": "reports:cham_cong_ca_nhan",
                "icon": "fas fa-user-clock",
            },
            {
                "name": "BCC Mục tiêu",
                "url": "reports:cham_cong_muc_tieu",
                "icon": "fas fa-chart-bar",
            },
        ]
    },
    
    "icons": {
        "auth": "fas fa-users-cog", "auth.user": "fas fa-user", "auth.Group": "fas fa-users",
        "users": "fas fa-id-card",
        "operations": "fas fa-cogs",
        "clients": "fas fa-handshake",
        "reports": "fas fa-print", # Icon cho menu Báo cáo
        "workflow": "fas fa-project-diagram",
        "inventory": "fas fa-boxes",
        "inspection": "fas fa-search",
        "accounting": "fas fa-cash-register",
        "main": "fas fa-globe",
        "backup_restore": "fas fa-database",
    },
}

# ==============================================================================
# 12. CẤU HÌNH SẮP XẾP MENU ADMIN (ADMIN_REORDER)
# ==============================================================================
ADMIN_REORDER = (
    # Nghiệp vụ cốt lõi
    {"app": "operations", "label": "Vận hành & Giám sát"},
    {"app": "users", "label": "Quản lý Nhân sự"},
    {"app": "clients", "label": "Khách hàng & Kinh doanh"},
    {"app": "workflow", "label": "Công việc & Đề xuất"},
    
    # --- ĐƯA APP "reports" VÀO ĐÚNG VỊ TRÍ MONG MUỐN ---
    {"app": "reports", "label": "Báo cáo & Thống kê"},
    
    # Nghiệp vụ hỗ trợ
    {"app": "inspection", "label": "Thanh tra & Tuần tra"},
    {"app": "inventory", "label": "Kho & Vật tư"},
    {"app": "accounting", "label": "Kế toán"},
    
    # Cấu hình hệ thống
    {"app": "main", "label": "Cấu hình Chung"},
    {"app": "backup_restore", "label": "Sao lưu & Phục hồi"},
    {"app": "auth", "label": "Tài khoản & Phân quyền"},
)
# ==============================================================================
# 13. CẤU HÌNH LOGGING
# ==============================================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}", "style": "{",},
        "simple": {"format": "{levelname} {message}", "style": "{",},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple",},
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "debug.log"),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 2,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {"handlers": ["console", "file"], "level": "INFO", "propagate": True,},
    },
}