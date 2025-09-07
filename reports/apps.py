# file: reports/apps.py

from django.apps import AppConfig


class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reports'
    verbose_name = "Báo cáo & Thống kê" # Tên sẽ hiển thị trên trang Admin