# file: users/admin.py

from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from .models import NhanVien, PhongBan, CauHinhMaNhanVien, ChungChi, LichSuCongTac
from inventory.models import TrangBiTieuChuan, CapPhatCaNhan

class ChungChiInline(admin.TabularInline):
    model = ChungChi
    extra = 1

class CapPhatCaNhanInline(admin.TabularInline):
    model = CapPhatCaNhan
    extra = 0
    autocomplete_fields = ['vat_tu']
    readonly_fields = ('ngay_cap_phat',)

class LichSuCongTacInline(admin.TabularInline):
    model = LichSuCongTac
    extra = 1
    autocomplete_fields = ['muc_tieu']

@admin.register(CauHinhMaNhanVien)
class CauHinhMaNhanVienAdmin(admin.ModelAdmin):
    list_display = ('tien_to', 'do_dai_so', 'so_hien_tai')
    
    def has_add_permission(self, request):
        return CauHinhMaNhanVien.objects.count() == 0

@admin.register(PhongBan)
class PhongBanAdmin(admin.ModelAdmin):
    list_display = ('ten_phong_ban', 'mo_ta')
    search_fields = ('ten_phong_ban',)

@admin.register(ChungChi)
class ChungChiAdmin(admin.ModelAdmin):
    list_display = ('ten_chung_chi', 'nhan_vien', 'ngay_cap', 'ngay_het_han')
    autocomplete_fields = ['nhan_vien']

@admin.register(LichSuCongTac)
class LichSuCongTacAdmin(admin.ModelAdmin):
    list_display = ('nhan_vien', 'muc_tieu', 'chuc_vu', 'ngay_bat_dau')
    autocomplete_fields = ['nhan_vien', 'muc_tieu']

@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    inlines = [ChungChiInline, CapPhatCaNhanInline, LichSuCongTacInline]
    
    actions = ['cap_phat_tieu_chuan']

    def cap_phat_tieu_chuan(self, request, queryset):
        trang_bi_list = TrangBiTieuChuan.objects.all()
        if not trang_bi_list.exists():
            messages.error(request, "Chưa có trang bị tiêu chuẩn nào được thiết lập.")
            return

        for nhan_vien in queryset:
            for trang_bi in trang_bi_list:
                CapPhatCaNhan.objects.get_or_create(
                    nhan_vien=nhan_vien,
                    vat_tu=trang_bi.vat_tu,
                    defaults={'so_luong': trang_bi.so_luong}
                )
            self.message_user(request, f"Đã tự động cấp phát trang bị tiêu chuẩn cho {nhan_vien.ho_ten}.")
    cap_phat_tieu_chuan.short_description = "Cấp phát trang bị tiêu chuẩn cho nhân viên đã chọn"
    
    list_display = ('ma_nhan_vien', 'ho_ten', 'phong_ban', 'chuc_vu', 'sdt_chinh')
    list_filter = ('phong_ban', 'chuc_vu', 'trang_thai_lam_viec', 'gioi_tinh')
    search_fields = ('ma_nhan_vien', 'ho_ten')
    ordering = ('-ma_nhan_vien',)
    autocomplete_fields = ['user', 'muc_tieu_lam_viec', 'quan_ly_truc_tiep', 'nguoi_gioi_thieu']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['ma_nhan_vien', 'xuat_ly_lich']
        return ['xuat_ly_lich']

    def xuat_ly_lich(self, obj):
        if obj.pk:
            url = reverse('users:export-ly-lich', args=[obj.pk])
            return format_html(f'<a href="{url}" class="button" target="_blank">Xuất Lý lịch (PDF)</a>')
        return "Lưu nhân viên trước khi xuất"
    xuat_ly_lich.short_description = 'Hành động'

    def get_fieldsets(self, request, obj=None):
        base_fieldsets = [
            ('Thông tin Định danh & Liên lạc', {
                'fields': ('so_cccd', 'ngay_cap_cccd', 'noi_cap_cccd', ('sdt_chinh', 'sdt_phu'), 'email', 'dia_chi_thuong_tru', 'dia_chi_tam_tru')
            }),
            ('Thông tin Công việc & Khác', {
                'fields': ('trang_thai_lam_viec', 'muc_tieu_lam_viec', 'nguoi_gioi_thieu', 'trang_thai_hon_nhan')
            }),
            ('Thông tin Khẩn cấp & Tài chính', {
                'fields': (('ten_lien_he_khan_cap', 'quan_he_khan_cap', 'sdt_khan_cap'), 'thong_tin_suc_khoe', 'thong_tin_ngan_hang')
            }),
        ]

        if obj: # Khi SỬA
            return [
                ('Tài khoản & Phân quyền', {'fields': ('user', 'phong_ban', 'chuc_vu', 'quan_ly_truc_tiep')}),
                ('Thông tin Cơ bản', {'fields': ('ma_nhan_vien', 'ho_ten', 'anh_the', ('ngay_sinh', 'gioi_tinh'), ('chieu_cao', 'can_nang'))}),
                ('Hành động', {'fields': ('xuat_ly_lich',)}),
            ] + base_fieldsets
        else: # Khi THÊM MỚI
            return [
                ('Tài khoản & Phân quyền', {'fields': ('phong_ban', 'chuc_vu', 'quan_ly_truc_tiep')}),
                ('Thông tin Cơ bản', {'fields': ('ho_ten', 'anh_the', ('ngay_sinh', 'gioi_tinh'), ('chieu_cao', 'can_nang'))}),
            ] + base_fieldsets