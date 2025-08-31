# file: accounting/admin.py
from django.contrib import admin
from .models import BangLuong, HoaDon


@admin.register(BangLuong)
class BangLuongAdmin(admin.ModelAdmin):
    list_display = ("nhan_vien", "ky_tinh_luong", "thuc_lanh")
    list_filter = ("ky_tinh_luong",)
    search_fields = ("nhan_vien__ho_ten",)


@admin.register(HoaDon)
class HoaDonAdmin(admin.ModelAdmin):
    list_display = ("hop_dong", "ky_thanh_toan", "so_tien", "trang_thai")
    list_filter = ("trang_thai", "ky_thanh_toan")
    search_fields = ("hop_dong__khach_hang__ten_cong_ty",)
