# file: operations/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ViTriChot,
    CaLamViec,
    PhanCongCaTruc,
    ChamCong,
    BaoCaoSuCo,
    BaoCaoDeXuat,
)
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from users.models import NhanVien
from clients.models import MucTieu


# --- CÁC LỚP RESOURCE ĐỂ XUẤT EXCEL (GIỮ NGUYÊN VÀ HOÀN THIỆN) ---

class PhanCongCaTrucResource(resources.ModelResource):
    nhan_vien = resources.Field(
        attribute="nhan_vien__ho_ten",
        column_name="Nhân viên",
    )
    muc_tieu = resources.Field(
        attribute="vi_tri_chot__muc_tieu__ten_muc_tieu",
        column_name="Mục tiêu",
    )
    vi_tri_chot = resources.Field(
        attribute="vi_tri_chot__ten_vi_tri",
        column_name="Vị trí chốt",
    )
    ca_lam_viec = resources.Field(
        attribute="ca_lam_viec__ten_ca",
        column_name="Ca làm việc",
    )
    ngay_truc = resources.Field(attribute="ngay_truc", column_name="Ngày trực")

    class Meta:
        model = PhanCongCaTruc
        fields = ("id", "ngay_truc", "nhan_vien", "muc_tieu", "vi_tri_chot", "ca_lam_viec")
        export_order = fields


class ChamCongResource(resources.ModelResource):
    nhan_vien = resources.Field(attribute="ca_truc__nhan_vien__ho_ten", column_name="Nhân viên")
    ma_nhan_vien = resources.Field(attribute="ca_truc__nhan_vien__ma_nhan_vien", column_name="Mã NV")
    muc_tieu = resources.Field(attribute="ca_truc__vi_tri_chot__muc_tieu__ten_muc_tieu", column_name="Mục tiêu")
    vi_tri_chot = resources.Field(attribute="ca_truc__vi_tri_chot__ten_vi_tri", column_name="Vị trí chốt")
    ca_lam_viec = resources.Field(attribute="ca_truc__ca_lam_viec__ten_ca", column_name="Ca làm việc")
    ngay_truc = resources.Field(attribute="ca_truc__ngay_truc", column_name="Ngày trực")

    class Meta:
        model = ChamCong
        fields = (
            "id", "ngay_truc", "nhan_vien", "ma_nhan_vien", "muc_tieu", "vi_tri_chot", 
            "ca_lam_viec", "thoi_gian_check_in", "thoi_gian_check_out",
        )
        export_order = fields


# --- CÁC LỚP ADMIN CHO TỪNG MODEL ---

@admin.register(ViTriChot)
class ViTriChotAdmin(admin.ModelAdmin):
    list_display = ("ten_vi_tri", "muc_tieu")
    search_fields = ("ten_vi_tri", "muc_tieu__ten_muc_tieu")
    list_filter = ("muc_tieu",)


@admin.register(CaLamViec)
class CaLamViecAdmin(admin.ModelAdmin):
    list_display = ("ten_ca", "gio_bat_dau", "gio_ket_thuc")
    search_fields = ("ten_ca",)


@admin.register(PhanCongCaTruc)
class PhanCongCaTrucAdmin(ImportExportModelAdmin): # Kế thừa ImportExportModelAdmin
    resource_class = PhanCongCaTrucResource # Liên kết với Resource
    list_display = (
        "ngay_truc",
        "get_muc_tieu",
        "vi_tri_chot",
        "nhan_vien",
        "ca_lam_viec",
    )
    list_filter = ("ngay_truc", "vi_tri_chot__muc_tieu", "ca_lam_viec")
    search_fields = ("nhan_vien__ho_ten", "vi_tri_chot__ten_vi_tri", "nhan_vien__ma_nhan_vien")
    autocomplete_fields = ["nhan_vien", "vi_tri_chot", "ca_lam_viec"]
    list_select_related = ("vi_tri_chot__muc_tieu", "nhan_vien", "ca_lam_viec")

    @admin.display(description="Mục tiêu", ordering="vi_tri_chot__muc_tieu")
    def get_muc_tieu(self, obj):
        return obj.vi_tri_chot.muc_tieu.ten_muc_tieu


@admin.register(ChamCong)
class ChamCongAdmin(ImportExportModelAdmin): # Kế thừa ImportExportModelAdmin
    resource_class = ChamCongResource # Liên kết với Resource
    list_display = (
        "get_nhan_vien",
        "get_muc_tieu",
        "get_ngay_truc",
        "get_ca_lam_viec",
        "thoi_gian_check_in",
        "thoi_gian_check_out",
        "xem_anh_check_in",
        "xem_anh_check_out",
    )
    list_filter = ("ca_truc__ngay_truc", "ca_truc__vi_tri_chot__muc_tieu", "ca_truc__nhan_vien")
    search_fields = ("ca_truc__nhan_vien__ho_ten", "ca_truc__nhan_vien__ma_nhan_vien")
    list_per_page = 20
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related(
            'ca_truc__nhan_vien', 
            'ca_truc__vi_tri_chot__muc_tieu', 
            'ca_truc__ca_lam_viec'
        )

    @admin.display(description='Nhân viên', ordering='ca_truc__nhan_vien__ho_ten')
    def get_nhan_vien(self, obj):
        return obj.ca_truc.nhan_vien

    @admin.display(description='Mục tiêu', ordering='ca_truc__vi_tri_chot__muc_tieu')
    def get_muc_tieu(self, obj):
        return obj.ca_truc.vi_tri_chot.muc_tieu
        
    @admin.display(description='Ngày trực', ordering='ca_truc__ngay_truc')
    def get_ngay_truc(self, obj):
        return obj.ca_truc.ngay_truc
        
    @admin.display(description='Ca làm việc', ordering='ca_truc__ca_lam_viec')
    def get_ca_lam_viec(self, obj):
        return obj.ca_truc.ca_lam_viec

    @admin.display(description='Ảnh Check-in')
    def xem_anh_check_in(self, obj):
        if obj.anh_check_in:
            return format_html('<a href="{0}" target="_blank"><img src="{0}" width="60" /></a>', obj.anh_check_in.url)
        return "Chưa có"

    @admin.display(description='Ảnh Check-out')
    def xem_anh_check_out(self, obj):
        if obj.anh_check_out:
            return format_html('<a href="{0}" target="_blank"><img src="{0}" width="60" /></a>', obj.anh_check_out.url)
        return "Chưa có"


@admin.register(BaoCaoSuCo)
class BaoCaoSuCoAdmin(admin.ModelAdmin):
    list_display = (
        "tieu_de",
        "ca_truc",
        "trang_thai",
        "nguoi_chiu_trach_nhiem",
        "thoi_gian_bao_cao",
    )
    list_filter = ("trang_thai", "nguoi_chiu_trach_nhiem", "ca_truc__vi_tri_chot__muc_tieu")
    search_fields = ("tieu_de", "ca_truc__nhan_vien__ho_ten")
    list_select_related = ('ca_truc__nhan_vien', 'ca_truc__vi_tri_chot__muc_tieu', 'nguoi_chiu_trach_nhiem')


@admin.register(BaoCaoDeXuat)
class BaoCaoDeXuatAdmin(admin.ModelAdmin):
    list_display = ("tieu_de", "nhan_vien", "loai_bao_cao", "ngay_gui", "da_doc")
    list_filter = ("loai_bao_cao", "da_doc")
    search_fields = ("tieu_de", "nhan_vien__ho_ten")
    readonly_fields = ("nhan_vien", "loai_bao_cao", "tieu_de", "noi_dung", "ngay_gui")