# file: main/admin.py
from django.contrib import admin
from .models import CompanyProfile # Sửa ThongTinCongTy thành CompanyProfile

# Đăng ký model CompanyProfile vào trang admin
@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('ten_cong_ty', 'email', 'sdt', 'website')