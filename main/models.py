# file: core/models.py
from django.db import models


class ThongTinCongTy(models.Model):
    ten_cong_ty = models.CharField(
        "Tên công ty", max_length=255, default="Công ty TNHH Dịch vụ Bảo vệ XYZ"
    )
    dia_chi = models.CharField("Địa chỉ", max_length=255, blank=True)
    so_dien_thoai = models.CharField("Số điện thoại", max_length=20, blank=True)
    email = models.EmailField("Email", blank=True)
    website = models.URLField("Website", blank=True)
    logo = models.ImageField("Logo công ty", upload_to="logos/", blank=True, null=True)

    class Meta:
        verbose_name = "Thông tin Công ty"
        verbose_name_plural = "Thông tin Công ty"

    def __str__(self):
        return self.ten_cong_ty
