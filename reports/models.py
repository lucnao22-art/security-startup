# file: reports/models.py

from django.db import models

class BaoCao(models.Model):
    """
    Model này chỉ dùng để giữ chỗ, giúp app "reports" có thể hiển thị
    trên trang Admin. Nó không lưu trữ dữ liệu thực tế.
    """
    class Meta:
        verbose_name = "Truy cập Báo cáo"
        verbose_name_plural = "Truy cập Báo cáo"