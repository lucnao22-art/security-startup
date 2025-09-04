# config/settings.py

from pathlib import Path
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []

# Lấy giá trị của biến RENDER_EXTERNAL_HOSTNAME từ môi trường
RENDER_HOSTNAME = config("RENDER_EXTERNAL_HOSTNAME", default=None)

if RENDER_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_HOSTNAME)
else:
    # Thêm các host cho môi trường local nếu không tìm thấy biến của Render
    ALLOWED_HOSTS.extend(["localhost", "127.0.0.1"])

# ==============================================================================
# CẤU HÌNH CÁC ỨNG DỤNG (APPS)
# ==============================================================================
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Các ứng dụng của bên thứ ba
    'django_bootstrap5',
    'import_export',
    'weasyprint',
    'admin_reorder',

    # Các ứng dụng của bạn (SỬA LẠI ĐỂ DÙNG APPCONFIG)
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
]


# ==============================================================================
# CẤU HÌNH MIDDLEWARE
# ==============================================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Đặt middleware của admin_reorder ở cuối cùng
    "admin_reorder.middleware.ModelAdminReorder",
]

ROOT_URLCONF = "config.urls"

# ==============================================================================
# CẤU HÌNH TEMPLATES
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

WSGI_APPLICATION = "config.wsgi.application"

# ==============================================================================
# CẤU HÌNH DATABASE
# ==============================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ==============================================================================
# CẤU HÌNH XÁC THỰC MẬT KHẨU
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================================================================
# CẤU HÌNH QUỐC TẾ HÓA (I18N)
# ==============================================================================
LANGUAGE_CODE = "vi"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True

DATE_FORMAT = "d/m/Y"
DATETIME_FORMAT = "H:i d/m/Y"
DATE_INPUT_FORMATS = ["%d/%m/%Y", "%Y-%m-%d"]
DATETIME_INPUT_FORMATS = ["%H:%M %d/%m/%Y", "%Y-%m-%d %H:%M:%S"]

# ==============================================================================
# CẤU HÌNH STATIC & MEDIA FILES
# ==============================================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================================================================
# CẤU HÌNH ĐĂNG NHẬP/ĐĂNG XUẤT
# ==============================================================================
LOGIN_URL = "homepage"
LOGIN_REDIRECT_URL = "/hub/"
LOGOUT_REDIRECT_URL = "/"

# ==============================================================================
# CẤU HÌNH CELERY & CHANNELS
# ==============================================================================
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

ASGI_APPLICATION = "config.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    },
}

# ==============================================================================
# CẤU HÌNH GIAO DIỆN ADMIN (JAZZMIN)
# ==============================================================================
JAZZMIN_SETTINGS = {
    "site_title": "Security Corp Admin",
    "site_header": "SECURITY CORP",
    "site_brand": "SECURITY CORP",
    "login_logo": "img/company_logo.png",
    "login_logo_dark": "img/company_logo.png",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Chào mừng đến với Hệ thống Quản lý An ninh",
    "copyright": "Security Corp Ltd",
    "theme": "darkly",
    "custom_css": "css/login_styles.css",

    "custom_links": {
        "workflow": [
            {
                "name": "Giao việc mới",
                "url": "workflow:task_create",
                "icon": "fas fa-plus",
                "permissions": ["workflow.add_task"]
            },
            {
                "name": "Công việc của tôi",
                "url": "workflow:task_list",
                "icon": "fas fa-tasks"
            },
            {
                "name": "Tạo đề xuất mới",
                "url": "workflow:proposal_create",
                "icon": "fas fa-file-signature"
            },
            {
                "name": "Danh sách đề xuất",
                "url": "workflow:proposal_list",
                "icon": "fas fa-folder-open"
            }
        ]
    },
    
    "icons": {
        "workflow.Task": "fas fa-tasks",
        "workflow.Proposal": "fas fa-file-alt",
    },
}

# ==============================================================================
# CẤU HÌNH SẮP XẾP MENU ADMIN (ADMIN_REORDER)
# ==============================================================================
ADMIN_REORDER = (
    {"app": "main", "label": "Cấu hình Hệ thống"},
    {
        "app": "users",
        "label": "Quản lý Nhân sự",
        "models": (
            "users.NhanVien",
            "users.PhongBan",
            "users.ChucDanh",
            "users.LichSuCongTac",
            "users.CauHinhMaNhanVien",
        ),
    },
    {"app": "workflow", "label": "Quản lý Công việc & Đề xuất"},
    {"app": "operations", "label": "Quản lý Vận hành"},
    {"app": "clients", "label": "Quản lý Khách hàng & Hợp đồng"},
    {"app": "inventory", "label": "Quản lý Kho & Tài sản"},
    {"app": "inspection", "label": "Thanh tra & Đào tạo"},
    {"app": "accounting", "label": "Kế toán & Tài chính"},
    {
        "app": "auth",
        "label": "Xác thực & Ủy quyền",
        "models": ("auth.User", "auth.Group"),
    },
)

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
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
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "my_project_logger": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}