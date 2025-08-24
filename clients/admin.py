# file: clients/admin.py
from django.contrib import admin
from .models import KhachHang, HopDong, MucTieu

@admin.register(KhachHang)
class KhachHangAdmin(admin.ModelAdmin):
    list_display = ('ten_cong_ty', 'nguoi_lien_he', 'sdt_lien_he')
    search_fields = ('ten_cong_ty',)

@admin.register(HopDong)
class HopDongAdmin(admin.ModelAdmin):
    list_display = ('so_hop_dong', 'khach_hang', 'ngay_hieu_luc', 'ngay_het_han')
    search_fields = ('so_hop_dong', 'khach_hang__ten_cong_ty')
    list_filter = ('khach_hang',)

@admin.register(MucTieu)
class MucTieuAdmin(admin.ModelAdmin):
    list_display = ('ten_muc_tieu', 'hop_dong')
    search_fields = ('ten_muc_tieu', 'hop_dong__so_hop_dong')
    list_filter = ('hop_dong__khach_hang',)