from django.db import models


class KhachHangTiemNang(models.Model):
    ten_cong_ty = models.CharField("Tên công ty", max_length=255)
    nguoi_lien_he = models.CharField("Người liên hệ", max_length=255)
    email = models.EmailField("Email")
    sdt = models.CharField("Số điện thoại", max_length=20)
    dia_chi = models.TextField("Địa chỉ")
    nguon = models.CharField("Nguồn", max_length=100, blank=True)
    ghi_chu = models.TextField("Ghi chú", blank=True)

    class Meta:
        verbose_name = "Khách hàng Tiềm năng"
        verbose_name_plural = "DS Khách hàng Tiềm năng"

    def __str__(self):
        return self.ten_cong_ty


class CoHoiKinhDoanh(models.Model):
    class TrangThai(models.TextChoices):
        MOI = "MOI", "Mới"
        LIEN_HE = "LIENHE", "Đã liên hệ"
        GUI_BAO_GIA = "BAOGIA", "Đã gửi báo giá"
        THUONG_LUONG = "THUONGLUONG", "Đang thương lượng"
        THANH_CONG = "THANHCONG", "Thành công"
        THAT_BAI = "THATBAI", "Thất bại"

    ten_co_hoi = models.CharField("Tên cơ hội", max_length=255)
    khach_hang_tiem_nang = models.ForeignKey(
        KhachHangTiemNang, on_delete=models.CASCADE, verbose_name="Khách hàng tiềm năng"
    )
    gia_tri_uoc_tinh = models.DecimalField(
        "Giá trị ước tính (VND)", max_digits=15, decimal_places=2
    )
    ngay_tao = models.DateTimeField("Ngày tạo", auto_now_add=True)
    ngay_ket_thuc_du_kien = models.DateField("Ngày kết thúc dự kiến")
    trang_thai = models.CharField(
        "Trạng thái", max_length=20, choices=TrangThai.choices, default=TrangThai.MOI
    )

    nguoi_phu_trach = models.ForeignKey(
        "users.NhanVien",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Người phụ trách",
    )

    class Meta:
        verbose_name = "Cơ hội Kinh doanh"
        verbose_name_plural = "Pipeline Kinh doanh"

    def __str__(self):
        return self.ten_co_hoi


class HopDong(models.Model):
    # --- DÒNG ĐÃ SỬA LỖI ---
    # Thêm null=True và blank=True để cho phép các hợp đồng cũ không có cơ hội liên quan
    co_hoi = models.OneToOneField(
        CoHoiKinhDoanh,
        on_delete=models.CASCADE,
        verbose_name="Cơ hội liên quan",
        null=True,
        blank=True,
    )

    so_hop_dong = models.CharField("Số hợp đồng", max_length=100, unique=True)
    ngay_ky = models.DateField("Ngày ký")
    ngay_hieu_luc = models.DateField("Ngày hiệu lực")
    ngay_het_han = models.DateField("Ngày hết hạn")
    gia_tri = models.DecimalField(
        "Giá trị Hợp đồng (VND)", max_digits=15, decimal_places=2
    )
    file_hop_dong = models.FileField(
        "File đính kèm", upload_to="hop_dong/", null=True, blank=True
    )

    class Meta:
        verbose_name = "Hợp đồng"
        verbose_name_plural = "Danh sách Hợp đồng"

    def __str__(self):
        return self.so_hop_dong


class MucTieu(models.Model):
    hop_dong = models.ForeignKey(
        HopDong,
        on_delete=models.CASCADE,
        related_name="muc_tieu",
        verbose_name="Hợp đồng",
    )
    ten_muc_tieu = models.CharField("Tên mục tiêu", max_length=255)
    dia_chi = models.TextField("Địa chỉ Mục tiêu")
    nguoi_lien_he = models.CharField("Người liên hệ tại Mục tiêu", max_length=255)
    sdt_lien_he = models.CharField("SĐT liên hệ", max_length=20)

    quan_ly_muc_tieu = models.ForeignKey(
        "users.NhanVien",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="muc_tieu_quan_ly",
        verbose_name="Chỉ huy trưởng/Quản lý",
    )

    class Meta:
        verbose_name = "Mục tiêu Bảo vệ"
        verbose_name_plural = "Danh sách Mục tiêu"

    def __str__(self):
        return self.ten_muc_tieu
