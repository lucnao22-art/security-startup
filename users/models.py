# file: users/models.py

from django.db import models

class NhanVien(models.Model):
    class TrangThai(models.TextChoices):
        UNG_VIEN = 'UV', 'Ứng viên'
        THU_VIEC = 'TV', 'Thử việc'
        CHINH_THUC = 'CT', 'Chính thức'
        TAM_NGHI = 'TN', 'Tạm nghỉ'
        DA_NGHI_VIEC = 'DNV', 'Đã nghỉ việc'

    class GioiTinh(models.TextChoices):
        NAM = 'M', 'Nam'
        NU = 'F', 'Nữ'
        KHAC = 'O', 'Khác'

    ma_nhan_vien = models.CharField("Mã số nhân viên", max_length=20, unique=True)
    anh_the = models.ImageField("Ảnh thẻ", upload_to='anh_the/', null=True, blank=True)
    ho_ten = models.CharField("Họ và Tên", max_length=255)
    ngay_sinh = models.DateField("Ngày sinh")
    gioi_tinh = models.CharField("Giới tính", max_length=1, choices=GioiTinh.choices)
    chieu_cao = models.FloatField("Chiều cao (cm)", null=True, blank=True)
    can_nang = models.FloatField("Cân nặng (kg)", null=True, blank=True)
    so_cccd = models.CharField("Số CCCD/CMND", max_length=20, unique=True)
    ngay_cap_cccd = models.DateField("Ngày cấp CCCD")
    noi_cap_cccd = models.CharField("Nơi cấp CCCD", max_length=255)
    sdt_chinh = models.CharField("SĐT chính", max_length=15)
    sdt_phu = models.CharField("SĐT phụ", max_length=15, blank=True, null=True)
    email = models.EmailField("Email", unique=True, null=True, blank=True)
    dia_chi_thuong_tru = models.TextField("Địa chỉ Thường trú")
    dia_chi_tam_tru = models.TextField("Địa chỉ Tạm trú")
    trang_thai_hon_nhan = models.CharField("Trạng thái Hôn nhân", max_length=50, blank=True, null=True)
    trinh_do_hoc_van = models.CharField("Trình độ Học vấn", max_length=100, blank=True, null=True)
    ten_lien_he_khan_cap = models.CharField("Tên người liên hệ khẩn cấp", max_length=255)
    quan_he_khan_cap = models.CharField("Mối quan hệ", max_length=50)
    sdt_khan_cap = models.CharField("SĐT người liên hệ khẩn cấp", max_length=15)
    thong_tin_suc_khoe = models.TextField("Ghi chú Sức khỏe", blank=True, null=True)
    thong_tin_ngan_hang = models.TextField("Thông tin Ngân hàng", blank=True, null=True)
    trang_thai_lam_viec = models.CharField(
        "Trạng thái làm việc",
        max_length=3,
        choices=TrangThai.choices,
        default=TrangThai.UNG_VIEN,
    )
    nguoi_gioi_thieu = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Người giới thiệu"
    )

    class Meta:
        verbose_name = "Nhân viên"
        verbose_name_plural = "Danh sách Nhân viên"

    def __str__(self):
        return f"{self.ma_nhan_vien} - {self.ho_ten}"