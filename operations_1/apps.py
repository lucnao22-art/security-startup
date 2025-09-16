# operations/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OperationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "operations"
    verbose_name = _("Quản lý Vận hành")  # Thêm tên tiếng Việt

    def ready(self):
        import operations.signals  # Đảm bảo dòng này tồn tại và không bị comment
