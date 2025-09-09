# file: inspection/models.py

from django.db import models
from django.utils import timezone
from users.models import NhanVien
from clients.models import MucTieu
from operations.models import PhanCongCaTruc

# ==============================================================================
# PHẦN 1: CÁC MODEL CHO NGHIỆP VỤ TUẦN TRA (GIÁM SÁT VỊ TRÍ)
# ==============================================================================

class LoaiTuanTra(models.Model):
    muc_tieu = models.ForeignKey(MucTieu, on_delete=models.CASCADE, related_name='cac_loai_tuan_tra')
    ten_loai = models.CharField("Tên loại tuần tra", max_length=255)
    mo_ta = models.TextField("Mô tả", blank=True)

    class Meta:
        verbose_name = "1. Loại Tuần Tra (NV Bảo vệ)"
        verbose_name_plural = "1. Các Loại Tuần Tra (NV Bảo vệ)"

    def __str__(self):
        return f"{self.ten_loai} ({self.muc_tieu.ten_muc_tieu})"

class DiemTuanTra(models.Model):
    loai_tuan_tra = models.ForeignKey(LoaiTuanTra, on_delete=models.CASCADE, related_name='cac_diem_tuan_tra')
    ten_diem = models.CharField("Tên điểm tuần tra", max_length=255)
    ma_qr = models.CharField("Mã QR", max_length=255, unique=True)
    vi_tri_cu_the = models.CharField("Vị trí cụ thể", max_length=255, blank=True)
    thu_tu = models.PositiveIntegerField("Thứ tự điểm quét")

    class Meta:
        verbose_name = "2. Điểm Tuần Tra (Checkpoint)"
        verbose_name_plural = "2. Các Điểm Tuần Tra (Checkpoints)"
        ordering = ['loai_tuan_tra', 'thu_tu']

    def __str__(self):
        return f"{self.loai_tuan_tra.ten_loai} - Điểm {self.thu_tu}: {self.ten_diem}"

class LuotTuanTra(models.Model):
    class TrangThai(models.TextChoices):
        DANG_TIEN_HANH = 'IN_PROGRESS', 'Đang tiến hành'
        HOAN_THANH = 'COMPLETED', 'Hoàn thành'
        KHONG_HOAN_THANH = 'INCOMPLETE', 'Không hoàn thành'

    loai_tuan_tra = models.ForeignKey(LoaiTuanTra, on_delete=models.CASCADE, null=True, blank=True)
    ca_truc = models.ForeignKey(PhanCongCaTruc, on_delete=models.CASCADE, null=True, blank=True)
    thoi_gian_bat_dau = models.DateTimeField(default=timezone.now)
    thoi_gian_ket_thuc = models.DateTimeField(null=True, blank=True)
    trang_thai = models.CharField(max_length=20, choices=TrangThai.choices, default=TrangThai.DANG_TIEN_HANH)

    class Meta:
        verbose_name = "3. Lượt Tuần Tra"
        verbose_name_plural = "3. Các Lượt Tuần Tra"
        ordering = ['-thoi_gian_bat_dau']

    def __str__(self):
        if self.loai_tuan_tra:
            return f"Lượt tuần tra {self.loai_tuan_tra.ten_loai} lúc {self.thoi_gian_bat_dau.strftime('%H:%M %d/%m')}"
        return f"Lượt tuần tra (chưa xác định) lúc {self.thoi_gian_bat_dau.strftime('%H:%M %d/%m')}"


class GhiNhanTuanTra(models.Model):
    luot_tuan_tra = models.ForeignKey(LuotTuanTra, on_delete=models.CASCADE, related_name='cac_ghi_nhan')
    diem_tuan_tra = models.ForeignKey(DiemTuanTra, on_delete=models.CASCADE)
    thoi_gian_quet = models.DateTimeField(default=timezone.now)
    ghi_chu = models.TextField("Ghi chú", blank=True)
    hinh_anh = models.ImageField("Hình ảnh", upload_to='ghi_nhan_tuan_tra/', null=True, blank=True)

    class Meta:
        verbose_name = "4. Ghi Nhận Tuần Tra"
        verbose_name_plural = "4. Các Ghi Nhận Tuần Tra"
        ordering = ['thoi_gian_quet']

    def __str__(self):
        return f"Quét điểm {self.diem_tuan_tra.ten_diem} lúc {self.thoi_gian_quet.strftime('%H:%M')}"

# ==============================================================================
# PHẦN 2: CÁC MODEL CHO NGHIỆP VỤ THANH TRA (GIÁM SÁT CON NGƯỜI & MỤC TIÊU)
# ==============================================================================

