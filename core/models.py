# file: core/models.py
from django.db import models

class ThongTinCongTy(models.Model):
    ten_cong_ty = models.CharField("Tên công ty", max_length=255, default="Công ty TNHH Dịch vụ Bảo vệ XYZ")
    dia_chi = models.CharField("Địa chỉ", max_length=255, blank=True)
    so_dien_thoai = models.CharField("Số điện thoại", max_length=20, blank=True)
    email = models.EmailField("Email", blank=True)
    website = models.URLField("Website", blank=True)
    logo = models.ImageField("Logo công ty", upload_to='logos/', blank=True, null=True)

    class Meta:
        verbose_name = "Thông tin Công ty"
        verbose_name_plural = "Thông tin Công ty"

    def __str__(self):
        return self.ten_cong_ty

class PhongBan(models.Model):
    ten_phong_ban = models.CharField("Tên phòng ban", max_length=100, unique=True)
    mo_ta = models.TextField("Mô tả", blank=True)

    class Meta:
        verbose_name = "Phòng ban"
        verbose_name_plural = "Danh mục Phòng ban"

    def __str__(self):
        return self.ten_phong_ban

class ChucDanh(models.Model):
    ten_chuc_danh = models.CharField("Tên chức danh", max_length=100, unique=True)
    phong_ban = models.ForeignKey(PhongBan, on_delete=models.CASCADE, verbose_name="Thuộc phòng ban")
    
    class Meta:
        verbose_name = "Chức danh"
        verbose_name_plural = "Danh mục Chức danh"

    def __str__(self):
        return f"{self.ten_chuc_danh} ({self.phong_ban.ten_phong_ban})"
