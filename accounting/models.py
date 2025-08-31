# file: accounting/models.py
from django.db import models
from users.models import NhanVien
from clients.models import HopDong


class BangLuong(models.Model):
    nhan_vien = models.ForeignKey(
        NhanVien, on_delete=models.CASCADE, verbose_name="Nhân viên"
    )
    ky_tinh_luong = models.DateField("Kỳ tính lương (chọn ngày đầu tháng)")
    luong_co_ban = models.DecimalField("Lương cơ bản", max_digits=10, decimal_places=2)
    luong_tang_ca = models.DecimalField(
        "Lương tăng ca", max_digits=10, decimal_places=2, default=0
    )
    phu_cap = models.DecimalField("Phụ cấp", max_digits=10, decimal_places=2, default=0)
    khau_tru = models.DecimalField(
        "Khấu trừ", max_digits=10, decimal_places=2, default=0
    )
    thuc_lanh = models.DecimalField("Thực lãnh", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Bảng lương"
        verbose_name_plural = "Bảng lương Nhân viên"

    def __str__(self):
        return f"Bảng lương tháng {self.ky_tinh_luong.strftime('%m/%Y')} cho {self.nhan_vien.ho_ten}"


class HoaDon(models.Model):
    hop_dong = models.ForeignKey(
        HopDong, on_delete=models.CASCADE, verbose_name="Hợp đồng"
    )
    ky_thanh_toan = models.DateField("Kỳ thanh toán (chọn ngày đầu tháng)")
    so_tien = models.DecimalField("Số tiền", max_digits=12, decimal_places=2)
    trang_thai = models.CharField(
        "Trạng thái", max_length=50, default="Chưa thanh toán"
    )  # Ví dụ: Chưa thanh toán, Đã thanh toán, Quá hạn
    ngay_tao = models.DateTimeField("Ngày tạo", auto_now_add=True)
    ngay_thanh_toan = models.DateField("Ngày thanh toán", null=True, blank=True)

    class Meta:
        verbose_name = "Hóa đơn"
        verbose_name_plural = "Danh sách Hóa đơn"

    def __str__(self):
        return f"Hóa đơn tháng {self.ky_thanh_toan.strftime('%m/%Y')} cho {self.hop_dong.khach_hang.ten_cong_ty}"
