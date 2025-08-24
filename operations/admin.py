# file: operations/admin.py
from django.contrib import admin
from .models import CaLamViec, PhanCongCaTruc, ChamCong, BaoCaoSuCo

@admin.register(CaLamViec)
class CaLamViecAdmin(admin.ModelAdmin):
    list_display = ('ten_ca', 'gio_bat_dau', 'gio_ket_thuc')

@admin.register(PhanCongCaTruc)
class PhanCongCaTrucAdmin(admin.ModelAdmin):
    list_display = ('nhan_vien', 'muc_tieu', 'ca_lam_viec', 'ngay_truc')
    list_filter = ('muc_tieu', 'ca_lam_viec', 'ngay_truc')
    search_fields = ('nhan_vien__ho_ten', 'muc_tieu__ten_muc_tieu')

@admin.register(ChamCong)
class ChamCongAdmin(admin.ModelAdmin):
    list_display = ('ca_truc', 'thoi_gian_check_in', 'thoi_gian_check_out')

@admin.register(BaoCaoSuCo)
class BaoCaoSuCoAdmin(admin.ModelAdmin):
    list_display = ('tieu_de', 'ca_truc', 'thoi_gian_bao_cao')