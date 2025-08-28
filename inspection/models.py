# file: inspection/models.py
from django.db import models
from users.models import NhanVien
from clients.models import MucTieu

class PhieuThanhTra(models.Model):
    muc_tieu = models.ForeignKey(MucTieu, on_delete=models.CASCADE, verbose_name="Mục tiêu được thanh tra")
    nhan_vien_thanh_tra = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True, related_name='nguoi_thanh_tra', verbose_name="Cán bộ thanh tra")
    nhan_vien_bi_thanh_tra = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True, related_name='nguoi_bi_thanh_tra', verbose_name="Nhân viên bị thanh tra")
    ngay_thanh_tra = models.DateTimeField("Ngày giờ thanh tra", auto_now_add=True)
    ket_luan = models.TextField("Kết luận")
    hinh_anh = models.ImageField("Hình ảnh bằng chứng", upload_to='thanh_tra/', blank=True, null=True)

    class Meta:
        verbose_name = "Phiếu thanh tra"
        verbose_name_plural = "Danh sách Phiếu thanh tra"

    def __str__(self):
        return f"Thanh tra tại {self.muc_tieu.ten_muc_tieu} ngày {self.ngay_thanh_tra.strftime('%d/%m/%Y')}"

class KhoaHoc(models.Model):
    ten_khoa_hoc = models.CharField("Tên khóa học", max_length=255)
    mo_ta = models.TextField("Mô tả nội dung")

    class Meta:
        verbose_name = "Khóa học"
        verbose_name_plural = "Danh mục Khóa học"

    def __str__(self):
        return self.ten_khoa_hoc

class DangKyHoc(models.Model):
    khoa_hoc = models.ForeignKey(KhoaHoc, on_delete=models.CASCADE, verbose_name="Khóa học")
    nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, verbose_name="Học viên")
    ngay_dang_ky = models.DateField("Ngày đăng ký", auto_now_add=True)
    trang_thai = models.CharField("Trạng thái", max_length=50, default="Đã đăng ký") # Ví dụ: Đã đăng ký, Đã hoàn thành, Trượt

    class Meta:
        verbose_name = "Đăng ký học"
        verbose_name_plural = "Danh sách Đăng ký học"
        unique_together = ('khoa_hoc', 'nhan_vien')

    def __str__(self):
        return f"{self.nhan_vien.ho_ten} đăng ký khóa {self.khoa_hoc.ten_khoa_hoc}"