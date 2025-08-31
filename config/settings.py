from pathlib import Path
from decouple import config

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

INSTALLED_APPS = [
    "daphne",
    "channels",
    "main.apps.MainConfig",
    "import_export",
    "jazzmin",
    "admin_reorder",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_bootstrap5",
    "dashboard.apps.DashboardConfig",
    "accounting.apps.AccountingConfig",
    "inspection.apps.InspectionConfig",
    "inventory.apps.InventoryConfig",
    "operations.apps.OperationsConfig",
    "clients.apps.ClientsConfig",
    "users.apps.UsersConfig",
    "backup_restore.apps.BackupRestoreConfig",
    "notifications.apps.NotificationsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
]

ROOT_URLCONF = "config.urls"

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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "vi"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "homepage"
LOGIN_REDIRECT_URL = "dashboard_hub"
LOGOUT_REDIRECT_URL = "homepage"

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

ASGI_APPLICATION = "config.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    },
}

JAZZMIN_SETTINGS = {
    "site_title": "Hệ thống Quản lý",
    "site_header": "Admin",
    "site_brand": "Quản trị",
    "welcome_sign": "Chào mừng đến với Hệ thống Quản lý Vận hành",
    "copyright": "Bảo vệ XYZ Ltd",
}

# --- KHỐI CẤU HÌNH CÒN THIẾU ĐÃ ĐƯỢC BỔ SUNG ---
ADMIN_REORDER = (
    # Cấu hình hệ thống
    {"app": "main", "label": "Cấu hình Hệ thống"},
    # Quản lý nhân sự
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
    # Quản lý vận hành
    {"app": "operations", "label": "Quản lý Vận hành"},
    # Quản lý khách hàng
    {"app": "clients", "label": "Quản lý Khách hàng & Hợp đồng"},
    # Quản lý kho
    {"app": "inventory", "label": "Quản lý Kho & Tài sản"},
    # Thanh tra
    {"app": "inspection", "label": "Thanh tra & Đào tạo"},
    # Kế toán
    {"app": "accounting", "label": "Kế toán & Tài chính"},
    # Quyền
    {
        "app": "auth",
        "label": "Xác thực & Ủy quyền",
        "models": ("auth.User", "auth.Group"),
    },
)
