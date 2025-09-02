# file: users/models.py
from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from clients.models import MucTieu
from django.conf import settings


# --- CÁC MODEL CẤU HÌNH (GIỮ NGUYÊN) ---
class CauHinhMaNhanVien(models.Model):
    # ... (giữ nguyên)
    tien_to = models.CharField("Tiền tố", max_length=5, default="NV")
    do_dai_so = models.PositiveIntegerField("Độ dài phần số", default=4)
    so_hien_tai = models.PositiveIntegerField("Số hiện tại", default=0)

    class Meta:
        verbose_name = "Cấu hình Mã nhân viên"
        verbose_name_plural = "Cấu hình Mã nhân viên"

    def __str__(self):
        return "Cấu hình sinh mã nhân viên"


class ChucDanh(models.Model):
    # ... (giữ nguyên)
    ten_chuc_danh = models.CharField("Tên chức danh", max_length=100, unique=True)
    mo_ta = models.TextField("Mô tả", blank=True, null=True)
    nhom_quyen = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Nhóm quyền",
    )

    class Meta:
        verbose_name = "Chức danh"
        verbose_name_plural = "Danh sách Chức danh"

    def __str__(self):
        return self.ten_chuc_danh

class PhongBan(models.Model):
    # ... (giữ nguyên)
    ten_phong_ban = models.CharField("Tên phòng ban", max_length=100, unique=True)
    mo_ta = models.TextField("Mô tả", blank=True, null=True)
    nhom_quyen = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Nhóm quyền chung",
    )

    class Meta:
        verbose_name = "Phòng ban"
        verbose_name_plural = "Danh sách Phòng ban"

    def __str__(self):
        return self.ten_phong_ban

# --- MODEL NHÂN VIÊN (NÂNG CẤP) ---
class NhanVien(models.Model):
    # --- ENUMS (choices) ---
    class GioiTinh(models.TextChoices):
        NAM = "M", "Nam"
        NU = "F", "Nữ"
        KHAC = "O", "Khác"
        
    class TrangThaiLamViec(models.TextChoices):
        THU_VIEC = "THUVIEC", "Thử việc"
        CHINH_THUC = "CHINHTHUC", "Chính thức"
        TAM_HOAN = "TAMHOAN", "Tạm hoãn"
        NGHI_VIEC = "NGHIVIEC", "Đã nghỉ việc"

    class LoaiHopDong(models.TextChoices):
        XAC_DINH_THOI_HAN = "XDTH", "Xác định thời hạn"
        KHONG_XAC_DINH_THOI_HAN = "KXDTH", "Không xác định thời hạn"
        THOI_VU = "THOIVU", "Thời vụ"

    # --- Các quan hệ (giữ nguyên) ---
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Tài khoản đăng nhập",
        null=True, blank=True
    )
    phong_ban = models.ForeignKey(
        PhongBan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Phòng ban"
    )
    chuc_danh = models.ForeignKey(
        ChucDanh, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Chức danh"
    )

    # --- Thông tin cơ bản (giữ nguyên và bổ sung) ---
    ma_nhan_vien = models.CharField("Mã số nhân viên", max_length=20, unique=True, editable=False)
    anh_the = models.ImageField("Ảnh thẻ", upload_to="anh_the/", null=True, blank=True)
    ho_ten = models.CharField("Họ và Tên", max_length=255)
    ngay_sinh = models.DateField("Ngày sinh")
    gioi_tinh = models.CharField("Giới tính", max_length=1, choices=GioiTinh.choices)
    so_cccd = models.CharField("Số CCCD/CMND", max_length=20, unique=True)
    sdt_chinh = models.CharField("SĐT chính", max_length=15)
    email = models.EmailField("Email", unique=True, null=True, blank=True)

    # --- THÔNG TIN CƯ TRÚ (MỚI) ---
    dia_chi_thuong_tru = models.CharField("Địa chỉ thường trú", max_length=255, blank=True)
    dia_chi_tam_tru = models.CharField("Địa chỉ tạm trú", max_length=255, blank=True)

    # --- THÔNG TIN LIÊN HỆ KHẨN CẤP (MỚI) ---
    nguoi_lien_he_khan_cap = models.CharField("Người liên hệ khẩn cấp", max_length=255, blank=True)
    sdt_khan_cap = models.CharField("SĐT khẩn cấp", max_length=15, blank=True)
    
    # --- THÔNG TIN CÔNG VIỆC (MỚI) ---
    ngay_vao_lam = models.DateField("Ngày vào làm", null=True, blank=True)
    trang_thai_lam_viec = models.CharField(
        "Trạng thái làm việc", max_length=10, choices=TrangThaiLamViec.choices, default=TrangThaiLamViec.THU_VIEC
    )
    loai_hop_dong = models.CharField("Loại hợp đồng", max_length=10, choices=LoaiHopDong.choices, blank=True)

    # --- THÔNG TIN NGÂN HÀNG (MỚI) ---
    so_tai_khoan = models.CharField("Số tài khoản ngân hàng", max_length=20, blank=True)
    ngan_hang = models.CharField("Tên ngân hàng", max_length=255, blank=True)
    chi_nhanh_ngan_hang = models.CharField("Chi nhánh", max_length=255, blank=True)


    class Meta:
        verbose_name = "Nhân viên"
        verbose_name_plural = "Danh sách Nhân viên"

    def __str__(self):
        return f"{self.ma_nhan_vien} - {self.ho_ten}"

    def save(self, *args, **kwargs):
        # ... (giữ nguyên)
        if not self.ma_nhan_vien:
            config, created = CauHinhMaNhanVien.objects.get_or_create(pk=1)
            config.so_hien_tai += 1
            so_thu_tu = str(config.so_hien_tai).zfill(config.do_dai_so)
            self.ma_nhan_vien = f"{config.tien_to}{so_thu_tu}"
            config.save()
        super().save(*args, **kwargs)


