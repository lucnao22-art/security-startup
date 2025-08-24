# file: operations/models.py
from django.db import models
from django.conf import settings
from users.models import NhanVien
from clients.models import MucTieu

class CaLamViec(models.Model):
    # ... code của CaLamViec giữ nguyên ...
    ten_ca = models.CharField("Tên ca", max_length=100)
    gio_bat_dau = models.TimeField("Giờ bắt đầu")
    gio_ket_thuc = models.TimeField("Giờ kết thúc")

    class Meta:
        verbose_name = "Ca làm việc"
        verbose_name_plural = "Danh sách Ca làm việc"

    def __str__(self):
        return self.ten_ca

class PhanCongCaTruc(models.Model):
    # ... code của PhanCongCaTruc giữ nguyên ...
    nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, verbose_name="Nhân viên")
    muc_tieu = models.ForeignKey(MucTieu, on_delete=models.CASCADE, verbose_name="Mục tiêu")
    ca_lam_viec = models.ForeignKey(CaLamViec, on_delete=models.CASCADE, verbose_name="Ca làm việc")
    ngay_truc = models.DateField("Ngày trực")

    class Meta:
        verbose_name = "Phân công ca trực"
        verbose_name_plural = "Bảng Phân công ca trực"
        unique_together = ('nhan_vien', 'ngay_truc')

    def __str__(self):
        return f"{self.nhan_vien.ho_ten} trực tại {self.muc_tieu.ten_muc_tieu} ngày {self.ngay_truc}"

# ----- BẮT ĐẦU THÊM CODE MỚI TỪ ĐÂY -----

class ChamCong(models.Model):
    ca_truc = models.OneToOneField(PhanCongCaTruc, on_delete=models.CASCADE, verbose_name="Ca trực")
    thoi_gian_check_in = models.DateTimeField("Thời gian Check-in", null=True, blank=True)
    thoi_gian_check_out = models.DateTimeField("Thời gian Check-out", null=True, blank=True)
    anh_check_in = models.ImageField("Ảnh Check-in", upload_to='check_in/', null=True, blank=True)
    anh_check_out = models.ImageField("Ảnh Check-out", upload_to='check_out/', null=True, blank=True)
    ghi_chu = models.TextField("Ghi chú", blank=True)

    class Meta:
        verbose_name = "Chấm công"
        verbose_name_plural = "Dữ liệu Chấm công"

    def __str__(self):
        return f"Chấm công cho {self.ca_truc}"

class BaoCaoSuCo(models.Model):
    ca_truc = models.ForeignKey(PhanCongCaTruc, on_delete=models.CASCADE, verbose_name="Ca trực")
    thoi_gian_bao_cao = models.DateTimeField("Thời gian báo cáo", auto_now_add=True)
    tieu_de = models.CharField("Tiêu đề", max_length=255)
    noi_dung = models.TextField("Nội dung chi tiết")
    hinh_anh = models.ImageField("Hình ảnh minh họa", upload_to='su_co/', null=True, blank=True)

    class Meta:
        verbose_name = "Báo cáo Sự cố"
        verbose_name_plural = "Danh sách Báo cáo Sự cố"

    def __str__(self):
        return self.tieu_de