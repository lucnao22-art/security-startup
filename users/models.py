# file: users/models.py

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from clients.models import MucTieu
from django.conf import settings

class CauHinhMaNhanVien(models.Model):
    tien_to = models.CharField("Tiền tố", max_length=5, default="NV")
    do_dai_so = models.PositiveIntegerField("Độ dài phần số", default=4)
    so_hien_tai = models.PositiveIntegerField("Số hiện tại", default=0)

    class Meta:
        verbose_name = "Cấu hình Mã nhân viên"
        verbose_name_plural = "Cấu hình Mã nhân viên"

    def __str__(self):
        return "Cấu hình sinh mã nhân viên"

class PhongBan(models.Model):
    ten_phong_ban = models.CharField("Tên phòng ban", max_length=100, unique=True)
    mo_ta = models.TextField("Mô tả", blank=True, null=True)

    class Meta:
        verbose_name = "Phòng ban"
        verbose_name_plural = "Danh sách Phòng ban"

    def __str__(self):
        return self.ten_phong_ban

class ChungChi(models.Model):
    nhan_vien = models.ForeignKey('NhanVien', on_delete=models.CASCADE, related_name='chung_chi', verbose_name="Nhân viên")
    ten_chung_chi = models.CharField("Tên bằng cấp/chứng chỉ", max_length=255)
    so_hieu = models.CharField("Số hiệu", max_length=100, blank=True)
    ngay_cap = models.DateField("Ngày cấp")
    ngay_het_han = models.DateField("Ngày hết hạn", null=True, blank=True)
    file_scan = models.FileField("File đính kèm", upload_to='chung_chi/', blank=True, null=True)

    class Meta:
        verbose_name = "Bằng cấp/Chứng chỉ"
        verbose_name_plural = "Bằng cấp & Chứng chỉ"

    def __str__(self):
        return f"{self.ten_chung_chi} của {self.nhan_vien.ho_ten}"

class NhanVien(models.Model):
    class ChucVu(models.TextChoices):
        NHAN_VIEN = 'NV', 'Nhân viên'
        CA_TRUONG = 'CT', 'Ca trưởng'
        CHI_HUY_PHO = 'CHP', 'Chỉ huy phó'
        CHI_HUY_TRUONG = 'CHT', 'Chỉ huy trưởng'
        QUAN_LY_VUNG = 'QLV', 'Quản lý Vùng'
        TRUONG_PHONG = 'TP', 'Trưởng phòng'
    
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

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Tài khoản đăng nhập",
        null=True, blank=True
    )
    phong_ban = models.ForeignKey(PhongBan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Phòng ban")
    chuc_vu = models.CharField("Chức vụ", max_length=3, choices=ChucVu.choices, default=ChucVu.NHAN_VIEN)
    quan_ly_truc_tiep = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Quản lý trực tiếp"
    )
    ma_nhan_vien = models.CharField("Mã số nhân viên", max_length=20, unique=True, editable=False)
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
        related_name="nguoi_duoc_gioi_thieu",
        verbose_name="Người giới thiệu"
    )
    muc_tieu_lam_viec = models.ForeignKey(
        MucTieu,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Mục tiêu làm việc"
    )

    class Meta:
        verbose_name = "Nhân viên"
        verbose_name_plural = "Danh sách Nhân viên"

    def __str__(self):
        return f"{self.ma_nhan_vien} - {self.ho_ten}"

    def save(self, *args, **kwargs):
        if not self.pk:
            config, created = CauHinhMaNhanVien.objects.get_or_create(pk=1)
            config.so_hien_tai += 1
            so_thu_tu = str(config.so_hien_tai).zfill(config.do_dai_so)
            self.ma_nhan_vien = f"{config.tien_to}{so_thu_tu}"
            config.save()
        super().save(*args, **kwargs)

@receiver(post_save, sender=NhanVien)
def tu_dong_tao_user_va_phan_quyen(sender, instance, created, **kwargs):
    if created and not instance.user:
        user, user_created = User.objects.get_or_create(
            username=instance.ma_nhan_vien,
            defaults={'password': instance.ma_nhan_vien}
        )
        if user_created:
            user.set_password(instance.ma_nhan_vien)
            user.save()
        instance.user = user
        instance.save()

    if instance.user:
        user = instance.user
        user.groups.clear()
        chuc_vu_value = instance.get_chuc_vu_display()
        try:
            group, created = Group.objects.get_or_create(name=chuc_vu_value)
            user.groups.add(group)
        except Group.DoesNotExist:
            pass
        # ----- THÊM MODEL MỚI VÀO ĐÂY -----
class LichSuCongTac(models.Model):
    nhan_vien = models.ForeignKey('NhanVien', on_delete=models.CASCADE, related_name='lich_su_cong_tac')
    muc_tieu = models.ForeignKey(MucTieu, on_delete=models.SET_NULL, null=True, verbose_name="Mục tiêu")
    chuc_vu = models.CharField("Chức vụ tại mục tiêu", max_length=100)
    ngay_bat_dau = models.DateField("Ngày bắt đầu")
    ngay_ket_thuc = models.DateField("Ngày kết thúc", null=True, blank=True)
    mo_ta_nhiem_vu = models.TextField("Mô tả nhiệm vụ", blank=True)

    class Meta:
        verbose_name = "Lịch sử công tác"
        verbose_name_plural = "Lịch sử công tác"
        ordering = ['-ngay_bat_dau']

    def __str__(self):
        return f"{self.nhan_vien.ho_ten} tại {self.muc_tieu.ten_muc_tieu}"