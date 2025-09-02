# file: main/models.py
from django.db import models

class CompanyProfile(models.Model):
    ten_cong_ty = models.CharField("Tên công ty", max_length=255)
    logo = models.ImageField("Logo", upload_to="logos/", null=True, blank=True)
    dia_chi = models.CharField("Địa chỉ", max_length=255, blank=True)
    email = models.EmailField("Email", blank=True)
    sdt = models.CharField("Số điện thoại", max_length=20, blank=True)
    website = models.URLField("Website", blank=True)

    class Meta:
        verbose_name = "Thông tin Công ty"
        verbose_name_plural = "Thông tin Công ty"

    def __str__(self):
        return self.ten_cong_ty