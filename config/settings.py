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
    # ĐƯA JAZZMIN LÊN TRÊN, NGAY TRƯỚC ADMIN
    'jazzmin',
    'django.contrib.admin',

    # CÁC APP CÒN LẠI CỦA DJANGO
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # CÁC THƯ VIỆN BÊN THỨ BA
    'debug_toolbar',
    'import_export',
    'admin_reorder',  # <--- admin_reorder nằm sau admin và jazzmin
    'tailwind',
    'theme',
    'django_bootstrap5',
    'phonenumber_field',

    # CÁC APP CỦA BẠN
    'main.apps.MainConfig',
    'users.apps.UsersConfig',
    'clients.apps.ClientsConfig',
    'operations.apps.OperationsConfig',
    'inventory.apps.InventoryConfig',
    'inspection.apps.InspectionConfig',
    'accounting.apps.AccountingConfig',
    'workflow.apps.WorkflowConfig',
    'notifications.apps.NotificationsConfig',
    'backup_restore.apps.BackupRestoreConfig',
    'reports.apps.ReportsConfig',
    'dashboard.apps.DashboardConfig',
    'mobile.apps.MobileConfig',
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
ASGI_APPLICATION = "config.routing.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = '/mobile/login/'
LOGIN_REDIRECT_URL = '/dashboard/'  # <-- THÊM DÒNG NÀY
PHONENUMBER_DEFAULT_REGION = "VN"

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
PHONENUMBER_DEFAULT_REGION = "VN"
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
NPM_BIN_PATH = config('NPM_BIN_PATH', default='npm')

# ==============================================================================
# 11. CẤU HÌNH GIAO DIỆN ADMIN (JAZZMIN)
# ==============================================================================
JAZZMIN_SETTINGS = {
    "site_title": "Security Admin",
    "site_header": "Security Admin",
    "site_brand": "Security Admin",
    "site_logo": "img/logo_moi.png",
    "login_logo": "img/logo_moi.png",
    "login_logo_dark": "img/logo_moi.png",
    "site_logo_classes": "img-circle",
    "site_icon": "img/logo_moi.png",
    "welcome_sign": "Chào mừng đến với Security Admin",
    "copyright": "Security Startup Ltd",
    "search_model": ["users.NhanVien", "clients.MucTieu"],

    "topmenu_links": [
        {"name": "Trang chủ", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"app": "operations", "permissions": ["operations.view_phancongcatruc"]},
    ],

    "usermenu_links": [
        {"model": "users.user"}
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],

    "order_with_respect_to": ["users", "clients", "operations", "inventory", "inspection", "reports", "accounting"],

    "icons": {
        "auth": "fas fa-users-cog",
        "users.User": "fas fa-user",
        "users.Group": "fas fa-users",
        "users.phongban": "fas fa-building",
        "users.chucdanh": "fas fa-id-badge",
        "users.nhanvien": "fas fa-users",
        "users.chungchi": "fas fa-certificate",

        "clients.khachhangtiemnang": "fas fa-user-tie",
        "clients.cohoikinhdoanh": "fas fa-lightbulb",
        "clients.hopdong": "fas fa-file-signature",
        "clients.muctieu": "fas fa-bullseye",

        "operations.vitrichot": "fas fa-map-marker-alt",
        "operations.calamviec": "fas fa-clock",
        "operations.phancongcatruc": "fas fa-calendar-alt",
        "operations.chamcong": "fas fa-check-circle",
        "operations.baocaosuco": "fas fa-exclamation-triangle",
        "operations.baocaodexuat": "fas fa-file-alt",
    },

    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "related_modal_active": True,

    "custom_css": "admin/custom_admin.css",
    "custom_js": None,
    "show_ui_builder": True,

    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"users.user": "collapsible", "auth.group": "vertical_tabs"},
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
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
