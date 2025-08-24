# file: inventory/admin.py
from django.contrib import admin
from .models import VatTu, CapPhatCaNhan, CapPhatMucTieu

@admin.register(VatTu)
class VatTuAdmin(admin.ModelAdmin):
    list_display = ('ten_vat_tu', 'don_vi_tinh', 'so_luong_ton_kho')
    search_fields = ('ten_vat_tu',)

@admin.register(CapPhatCaNhan)
class CapPhatCaNhanAdmin(admin.ModelAdmin):
    list_display = ('nhan_vien', 'vat_tu', 'so_luong', 'ngay_cap_phat')

@admin.register(CapPhatMucTieu)
class CapPhatMucTieuAdmin(admin.ModelAdmin):
    list_display = ('muc_tieu', 'vat_tu', 'so_luong', 'ngay_cap_phat')