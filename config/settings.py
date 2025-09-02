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

INSTALLED_APPS = [
    # --- SỬA LỖI Ở ĐÂY: ĐƯA JAZZMIN LÊN TRÊN CÙNG ---
    'jazzmin',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Các ứng dụng của bên thứ ba
    'django_bootstrap5',
    'import_export',
    'weasyprint',

    # Các ứng dụng của bạn
    'main',
    'users',
    'dashboard',
    'clients',
    'operations',
    'inspection',
    'inventory',
    'accounting',
    'notifications',
    'backup_restore',
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
        # SỬA LỖI Ở ĐÂY: Thêm dòng BASE_DIR / "templates"
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Thêm context processor của bạn
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
# --- THÊM CÁC DÒNG ĐỊNH DẠNG NGÀY THÁNG DƯỚI ĐÂY ---

# Định dạng hiển thị ngày tháng năm
DATE_FORMAT = "d/m/Y"

# Định dạng hiển thị ngày giờ
DATETIME_FORMAT = "H:i d/m/Y"

# Các định dạng mà Django sẽ chấp nhận khi người dùng nhập liệu vào form
DATE_INPUT_FORMATS = [
    "%d/%m/%Y",  # '25/10/2025'
    "%Y-%m-%d",  # '2025-10-25' (vẫn chấp nhận định dạng cũ để không gây lỗi)
]

DATETIME_INPUT_FORMATS = [
    "%H:%M %d/%m/%Y",  # '14:30 25/10/2025'
    "%Y-%m-%d %H:%M:%S", # '2025-10-25 14:30:59'
]

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]    
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "homepage"
LOGIN_REDIRECT_URL = "/hub/"
LOGOUT_REDIRECT_URL = "/"

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
    # Title trên tab trình duyệt (có thể để trống để dùng site_title)
    "site_title": "Security Corp Admin",

    # Title trên góc trái trên cùng (có thể dài hơn)
    "site_header": "SECURITY CORP",

    # Title trên trang đăng nhập (thường ngắn)
    "site_brand": "SECURITY CORP",

    # Logo cho trang đăng nhập
    "login_logo": "img/company_logo.png", # Đường dẫn trong thư mục static

    # Logo cho theme tối
    "login_logo_dark": "img/company_logo.png",

    # CSS class để áp dụng cho logo
    "site_logo_classes": "img-circle",

    # Chào mừng trên trang đăng nhập
    "welcome_sign": "Chào mừng đến với Hệ thống Quản lý An ninh",

    # Copyright ở footer
    "copyright": "Security Corp Ltd",

    # Giao diện
    "theme": "darkly", # Sử dụng theme "darkly" có sẵn, rất chuyên nghiệp

    # CSS tùy chỉnh để tinh chỉnh thêm
    "custom_css": "css/login_styles.css",
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
# ==============================================================================
# LOGGING CONFIGURATION (CẤU HÌNH GHI NHẬT KÝ)
# ==============================================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # Định dạng của dòng log
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
    # Nơi xử lý và xuất log ra (console, file, ...)
    "handlers": {
        # Ghi log ra màn hình console
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        # Ghi log vào file, tự động xoay vòng khi file đầy
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "debug.log"), # Tên file log
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 2, # Giữ lại 2 file backup
            "formatter": "verbose",
        },
    },
    # Bộ ghi log chính của ứng dụng
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO", # Mức log cho Django, có thể đổi thành WARNING trên production
            "propagate": True,
        },
        # Logger cho các ứng dụng của bạn (users, operations, ...)
        "my_project_logger": {
            "handlers": ["console", "file"],
            "level": "DEBUG", # Ghi lại tất cả các cấp độ log
            "propagate": True,
        },
    },
}