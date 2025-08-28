# file: inspection/admin.py
from django.contrib import admin
from .models import PhieuThanhTra, KhoaHoc, DangKyHoc

@admin.register(PhieuThanhTra)
class PhieuThanhTraAdmin(admin.ModelAdmin):
    list_display = ('muc_tieu', 'nhan_vien_thanh_tra', 'nhan_vien_bi_thanh_tra', 'ngay_thanh_tra')
    list_filter = ('muc_tieu',)
    search_fields = ('muc_tieu__ten_muc_tieu', 'nhan_vien_bi_thanh_tra__ho_ten')

@admin.register(KhoaHoc)
class KhoaHocAdmin(admin.ModelAdmin):
    list_display = ('ten_khoa_hoc',)
    search_fields = ('ten_khoa_hoc',)

@admin.register(DangKyHoc)
class DangKyHocAdmin(admin.ModelAdmin):
    list_display = ('nhan_vien', 'khoa_hoc', 'trang_thai', 'ngay_dang_ky')
    list_filter = ('khoa_hoc', 'trang_thai')
    search_fields = ('nhan_vien__ho_ten', 'khoa_hoc__ten_khoa_hoc')