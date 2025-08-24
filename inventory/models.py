# file: inventory/models.py
from django.db import models
from users.models import NhanVien
from clients.models import MucTieu

class VatTu(models.Model):
    ten_vat_tu = models.CharField("Tên vật tư", max_length=255)
    don_vi_tinh = models.CharField("Đơn vị tính", max_length=50)
    so_luong_ton_kho = models.PositiveIntegerField("Số lượng tồn kho", default=0)

    class Meta:
        verbose_name = "Vật tư"
        verbose_name_plural = "Danh mục Vật tư"

    def __str__(self):
        return self.ten_vat_tu

class CapPhatCaNhan(models.Model):
    nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, verbose_name="Nhân viên")
    vat_tu = models.ForeignKey(VatTu, on_delete=models.CASCADE, verbose_name="Vật tư")
    so_luong = models.PositiveIntegerField("Số lượng cấp phát")
    ngay_cap_phat = models.DateField("Ngày cấp phát", auto_now_add=True)
    ghi_chu = models.TextField("Ghi chú", blank=True)

    class Meta:
        verbose_name = "Cấp phát Cá nhân"
        verbose_name_plural = "Lịch sử Cấp phát Cá nhân"

    def __str__(self):
        return f"Cấp {self.vat_tu.ten_vat_tu} cho {self.nhan_vien.ho_ten}"

class CapPhatMucTieu(models.Model):
    muc_tieu = models.ForeignKey(MucTieu, on_delete=models.CASCADE, verbose_name="Mục tiêu")
    vat_tu = models.ForeignKey(VatTu, on_delete=models.CASCADE, verbose_name="Vật tư")
    so_luong = models.PositiveIntegerField("Số lượng cấp phát")
    ngay_cap_phat = models.DateField("Ngày cấp phát", auto_now_add=True)
    
    class Meta:
        verbose_name = "Cấp phát Mục tiêu"
        verbose_name_plural = "Lịch sử Cấp phát Mục tiêu"
        
    def __str__(self):
        return f"Cấp {self.vat_tu.ten_vat_tu} cho {self.muc_tieu.ten_muc_tieu}"