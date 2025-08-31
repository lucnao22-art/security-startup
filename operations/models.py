# file: operations/models.py
from django.db import models
from users.models import NhanVien
from clients.models import MucTieu


class ViTriChot(models.Model):
    muc_tieu = models.ForeignKey(
        MucTieu,
        on_delete=models.CASCADE,
        related_name="vi_tri_chot",
        verbose_name="Mục tiêu",
    )
    ten_vi_tri = models.CharField("Tên vị trí", max_length=255)

    class Meta:
        verbose_name = "Vị trí chốt"
        verbose_name_plural = "Danh sách Vị trí chốt"

    def __str__(self):
        return f"{self.ten_vi_tri} ({self.muc_tieu.ten_muc_tieu})"


class CaLamViec(models.Model):
    ten_ca = models.CharField("Tên ca", max_length=100)
    gio_bat_dau = models.TimeField("Giờ bắt đầu")
    gio_ket_thuc = models.TimeField("Giờ kết thúc")

    class Meta:
        verbose_name = "Ca làm việc"
        verbose_name_plural = "Danh sách Ca làm việc"

    def __str__(self):
        return self.ten_ca


class PhanCongCaTruc(models.Model):
    vi_tri_chot = models.ForeignKey(
        ViTriChot, on_delete=models.CASCADE, verbose_name="Vị trí chốt"
    )
    nhan_vien = models.ForeignKey(
        NhanVien, on_delete=models.CASCADE, verbose_name="Nhân viên"
    )
    ca_lam_viec = models.ForeignKey(
        CaLamViec, on_delete=models.CASCADE, verbose_name="Ca làm việc"
    )
    ngay_truc = models.DateField("Ngày trực")

    class Meta:
        verbose_name = "Phân công ca trực"
        verbose_name_plural = "Bảng Phân công ca trực"
        unique_together = ("vi_tri_chot", "nhan_vien", "ngay_truc", "ca_lam_viec")
        ordering = ["ngay_truc", "ca_lam_viec__gio_bat_dau"]

    def __str__(self):
        return f"{self.nhan_vien.ho_ten} trực tại {self.vi_tri_chot.ten_vi_tri} ngày {self.ngay_truc}"


class ChamCong(models.Model):
    ca_truc = models.OneToOneField(
        PhanCongCaTruc, on_delete=models.CASCADE, verbose_name="Ca trực"
    )
    thoi_gian_check_in = models.DateTimeField(
        "Thời gian Check-in", null=True, blank=True
    )
    thoi_gian_check_out = models.DateTimeField(
        "Thời gian Check-out", null=True, blank=True
    )
    anh_check_in = models.ImageField(
        "Ảnh Check-in", upload_to="check_in/", null=True, blank=True
    )
    anh_check_out = models.ImageField(
        "Ảnh Check-out", upload_to="check_out/", null=True, blank=True
    )
    ghi_chu = models.TextField("Ghi chú", blank=True)

    class Meta:
        verbose_name = "Chấm công"
        verbose_name_plural = "Dữ liệu Chấm công"

    def __str__(self):
        return f"Chấm công cho {self.ca_truc}"


class BaoCaoSuCo(models.Model):
    class TrangThaiBaoCao(models.TextChoices):
        MOI = "MOI", "Mới"
        DA_XEM = "DAXEM", "Đã xem"
        DANG_XU_LY = "DXL", "Đang xử lý"
        LEO_THANG = "LEOTHANG", "Đã leo thang"
        DA_GIAI_QUYET = "DGQ", "Đã giải quyết"

    ca_truc = models.ForeignKey(
        PhanCongCaTruc, on_delete=models.CASCADE, verbose_name="Ca trực"
    )
    thoi_gian_bao_cao = models.DateTimeField("Thời gian báo cáo", auto_now_add=True)
    tieu_de = models.CharField("Tiêu đề", max_length=255)
    noi_dung = models.TextField("Nội dung chi tiết")
    hinh_anh = models.ImageField(
        "Hình ảnh minh họa", upload_to="su_co/", null=True, blank=True
    )
    trang_thai = models.CharField(
        "Trạng thái",
        max_length=10,
        choices=TrangThaiBaoCao.choices,
        default=TrangThaiBaoCao.MOI,
    )
    nguoi_chiu_trach_nhiem = models.ForeignKey(
        NhanVien,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Người chịu trách nhiệm",
    )
    lich_su_xu_ly = models.TextField("Lịch sử xử lý", blank=True)

    class Meta:
        verbose_name = "Báo cáo Sự cố"
        verbose_name_plural = "Danh sách Báo cáo Sự cố"

    def __str__(self):
        return self.tieu_de


# ----- MODEL MỚI CHO BÁO CÁO / ĐỀ XUẤT -----
class BaoCaoDeXuat(models.Model):
    class LoaiBaoCao(models.TextChoices):
        BAO_CAO = "BC", "Báo cáo"
        DE_XUAT = "DX", "Đề xuất"
        KIEN_NGHI = "KN", "Kiến nghị"

    nhan_vien = models.ForeignKey(
        NhanVien, on_delete=models.CASCADE, verbose_name="Người gửi"
    )
    loai_bao_cao = models.CharField("Loại", max_length=2, choices=LoaiBaoCao.choices)
    tieu_de = models.CharField("Tiêu đề", max_length=255)
    noi_dung = models.TextField("Nội dung chi tiết")
    ngay_gui = models.DateTimeField("Ngày gửi", auto_now_add=True)
    da_doc = models.BooleanField("Đã đọc", default=False)

    class Meta:
        verbose_name = "Báo cáo & Đề xuất"
        verbose_name_plural = "DS Báo cáo & Đề xuất"

    def __str__(self):
        return f"{self.get_loai_bao_cao_display()} từ {self.nhan_vien.ho_ten}"
