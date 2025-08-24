# file: users/admin.py

from django.contrib import admin
from .models import NhanVien

@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    list_display = (
        'ma_nhan_vien', 
        'ho_ten', 
        'sdt_chinh', 
        'trang_thai_lam_viec',
    )
    list_filter = (
        'trang_thai_lam_viec',
        'gioi_tinh',
    )
    search_fields = (
        'ma_nhan_vien',
        'ho_ten',
        'sdt_chinh',
        'so_cccd',
    )
    ordering = ('ma_nhan_vien',)
    fieldsets = (
        ('Thông tin Cơ bản', {
            'fields': ('ma_nhan_vien', 'ho_ten', 'anh_the', ('ngay_sinh', 'gioi_tinh'), ('chieu_cao', 'can_nang'))
        }),
        ('Thông tin Định danh & Liên lạc', {
            'fields': ('so_cccd', 'ngay_cap_cccd', 'noi_cap_cccd', ('sdt_chinh', 'sdt_phu'), 'email', 'dia_chi_thuong_tru', 'dia_chi_tam_tru')
        }),
        ('Thông tin Công việc & Khác', {
            'fields': ('trang_thai_lam_viec', 'trinh_do_hoc_van', 'trang_thai_hon_nhan', 'nguoi_gioi_thieu')
        }),
        ('Thông tin Khẩn cấp & Tài chính', {
            'fields': (('ten_lien_he_khan_cap', 'quan_he_khan_cap', 'sdt_khan_cap'), 'thong_tin_suc_khoe', 'thong_tin_ngan_hang')
        }),
    )