# file: config/settings.py

import os
from pathlib import Path
import environ
import dj_database_url

# ==============================================================================
# 1. CẤU HÌNH CƠ BẢN & BIẾN MÔI TRƯỜNG
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# Sử dụng django-environ để quản lý các biến môi trường một cách an toàn
env = environ.Env(
    # Đặt giá trị mặc định cho DEBUG là False (an toàn cho production)
    DEBUG=(bool, False)
)

# Đọc file .env chỉ khi nó tồn tại (dành cho môi trường local)
if os.path.exists(os.path.join(BASE_DIR, '.env')):
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# ==============================================================================
# 2. CẤU HÌNH BẢO MẬT
# ==============================================================================
SECRET_KEY = env('SECRET_KEY')

# DEBUG sẽ là True nếu có biến DEBUG=True trong file .env, ngược lại là False
DEBUG = env.bool('DEBUG', default=False)

# Cấu hình ALLOWED_HOSTS linh hoạt cho cả local và production trên Render
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = env('RENDER_EXTERNAL_HOSTNAME', default=None)

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Thêm 'localhost' và '127.0.0.1' vào ALLOWED_HOSTS khi ở chế độ DEBUG
if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])


# ==============================================================================
# 3. CẤU HÌNH CÁC ỨNG DỤNG (APPS)
# ==============================================================================
INSTALLED_APPS = [
    'daphne',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Thư viện bên thứ ba
    'debug_toolbar',
    'django_bootstrap5',
    'import_export',
    'phonenumber_field',
    'tinymce',
    'tailwind',
    'theme',

    # Ứng dụng local
    'main',
    'users',
    'clients',
    'operations',
    'inventory',
    'inspection',
    'accounting',
    'reports',
    'workflow',
    'notifications',
    'backup_restore',
    'mobile',
    'dashboard',
]

# ==============================================================================
# 4. CẤU HÌNH MIDDLEWARE
# ==============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ==============================================================================
# 5. CẤU HÌNH TEMPLATES
# ==============================================================================
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
                'main.context_processors.company_info',
            ],
        },
    },
]

# ==============================================================================
# 6. CẤU HÌNH WSGI & ASGI
# ==============================================================================
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.routing.application'

# ==============================================================================
# 7. CẤU HÌNH CƠ SỞ DỮ LIỆU (DATABASE)
# ==============================================================================
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# ==============================================================================
# 8. CẤU HÌNH XÁC THỰC MẬT KHẨU
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================================================================
# 9. QUỐC TẾ HÓA (INTERNATIONALIZATION)
# ==============================================================================
LANGUAGE_CODE = 'vi-vn'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# 10. CẤU HÌNH TỆP TĨNH (STATIC) & MEDIA
# ==============================================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# SỬA LỖI: Bổ sung cấu hình `default` và `staticfiles` storage
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ==============================================================================
# 11. CÁC CẤU HÌNH KHÁC
# ==============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'operations:mobile_login'
LOGIN_REDIRECT_URL = 'dashboard:dashboard'
LOGOUT_REDIRECT_URL = 'main:homepage'
PHONENUMBER_DEFAULT_REGION = "VN"

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ['127.0.0.1']
NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

# ==============================================================================
# 12. CẤU HÌNH JAZZMIN (GIỮ NGUYÊN TỪ FILE CỦA BẠN)
# ==============================================================================
JAZZMIN_SETTINGS = {
    "site_title": "Hệ Thống Quản Lý",
    "site_header": "Bảo Vệ XYZ",
    "site_brand": "Quản trị viên",
    "site_logo": "img/logo_moi.png",
    "login_logo": "img/logo_moi.png",
    "login_logo_dark": "img/logo_moi.png",
    "site_logo_classes": "img-circle",
    "site_icon": "img/logo_moi.png",
    "welcome_sign": "Chào mừng đến với trang quản trị",
    "copyright": "Bảo Vệ XYZ Ltd",
    "search_model": ["users.NhanVien", "auth.User"],
    "topmenu_links": [
        {"name": "Trang chủ", "url": "index", "permissions": ["auth.view_user"]},
        {"name": "Dashboard", "url": "/dashboard/", "permissions": ["auth.view_user"]},
        {"app": "operations", "name": "Vận hành", "permissions": ["auth.view_user"]},
        {"app": "users", "name": "Nhân sự", "permissions": ["auth.view_user"]},
    ],
    "show_recent_actions": True,
    "custom_links": {
        "main": [
            {
                "name": "Lối tắt cho Quản trị viên",
                "icon": "fas fa-cogs",
                "permissions": ["auth.view_user"],
                "links": [
                    {"name": "+ Thêm người dùng quản trị", "url": "/admin/auth/user/add/", "icon": "fas fa-user-plus", "permissions": ["auth.add_user"]},
                    {"name": "Quản lý Phân quyền", "url": "/admin/auth/group/", "icon": "fas fa-users-cog", "permissions": ["auth.view_group"]},
                    {"name": "Sao lưu & Phục hồi", "url": "/backup/", "icon": "fas fa-database", "permissions": ["auth.view_user"]}
                ]
            }
        ]
    },
    "icons": {
        "auth": "fas fa-users-cog", "auth.user": "fas fa-user", "auth.Group": "fas fa-users",
        "users": "fas fa-id-card", "users.NhanVien": "fas fa-user-tie",
        "users.PhongBan": "fas fa-building", "users.ChucDanh": "fas fa-user-tag",
        "operations": "fas fa-cogs", "operations.BaoCaoSuCo": "fas fa-exclamation-triangle",
        "clients": "fas fa-handshake", "inventory": "fas fa-boxes",
        "inspection": "fas fa-clipboard-check", "accounting": "fas fa-file-invoice-dollar",
        "reports": "fas fa-chart-line", "workflow": "fas fa-project-diagram",
        "notifications": "fas fa-bell", "backup_restore": "fas fa-database",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": "admin/custom_admin.css",
    "custom_js": None,
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False, "footer_small_text": False, "body_small_text": False,
    "brand_small_text": False, "brand_colour": "navbar-dark", "accent": "accent-primary",
    "navbar": "navbar-dark", "no_navbar_border": False, "navbar_fixed": False,
    "layout_boxed": False, "footer_fixed": False, "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary", "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False, "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False, "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False, "theme": "default", "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary", "secondary": "btn-secondary", "info": "btn-info",
        "warning": "btn-warning", "danger": "btn-danger", "success": "btn-success"
    }
}

JAZZMIN_SETTINGS["order_with_respect_to"] = (
    {"app": "dashboard", "label": "Tổng quan"},
    {"app": "users", "label": "Quản lý Nhân sự"},
    {"app": "clients", "label": "Quản lý Khách hàng"},
    {"app": "operations", "label": "Vận hành & Tác nghiệp"},
    {"app": "workflow", "label": "Quy trình & Công việc"},
    {"app": "reports", "label": "Báo cáo & Thống kê"},
    {"app": "inspection", "label": "Thanh tra & Tuần tra"},
    {"app": "inventory", "label": "Kho & Vật tư"},
    {"app": "accounting", "label": "Kế toán"},
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
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "root": {"handlers": ["console", "file"], "level": "INFO",},
}