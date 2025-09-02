# file: users/admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import (
    NhanVien,
    PhongBan,
    ChucDanh,
    LichSuCongTac,
    HocVan,
    BangCapChungChi,
    CauHinhMaNhanVien,
)


# --- CÁC LỚP ADMIN CHO MODEL PHỤ ---

@admin.register(ChucDanh)
class ChucDanhAdmin(admin.ModelAdmin):
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
    list_display = ("ten_phong_ban", "link_den_nhom_quyen")
    search_fields = ("ten_phong_ban",)

    def link_den_nhom_quyen(self, obj):
        if obj.nhom_quyen:
            url = reverse("admin:auth_group_change", args=[obj.nhom_quyen.id])
            return format_html('<a href="{}">Thiết lập Quyền chung</a>', url)
        return "Chưa gán"
    link_den_nhom_quyen.short_description = "Nhóm Quyền chung"


# --- CẤU HÌNH HIỂN THỊ INLINE ---

class HocVanInline(admin.TabularInline):
    model = HocVan
    extra = 1
    verbose_name_plural = "Quá trình Học vấn"

class BangCapChungChiInline(admin.TabularInline):
    model = BangCapChungChi
    extra = 1
    verbose_name_plural = "Bằng cấp & Chứng chỉ"

class LichSuCongTacInline(admin.TabularInline):
    model = LichSuCongTac
    fk_name = "nhan_vien"
    extra = 1
    verbose_name_plural = "Lịch sử Công tác & Vị trí"
    raw_id_fields = ("quan_ly_truc_tiep", "muc_tieu",)


# --- CẤU HÌNH TRANG ADMIN NHÂN VIÊN (PHIÊN BẢN SỬA LỖI CUỐI CÙNG) ---

@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    list_display = ("ma_nhan_vien", "ho_ten", "phong_ban", "chuc_danh", "trang_thai_lam_viec")
    list_filter = ("trang_thai_lam_viec", "phong_ban", "chuc_danh", "gioi_tinh")
    search_fields = ('ho_ten', 'ma_nhan_vien', 'so_cccd', 'sdt_chinh', 'email')
    raw_id_fields = ("user",)

    readonly_fields = ('ma_nhan_vien', 'image_tag', 'xuat_ly_lich')

    def image_tag(self, obj):
        if obj.anh_the:
            return format_html('<img src="{}" style="max-width: 150px; height: auto; border-radius: 8px;" />', obj.anh_the.url)
        return "Chưa có ảnh thẻ"
    image_tag.short_description = 'Ảnh thẻ hiện tại'

    def xuat_ly_lich(self, obj):
        if obj.pk:
            # SỬA LỖI DỨT ĐIỂM: Trỏ đến trang tùy chọn "export-ly-lich-options"
            url = reverse("users:export-ly-lich-options", args=[obj.pk])
            return format_html('<a href="{}" class="btn btn-info" target="_blank"><i class="fas fa-print me-1"></i> Xuất Trích ngang Lý lịch</a>', url)
        return "Lưu nhân viên để bật chức năng này"
    xuat_ly_lich.short_description = 'Tác vụ'

    fieldsets = (
        ("Tài khoản & Tác vụ", {
            "fields": ("user", "phong_ban", "chuc_danh", "xuat_ly_lich")
        }),
        ("Thông tin Cá nhân", {
            "fields": (
                "ma_nhan_vien", "ho_ten",
                "image_tag", "anh_the",
                ('ngay_sinh', 'gioi_tinh'),
                ('so_cccd', 'sdt_chinh', 'email'),
            )
        }),
        ("Thông tin Công việc & Hợp đồng", {
            "fields": ('ngay_vao_lam', 'trang_thai_lam_viec', 'loai_hop_dong')
        }),
        ("Thông tin Cư trú & Khẩn cấp", {
            'classes': ('collapse',),
            'fields': ('dia_chi_thuong_tru', 'dia_chi_tam_tru', ('nguoi_lien_he_khan_cap', 'sdt_khan_cap'))
        }),
        ("Thông tin Thanh toán", {
            'classes': ('collapse',),
            'fields': (('so_tai_khoan', 'ngan_hang', 'chi_nhanh_ngan_hang'),)
        }),
    )

    inlines = [HocVanInline, BangCapChungChiInline, LichSuCongTacInline]

    jazzmin_opts = {
        "tabs": [
            {
                "name": "Thông tin chung", "fieldsets": ["Tài khoản & Tác vụ", "Thông tin Cá nhân", "Thông tin Công việc & Hợp đồng"],
            },
            {
                "name": "Hồ sơ & Năng lực", "inlines": ["HocVanInline", "BangCapChungChiInline"],
            },
            {
                "name": "Lịch sử Công tác", "inlines": ["LichSuCongTacInline"],
            },
            {
                "name": "Thông tin khác", "fieldsets": ["Thông tin Cư trú & Khẩn cấp", "Thông tin Thanh toán"],
            },
        ]
    }


# --- ĐĂNG KÝ CÁC MODEL CÒN LẠI ---
admin.site.register(CauHinhMaNhanVien)

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