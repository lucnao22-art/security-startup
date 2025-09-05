# file: inspection/models.py

from django.db import models
from django.utils import timezone
from users.models import NhanVien
from clients.models import MucTieu
from operations.models import PhanCongCaTruc

class LoaiTuanTra(models.Model):
    muc_tieu = models.ForeignKey(MucTieu, on_delete=models.CASCADE, related_name='cac_loai_tuan_tra')
    ten_loai = models.CharField("Tên loại tuần tra", max_length=255)
    mo_ta = models.TextField("Mô tả", blank=True)

    class Meta:
        verbose_name = "Loại Tuần Tra"
        verbose_name_plural = "Các Loại Tuần Tra"

    def __str__(self):
        return self.ten_loai

class DiemTuanTra(models.Model):
    loai_tuan_tra = models.ForeignKey(LoaiTuanTra, on_delete=models.CASCADE, related_name='cac_diem_tuan_tra')
    ten_diem = models.CharField("Tên điểm tuần tra", max_length=255)
    ma_qr = models.CharField("Mã QR", max_length=255, unique=True)
    vi_tri_cu_the = models.CharField("Vị trí cụ thể", max_length=255, blank=True)
    thu_tu = models.PositiveIntegerField("Thứ tự điểm quét")

    class Meta:
        verbose_name = "Điểm Tuần Tra"
        verbose_name_plural = "Các Điểm Tuần Tra"
        ordering = ['loai_tuan_tra', 'thu_tu']

    def __str__(self):
        return f"{self.loai_tuan_tra.ten_loai} - Điểm {self.thu_tu}: {self.ten_diem}"

class LuotTuanTra(models.Model):
    class TrangThai(models.TextChoices):
        DANG_TIEN_HANH = 'IN_PROGRESS', 'Đang tiến hành'
        HOAN_THANH = 'COMPLETED', 'Hoàn thành'
        KHONG_HOAN_THANH = 'INCOMPLETE', 'Không hoàn thành'

    # --- SỬA LẠI TRƯỜNG NÀY, THÊM null=True, blank=True ---
    loai_tuan_tra = models.ForeignKey(
        LoaiTuanTra, 
        on_delete=models.CASCADE,
        null=True, # Cho phép giá trị NULL trong CSDL
        blank=True # Cho phép để trống trong form
    )
    ca_truc = models.ForeignKey(
        PhanCongCaTruc, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    thoi_gian_bat_dau = models.DateTimeField(default=timezone.now)
    thoi_gian_ket_thuc = models.DateTimeField(null=True, blank=True)
    trang_thai = models.CharField(max_length=20, choices=TrangThai.choices, default=TrangThai.DANG_TIEN_HANH)

    class Meta:
        verbose_name = "Lượt Tuần Tra"
        verbose_name_plural = "Các Lượt Tuần Tra"
        ordering = ['-thoi_gian_bat_dau']

    def __str__(self):
        if self.loai_tuan_tra:
            return f"Lượt tuần tra {self.loai_tuan_tra.ten_loai} lúc {self.thoi_gian_bat_dau.strftime('%H:%M %d/%m')}"
        return f"Lượt tuần tra (chưa xác định) lúc {self.thoi_gian_bat_dau.strftime('%H:%M %d/%m')}"


class GhiNhanTuanTra(models.Model):
    luot_tuan_tra = models.ForeignKey(LuotTuanTra, on_delete=models.CASCADE, related_name='cac_ghi_nhan')
    diem_tuan_tra = models.ForeignKey(DiemTuanTra, on_delete=models.CASCADE)
    thoi_gian_quet = models.DateTimeField(default=timezone.now)
    ghi_chu = models.TextField("Ghi chú", blank=True)
    hinh_anh = models.ImageField("Hình ảnh", upload_to='ghi_nhan_tuan_tra/', null=True, blank=True)

    class Meta:
        verbose_name = "Ghi Nhận Tuần Tra"
        verbose_name_plural = "Các Ghi Nhận Tuần Tra"
        ordering = ['thoi_gian_quet']

    def __str__(self):
        return f"Quét điểm {self.diem_tuan_tra.ten_diem} lúc {self.thoi_gian_quet.strftime('%H:%M')}"