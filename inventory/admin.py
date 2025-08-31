# file: inventory/admin.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import VatTu, CapPhatCaNhan, CapPhatMucTieu, TrangBiTieuChuan


@admin.register(VatTu)
class VatTuAdmin(admin.ModelAdmin):
    list_display = ("ten_vat_tu", "don_vi_tinh", "so_luong_ton_kho")
    search_fields = ("ten_vat_tu",)

    # Ghi đè để thêm URL báo cáo
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "report/",
                self.admin_site.admin_view(self.report_view),
                name="inventory_vattu_report",
            ),
        ]
        return custom_urls + urls

    # View để hiển thị trang báo cáo
    def report_view(self, request):
        vat_tu_list = VatTu.objects.all().order_by("ten_vat_tu")
        context = dict(
            self.admin_site.each_context(request),
            vat_tu_list=vat_tu_list,
        )
        return render(request, "admin/inventory/vattu/report.html", context)

    # Ghi đè để thêm nút "Báo cáo" vào giao diện
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["report_button_url"] = "report/"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(CapPhatCaNhan)
class CapPhatCaNhanAdmin(admin.ModelAdmin):
    list_display = ("nhan_vien", "vat_tu", "so_luong", "ngay_cap_phat")
    autocomplete_fields = ["nhan_vien", "vat_tu"]


@admin.register(CapPhatMucTieu)
class CapPhatMucTieuAdmin(admin.ModelAdmin):
    list_display = ("muc_tieu", "vat_tu", "so_luong", "ngay_cap_phat")
    autocomplete_fields = ["muc_tieu", "vat_tu"]


@admin.register(TrangBiTieuChuan)
class TrangBiTieuChuanAdmin(admin.ModelAdmin):
    list_display = ("vat_tu", "so_luong")
    autocomplete_fields = ["vat_tu"]
