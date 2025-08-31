# file: users/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _  # Thêm dòng này


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = _("Quản lý Nhân sự")