class HangMucKiemTra(models.Model):
    class NhomKiemTra(models.TextChoices):
        NV_TAC_PHONG = 'NV_TAC_PHONG', 'NV: Tác phong - Điều lệnh'
        NV_NGHIEP_VU = 'NV_NGHIEP_VU', 'NV: Kiến thức nghiệp vụ'
        MT_NHAN_SU = 'MT_NHAN_SU', 'Mục tiêu: Tình hình nhân sự'
        MT_CONG_CU = 'MT_CONG_CU', 'Mục tiêu: Công cụ & Sổ sách'
        MT_AN_NINH = 'MT_AN_NINH', 'Mục tiêu: Tình hình an ninh'
        KHAC = 'KHAC', 'Khác'

    noi_dung = models.CharField("Nội dung/Tiêu chí kiểm tra", max_length=255)
    nhom_kiem_tra = models.CharField("Nhóm kiểm tra", max_length=20, choices=NhomKiemTra.choices)
    is_active = models.BooleanField("Đang áp dụng", default=True)

    class Meta:
        verbose_name = "5. Hạng mục Thanh tra"
        verbose_name_plural = "5. Các Hạng mục Thanh tra"
        ordering = ['nhom_kiem_tra', 'noi_dung']

    def __str__(self):
        return f"[{self.get_nhom_kiem_tra_display()}] {self.noi_dung}"

class BienBanThanhTra(models.Model):
    class LoaiThanhTra(models.TextChoices):
        NV_DINH_KY = 'NV_DINH_KY', 'Thanh tra Nhân viên (Định kỳ)'
        NV_DOT_XUAT = 'NV_DOT_XUAT', 'Thanh tra Nhân viên (Đột xuất)'
        MT_DINH_KY = 'MT_DINH_KY', 'Thanh tra Mục tiêu (Định kỳ)'
        MT_DOT_XUAT = 'MT_DOT_XUAT', 'Thanh tra Mục tiêu (Đột xuất)'

    thanh_tra_vien = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True, related_name='cac_cuoc_thanh_tra', verbose_name="Thanh tra viên")
    # Cho phép để trống nếu là thanh tra toàn mục tiêu
    nhan_vien_duoc_kiem_tra = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True, blank=True, related_name='cac_lan_bi_thanh_tra', verbose_name="Nhân viên được kiểm tra")
    muc_tieu = models.ForeignKey(MucTieu, on_delete=models.SET_NULL, null=True, verbose_name="Mục tiêu kiểm tra")
    thoi_gian_kiem_tra = models.DateTimeField("Thời gian kiểm tra", default=timezone.now)
    loai_thanh_tra = models.CharField("Loại hình", max_length=20, choices=LoaiThanhTra.choices)
    danh_gia_chung = models.TextField("Đánh giá chung và Biện pháp khắc phục", blank=True)

    class Meta:
        verbose_name = "6. Biên bản Thanh tra"
        verbose_name_plural = "6. Các Biên bản Thanh tra"
        ordering = ['-thoi_gian_kiem_tra']

    def __str__(self):
        return f"BBTT tại {self.muc_tieu} lúc {self.thoi_gian_kiem_tra.strftime('%H:%M %d/%m/%Y')}"

class KetQuaKiemTra(models.Model):
    class KetQua(models.TextChoices):
        DAT = 'DAT', 'Đạt'
        KHONG_DAT = 'KHONG_DAT', 'Không đạt'
        CAI_THIEN = 'CAI_THIEN', 'Cần cải thiện'
    
    bien_ban = models.ForeignKey(BienBanThanhTra, on_delete=models.CASCADE, related_name='ket_qua_chi_tiet')
    hang_muc = models.ForeignKey(HangMucKiemTra, on_delete=models.PROTECT, verbose_name="Hạng mục")
    ket_qua = models.CharField("Kết quả", max_length=20, choices=KetQua.choices)
    ghi_chu = models.TextField("Ghi chú/Chi tiết", blank=True)
    
    class Meta:
        verbose_name = "7. Kết quả Thanh tra Chi tiết"
        verbose_name_plural = "7. Các Kết quả Thanh tra Chi tiết"

    def __str__(self):
        return f"{self.hang_muc.noi_dung}: {self.get_ket_qua_display()}"

# ==============================================================================
# PHẦN 3: CÁC MODEL MỚI CHO NGHIỆP VỤ ĐÀO TẠO
# ==============================================================================

class BuoiHuanLuyen(models.Model):
    ten_buoi_huan_luyen = models.CharField("Tên buổi huấn luyện/đào tạo", max_length=255)
    noi_dung = models.TextField("Nội dung chính")
    giang_vien = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True, blank=True, related_name='cac_buoi_giang_day', verbose_name="Giảng viên/Người hướng dẫn")
    ngay_to_chuc = models.DateField("Ngày tổ chức")
    thoi_luong = models.CharField("Thời lượng (ví dụ: 4 giờ)", max_length=50, blank=True)
    nhan_vien_tham_gia = models.ManyToManyField(NhanVien, related_name='cac_buoi_dao_tao_da_hoc', verbose_name="Nhân viên tham gia")

    class Meta:
        verbose_name = "8. Buổi Huấn luyện & Đào tạo"
        verbose_name_plural = "8. Các Buổi Huấn luyện & Đào tạo"
        ordering = ['-ngay_to_chuc']

    def __str__(self):
        return self.ten_buoi_huan_luyen

