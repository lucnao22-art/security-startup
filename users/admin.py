# file: users/admin.py (Bố cục MỘT HÀNG MỘT TRƯỜNG)
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import (
    NhanVien, PhongBan, ChucDanh, LichSuCongTac, HocVan, BangCapChungChi,
    CauHinhMaNhanVien, MauVanBan, HopDongLaoDong, QuyetDinh
)

# --- ADMIN CHO CÁC MODEL CẤU HÌNH VÀ PHỤ TRỢ ---
@admin.register(ChucDanh)
class ChucDanhAdmin(admin.ModelAdmin):
    # ... (giữ nguyên, không thay đổi)
    list_display = ("ten_chuc_danh", "link_den_nhom_quyen")
    search_fields = ("ten_chuc_danh",)
    def link_den_nhom_quyen(self, obj):
        if obj.nhom_quyen:
            url = reverse("admin:auth_group_change", args=[obj.nhom_quyen.id])
            return format_html('<a href="{}">Thiết lập Quyền</a>', url)
        return "Chưa gán"
    link_den_nhom_quyen.short_description = "Nhóm Quyền"

@admin.register(PhongBan)
class PhongBanAdmin(admin.ModelAdmin):
    # ... (giữ nguyên, không thay đổi)
    list_display = ("ten_phong_ban", "link_den_nhom_quyen")
    search_fields = ("ten_phong_ban",)
    def link_den_nhom_quyen(self, obj):
        if obj.nhom_quyen:
            url = reverse("admin:auth_group_change", args=[obj.nhom_quyen.id])
            return format_html('<a href="{}">Thiết lập Quyền chung</a>', url)
        return "Chưa gán"
    link_den_nhom_quyen.short_description = "Nhóm Quyền chung"

# ... (Các admin class khác giữ nguyên)
@admin.register(MauVanBan)
class MauVanBanAdmin(admin.ModelAdmin):
    list_display = ('ten_mau', 'loai_van_ban')
    list_filter = ('loai_van_ban',)
    search_fields = ('ten_mau',)

@admin.register(HocVan)
class HocVanAdmin(admin.ModelAdmin):
    list_display = ('nhan_vien', 'truong_dao_tao', 'chuyen_nganh', 'trinh_do')
    autocomplete_fields = ['nhan_vien']
    search_fields = ('nhan_vien__ho_ten', 'truong_dao_tao', 'chuyen_nganh')

@admin.register(BangCapChungChi)
class BangCapChungChiAdmin(admin.ModelAdmin):
    list_display = ('nhan_vien', 'ten_bang_cap', 'ngay_cap', 'ngay_het_han')
    autocomplete_fields = ['nhan_vien']
    search_fields = ('nhan_vien__ho_ten', 'ten_bang_cap')


# --- CÁC INLINE CHO TRANG CHI TIẾT NHÂN VIÊN ---
class HocVanInline(admin.TabularInline): model = HocVan; extra = 0
class BangCapChungChiInline(admin.TabularInline): model = BangCapChungChi; extra = 0
class LichSuCongTacInline(admin.TabularInline): model = LichSuCongTac; fk_name = "nhan_vien"; extra = 0; raw_id_fields = ("quan_ly_truc_tiep", "muc_tieu",); ordering = ('-ngay_bat_dau',)
class HopDongLaoDongInline(admin.TabularInline):
    model = HopDongLaoDong
    extra = 0
    readonly_fields = ('in_hop_dong',)
    def in_hop_dong(self, obj):
        if obj.pk and obj.mau_hop_dong:
            url = reverse("users:in-hop-dong", args=[obj.pk])
            return format_html('<a href="{}" class="btn btn-success" target="_blank"><i class="fas fa-print"></i> In</a>', url)
        return "N/A (Lưu để in)"
    in_hop_dong.short_description = "Tác vụ"
class QuyetDinhInline(admin.TabularInline):
    model = QuyetDinh
    extra = 0
    readonly_fields = ('in_quyet_dinh',)
    def in_quyet_dinh(self, obj):
        if obj.pk and obj.mau_quyet_dinh:
            url = reverse("users:in-quyet-dinh", args=[obj.pk])
            return format_html('<a href="{}" class="btn btn-warning" target="_blank"><i class="fas fa-print"></i> In</a>', url)
        return "N/A (Lưu để in)"
    in_quyet_dinh.short_description = "Tác vụ"


# --- ADMIN CHÍNH CHO NHÂN VIÊN ---