# --- CÁC MODEL MỚI ĐỂ LƯU THÔNG TIN PHỤ ---

class HocVan(models.Model):
    nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, related_name="hoc_van")
    truong_dao_tao = models.CharField("Trường/Trung tâm đào tạo", max_length=255)
    chuyen_nganh = models.CharField("Chuyên ngành", max_length=255)
    trinh_do = models.CharField("Trình độ", max_length=100) # Ví dụ: Đại học, Cao đẳng, 12/12
    tu_ngay = models.DateField("Từ ngày")
    den_ngay = models.DateField("Đến ngày")

    class Meta:
        verbose_name = "Học vấn"
        verbose_name_plural = "Quá trình Học vấn"

    def __str__(self):
        return f"{self.trinh_do} - {self.chuyen_nganh} tại {self.truong_dao_tao}"

class BangCapChungChi(models.Model):
    nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, related_name="bang_cap")
    ten_bang_cap = models.CharField("Tên bằng cấp/Chứng chỉ", max_length=255)
    noi_cap = models.CharField("Nơi cấp", max_length=255)
    ngay_cap = models.DateField("Ngày cấp")
    ngay_het_han = models.DateField("Ngày hết hạn", null=True, blank=True)
    file_dinh_kem = models.FileField("File đính kèm", upload_to="bang_cap/", null=True, blank=True)

    class Meta:
        verbose_name = "Bằng cấp & Chứng chỉ"
        verbose_name_plural = "Danh sách Bằng cấp & Chứng chỉ"

    def __str__(self):
        return self.ten_bang_cap

# --- MODEL LỊCH SỬ CÔNG TÁC (GIỮ NGUYÊN) ---
class LichSuCongTac(models.Model):
    # ... (giữ nguyên)
    nhan_vien = models.ForeignKey(
        "NhanVien", on_delete=models.CASCADE, related_name="lich_su_cong_tac"
    )
    muc_tieu = models.ForeignKey(
        MucTieu,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Mục tiêu",
    )
    chuc_danh_kiem_nhiem = models.ForeignKey(
        ChucDanh,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Chức danh tại mục tiêu",
    )
    quan_ly_truc_tiep = models.ForeignKey(
        "NhanVien",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Quản lý trực tiếp",
    )
    ngay_bat_dau = models.DateField("Ngày bắt đầu")
    ngay_ket_thuc = models.DateField("Ngày kết thúc", null=True, blank=True)
    la_vi_tri_hien_tai = models.BooleanField("Vị trí hiện tại?", default=True)

    class Meta:
        verbose_name = "Lịch sử công tác"
        verbose_name_plural = "Lịch sử công tác"
        ordering = ["-ngay_bat_dau"]

    def __str__(self):
        return f"{self.nhan_vien.ho_ten} tại {self.muc_tieu.ten_muc_tieu if self.muc_tieu else 'Văn phòng'}"

# --- TÍN HIỆU (SIGNAL) (GIỮ NGUYÊN) ---
@receiver(post_save, sender=NhanVien)
def cap_nhat_quyen_tu_dong(sender, instance, created, **kwargs):
    # ... (giữ nguyên)
    if instance.user:
        user = instance.user
        user.groups.clear()  # Xóa hết các quyền cũ

        # Thêm quyền từ Chức danh (quyền cá nhân)
        if instance.chuc_danh and instance.chuc_danh.nhom_quyen:
            user.groups.add(instance.chuc_danh.nhom_quyen)

        # Thêm quyền từ Phòng ban (quyền chung)
        if instance.phong_ban and instance.phong_ban.nhom_quyen:
            user.groups.add(instance.phong_ban.nhom_quyen)