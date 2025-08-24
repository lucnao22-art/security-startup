# file: clients/models.py
from django.db import models

class KhachHang(models.Model):
    ten_cong_ty = models.CharField("Tên công ty", max_length=255)
    ma_so_thue = models.CharField("Mã số thuế", max_length=20, blank=True)
    dia_chi = models.TextField("Địa chỉ")
    nguoi_lien_he = models.CharField("Người liên hệ", max_length=100)
    sdt_lien_he = models.CharField("SĐT liên hệ", max_length=15)
    email_lien_he = models.EmailField("Email liên hệ", blank=True)

    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "Danh sách Khách hàng"

    def __str__(self):
        return self.ten_cong_ty

class HopDong(models.Model):
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE, verbose_name="Khách hàng")
    so_hop_dong = models.CharField("Số hợp đồng", max_length=50, unique=True)
    ngay_ky = models.DateField("Ngày ký")
    ngay_hieu_luc = models.DateField("Ngày hiệu lực")
    ngay_het_han = models.DateField("Ngày hết hạn")
    file_hop_dong = models.FileField("File đính kèm", upload_to='hop_dong/', blank=True, null=True)

    class Meta:
        verbose_name = "Hợp đồng"
        verbose_name_plural = "Danh sách Hợp đồng"

    def __str__(self):
        return f"Hợp đồng {self.so_hop_dong} - {self.khach_hang.ten_cong_ty}"

class MucTieu(models.Model):
    hop_dong = models.ForeignKey(HopDong, on_delete=models.CASCADE, verbose_name="Hợp đồng")
    ten_muc_tieu = models.CharField("Tên mục tiêu", max_length=255)
    dia_chi = models.TextField("Địa chỉ mục tiêu")
    
    class Meta:
        verbose_name = "Mục tiêu"
        verbose_name_plural = "Danh sách Mục tiêu"

    def __str__(self):
        return self.ten_muc_tieu