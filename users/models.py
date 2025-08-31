# file: users/models.py

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from clients.models import MucTieu
from django.conf import settings


# --- CÁC MODEL CẤU HÌNH ---
class CauHinhMaNhanVien(models.Model):
    tien_to = models.CharField("Tiền tố", max_length=5, default="NV")
    do_dai_so = models.PositiveIntegerField("Độ dài phần số", default=4)
    so_hien_tai = models.PositiveIntegerField("Số hiện tại", default=0)

    class Meta:
        verbose_name = "Cấu hình Mã nhân viên"
        verbose_name_plural = "Cấu hình Mã nhân viên"

    def __str__(self):
        return "Cấu hình sinh mã nhân viên"


class ChucDanh(models.Model):
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


# --- MODEL NHÂN VIÊN ---
class NhanVien(models.Model):
    class GioiTinh(models.TextChoices):
        NAM = "M", "Nam"
        NU = "F", "Nữ"
        KHAC = "O", "Khác"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Tài khoản đăng nhập",
        null=True,
        blank=True,
    )
    phong_ban = models.ForeignKey(
        PhongBan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Phòng ban",
    )
    chuc_danh = models.ForeignKey(
        ChucDanh,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Chức danh",
    )

    ma_nhan_vien = models.CharField(
        "Mã số nhân viên", max_length=20, unique=True, editable=False
    )
    anh_the = models.ImageField("Ảnh thẻ", upload_to="anh_the/", null=True, blank=True)
    ho_ten = models.CharField("Họ và Tên", max_length=255)
    ngay_sinh = models.DateField("Ngày sinh")
    gioi_tinh = models.CharField("Giới tính", max_length=1, choices=GioiTinh.choices)
    so_cccd = models.CharField("Số CCCD/CMND", max_length=20, unique=True)
    sdt_chinh = models.CharField("SĐT chính", max_length=15)
    email = models.EmailField("Email", unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Nhân viên"
        verbose_name_plural = "Danh sách Nhân viên"

    def __str__(self):
        return f"{self.ma_nhan_vien} - {self.ho_ten}"

    def save(self, *args, **kwargs):
        if not self.ma_nhan_vien:
            config, created = CauHinhMaNhanVien.objects.get_or_create(pk=1)
            config.so_hien_tai += 1
            so_thu_tu = str(config.so_hien_tai).zfill(config.do_dai_so)
            self.ma_nhan_vien = f"{config.tien_to}{so_thu_tu}"
            config.save()
        super().save(*args, **kwargs)


# --- MODEL LỊCH SỬ CÔNG TÁC ---
# Lớp này đã được di chuyển ra ngoài hàm, ngang hàng với NhanVien
class LichSuCongTac(models.Model):
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


# --- TÍN HIỆU (SIGNAL) ---
@receiver(post_save, sender=NhanVien)
def cap_nhat_quyen_tu_dong(sender, instance, created, **kwargs):
    if instance.user:
        user = instance.user
        user.groups.clear()  # Xóa hết các quyền cũ

        # Thêm quyền từ Chức danh (quyền cá nhân)
        if instance.chuc_danh and instance.chuc_danh.nhom_quyen:
            user.groups.add(instance.chuc_danh.nhom_quyen)

        # Thêm quyền từ Phòng ban (quyền chung)
        if instance.phong_ban and instance.phong_ban.nhom_quyen:
            user.groups.add(instance.phong_ban.nhom_quyen)
