# file: clients/admin.py
from django.contrib import admin
from .models import KhachHang, HopDong, MucTieu
from operations.models import ViTriChot # Import từ app operations

class ViTriChotInline(admin.TabularInline):
    model = ViTriChot
    extra = 1

@admin.register(KhachHang)
class KhachHangAdmin(admin.ModelAdmin):
    list_display = ('ten_cong_ty', 'nguoi_lien_he', 'sdt_lien_he')
    search_fields = ('ten_cong_ty',)

@admin.register(HopDong)
class HopDongAdmin(admin.ModelAdmin):
    list_display = ('so_hop_dong', 'khach_hang', 'ngay_hieu_luc', 'ngay_het_han')
    search_fields = ('so_hop_dong', 'khach_hang__ten_cong_ty')
    list_filter = ('khach_hang',)
    autocomplete_fields = ['khach_hang']

@admin.register(MucTieu)
class MucTieuAdmin(admin.ModelAdmin):
    inlines = [ViTriChotInline]
    fields = ('hop_dong', 'ten_muc_tieu', 'dia_chi', 'chi_huy_truong')
    list_display = ('ten_muc_tieu', 'hop_dong', 'chi_huy_truong')
    search_fields = ('ten_muc_tieu', 'hop_dong__so_hop_dong', 'chi_huy_truong__ho_ten')
    list_filter = ('hop_dong__khach_hang',)
    autocomplete_fields = ['hop_dong', 'chi_huy_truong']