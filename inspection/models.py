from django.db import models
from clients.models import MucTieu
from users.models import NhanVien
import uuid


class TuyenTuanTra(models.Model):
    muc_tieu = models.ForeignKey(
        MucTieu, on_delete=models.CASCADE, verbose_name="Mục tiêu"
    )
    ten_tuyen = models.CharField("Tên tuyến tuần tra", max_length=255)
    mo_ta = models.TextField("Mô tả", blank=True)
    is_active = models.BooleanField("Đang hoạt động", default=True)

    class Meta:
        verbose_name = "Tuyến tuần tra"
        verbose_name_plural = "Quản lý Tuyến tuần tra"

    def __str__(self):
        return f"{self.ten_tuyen} - {self.muc_tieu.ten_muc_tieu}"


class DiemKiemTra(models.Model):
    tuyen_tuan_tra = models.ForeignKey(
        TuyenTuanTra,
        on_delete=models.CASCADE,
        related_name="diem_kiem_tra",
        verbose_name="Tuyến tuần tra",
    )
    ten_diem = models.CharField("Tên điểm kiểm tra", max_length=255)
    vi_tri_mo_ta = models.CharField(
        "Mô tả vị trí", max_length=255, help_text="Ví dụ: Cửa sau, góc tây nam nhà kho"
    )
    qr_code_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="Mã QR"
    )
    thu_tu = models.PositiveIntegerField("Thứ tự kiểm tra", default=0)

    class Meta:
        verbose_name = "Điểm kiểm tra (Checkpoint)"
        verbose_name_plural = "Danh sách Điểm kiểm tra"
        ordering = ["thu_tu"]

    def __str__(self):
        return self.ten_diem


class LuotTuanTra(models.Model):
    class TrangThai(models.TextChoices):
        DANG_TIEN_HANH = "IN_PROGRESS", "Đang tiến hành"
        HOAN_THANH = "COMPLETED", "Hoàn thành"
        KHONG_HOAN_THANH = "INCOMPLETE", "Không hoàn thành"

    tuyen_tuan_tra = models.ForeignKey(
        TuyenTuanTra, on_delete=models.PROTECT, verbose_name="Tuyến tuần tra"
    )
    nhan_vien = models.ForeignKey(
        NhanVien, on_delete=models.PROTECT, verbose_name="Nhân viên thực hiện"
    )
    thoi_gian_bat_dau = models.DateTimeField(
        auto_now_add=True, verbose_name="Thời gian bắt đầu"
    )
    thoi_gian_ket_thuc = models.DateTimeField(
        null=True, blank=True, verbose_name="Thời gian kết thúc"
    )
    trang_thai = models.CharField(
        "Trạng thái",
        max_length=20,
        choices=TrangThai.choices,
        default=TrangThai.DANG_TIEN_HANH,
    )
    ghi_chu_chung = models.TextField("Ghi chú chung", blank=True)

    class Meta:
        verbose_name = "Lượt tuần tra"
        verbose_name_plural = "Nhật ký Lượt tuần tra"
        ordering = ["-thoi_gian_bat_dau"]

    def __str__(self):
        return f"Lượt tuần tra của {self.nhan_vien.ho_ten} lúc {self.thoi_gian_bat_dau.strftime('%H:%M %d/%m/%Y')}"


class KetQuaKiemTra(models.Model):
    class TrangThaiDiem(models.TextChoices):
        BINH_THUONG = "OK", "Bình thường"
        CO_VAN_DE = "ISSUE", "Có vấn đề"

    luot_tuan_tra = models.ForeignKey(
        LuotTuanTra,
        on_delete=models.CASCADE,
        related_name="ket_qua",
        verbose_name="Lượt tuần tra",
    )
    diem_kiem_tra = models.ForeignKey(
        DiemKiemTra, on_delete=models.PROTECT, verbose_name="Điểm kiểm tra"
    )
    thoi_gian_quet = models.DateTimeField(
        auto_now_add=True, verbose_name="Thời gian quét"
    )
    trang_thai = models.CharField(
        "Trạng thái", max_length=10, choices=TrangThaiDiem.choices
    )
    ghi_chu = models.TextField("Ghi chú", blank=True)
    hinh_anh = models.ImageField(
        "Hình ảnh", upload_to="inspections/", null=True, blank=True
    )

    class Meta:
        verbose_name = "Kết quả kiểm tra điểm"
        verbose_name_plural = "Chi tiết Kết quả kiểm tra"
        ordering = ["thoi_gian_quet"]

    def __str__(self):
        return (
            f"Kiểm tra {self.diem_kiem_tra.ten_diem} - {self.get_trang_thai_display()}"
        )
