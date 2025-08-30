# file: core/admin.py
from django.contrib import admin
from .models import ThongTinCongTy, PhongBan, ChucDanh

@admin.register(ThongTinCongTy)
class ThongTinCongTyAdmin(admin.ModelAdmin):
    # Chỉ cho phép có 1 bản ghi thông tin công ty duy nhất
    def has_add_permission(self, request):
        return ThongTinCongTy.objects.count() == 0

@admin.register(PhongBan)
class PhongBanAdmin(admin.ModelAdmin):
    list_display = ('ten_phong_ban', 'mo_ta')
    search_fields = ('ten_phong_ban',)

@admin.register(ChucDanh)
class ChucDanhAdmin(admin.ModelAdmin):
    list_display = ('ten_chuc_danh', 'phong_ban')
    list_filter = ('phong_ban',)
    search_fields = ('ten_chuc_danh',)
