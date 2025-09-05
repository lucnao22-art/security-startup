# file: inspection/admin.py

from django.contrib import admin
# Sửa lại import để sử dụng đúng tên model đã khôi phục
from .models import LoaiTuanTra, DiemTuanTra, LuotTuanTra, GhiNhanTuanTra

@admin.register(LoaiTuanTra)
class LoaiTuanTraAdmin(admin.ModelAdmin):
    list_display = ('ten_loai', 'muc_tieu')
    list_filter = ('muc_tieu',)
    search_fields = ('ten_loai',)

@admin.register(DiemTuanTra)
class DiemTuanTraAdmin(admin.ModelAdmin):
    list_display = ('ten_diem', 'loai_tuan_tra', 'thu_tu', 'ma_qr')
    list_filter = ('loai_tuan_tra__muc_tieu', 'loai_tuan_tra')
    search_fields = ('ten_diem', 'ma_qr')

@admin.register(LuotTuanTra)
class LuotTuanTraAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'ca_truc', 'trang_thai', 'thoi_gian_bat_dau')
    list_filter = ('trang_thai', 'ca_truc__vi_tri_chot__muc_tieu')
    search_fields = ('loai_tuan_tra__ten_loai', 'ca_truc__nhan_vien__ho_ten')

@admin.register(GhiNhanTuanTra)
class GhiNhanTuanTraAdmin(admin.ModelAdmin):
    list_display = ('diem_tuan_tra', 'luot_tuan_tra', 'thoi_gian_quet')
    list_filter = ('luot_tuan_tra__ca_truc__vi_tri_chot__muc_tieu',)
    search_fields = ('diem_tuan_tra__ten_diem',)