@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    list_display = ("avatar_preview", "ma_nhan_vien", "ho_ten", "phong_ban", "chuc_danh", "sdt_chinh", "trang_thai_lam_viec")
    list_filter = ("trang_thai_lam_viec", "phong_ban", "chuc_danh", "gioi_tinh")
    search_fields = ('ho_ten', 'ma_nhan_vien', 'sdt_chinh', 'email')
    raw_id_fields = ("user",)
    readonly_fields = ('ma_nhan_vien_display', 'image_tag', 'xuat_ly_lich')
    actions = ['mark_as_nghi_viec']

    # Hàm tạo khung cho Mã Nhân Viên
    def ma_nhan_vien_display(self, obj):
        if obj.ma_nhan_vien:
            # Bọc mã nhân viên trong div với class 'readonly-input-short'
            return format_html('<div class="readonly-input readonly-input-short">{}</div>', obj.ma_nhan_vien)
        return None
    ma_nhan_vien_display.short_description = "Mã số nhân viên"

    # ... các hàm khác giữ nguyên ...
    def avatar_preview(self, obj): return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;" />', obj.avatar_url)
    avatar_preview.short_description = 'Ảnh'
    def image_tag(self, obj):
        if obj.anh_the: return format_html('<img src="{}" style="max-width: 150px; height: auto; border-radius: 8px;" />', obj.anh_the.url)
        return "Chưa có ảnh"
    image_tag.short_description = 'Ảnh thẻ hiện tại'
    def xuat_ly_lich(self, obj):
        if obj.pk:
            url = reverse("users:export-ly-lich-options", args=[obj.pk])
            return format_html('<a href="{}" class="btn btn-info" target="_blank"><i class="fas fa-print me-1"></i> Xuất Trích ngang</a>', url)
        return "Lưu để bật chức năng này"
    xuat_ly_lich.short_description = 'Tác vụ chung'

    # *** SẮP XẾP LẠI FIELDSETS: MỖI TRƯỜNG MỘT HÀNG ***
    fieldsets = (
        ("Thông tin Công việc & Tài khoản", {
            "fields": (
                'ma_nhan_vien_display', # Trường readonly có khung
                'user',
                'phong_ban',
                'chuc_danh',
                'ngay_vao_lam',
                'trang_thai_lam_viec',
                'xuat_ly_lich'
            )
        }),
        ("Thông tin Cá nhân", {
            "fields": (
                'ho_ten',
                'ngay_sinh',
                'gioi_tinh',
                'so_cccd',
                'sdt_chinh',
                'email',
                ('image_tag', 'anh_the'), # Cặp này đi cùng nhau là hợp lý
            )
        }),
        ("Thông tin Cư trú & Khẩn cấp", {
            'classes': ('collapse',),
            'fields': (
                'dia_chi_thuong_tru',
                'dia_chi_tam_tru',
                'nguoi_lien_he_khan_cap',
                'sdt_khan_cap',
            )
        }),
        ("Thông tin Thanh toán", {
            'classes': ('collapse',),
            'fields': (
                'ngan_hang',
                'chi_nhanh_ngan_hang',
                'so_tai_khoan'
            )
        }),
    )
    
    inlines = [HopDongLaoDongInline, QuyetDinhInline, LichSuCongTacInline, HocVanInline, BangCapChungChiInline]
    
    # ... (jazzmin_opts giữ nguyên)
    jazzmin_opts = { "tabs": [ {"name": "Thông tin chung", "fieldsets": ["Thông tin Công việc & Tài khoản", "Thông tin Cá nhân"]}, {"name": "Hợp đồng & Quyết định", "inlines": ["HopDongLaoDongInline", "QuyetDinhInline"]}, {"name": "Quá trình công tác", "inlines": ["LichSuCongTacInline"]}, {"name": "Hồ sơ & Năng lực", "inlines": ["HocVanInline", "BangCapChungChiInline"]}, {"name": "Thông tin khác", "fieldsets": ["Thông tin Cư trú & Khẩn cấp", "Thông tin Thanh toán"]}, ] }
    @admin.action(description="Chuyển trạng thái thành 'Đã nghỉ việc'")
    def mark_as_nghi_viec(self, request, queryset): queryset.update(trang_thai_lam_viec=NhanVien.TrangThaiLamViec.NGHI_VIEC); self.message_user(request, "Đã cập nhật trạng thái cho các nhân viên được chọn.")

# --- ĐĂNG KÝ MODEL CÒN LẠI ---
admin.site.register(CauHinhMaNhanVien)