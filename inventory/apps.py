# file: inventory/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'
    verbose_name = _("Quản lý Kho & Tài sản")

    def ready(self):
        # Dòng này sẽ import và kích hoạt các tín hiệu
        import inventory.signals