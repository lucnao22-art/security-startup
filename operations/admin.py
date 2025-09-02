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


# Lớp tùy chỉnh để xuất file Excel chuyên nghiệp
class PhanCongCaTrucResource(resources.ModelResource):
    nhan_vien = resources.Field(
        attribute="nhan_vien",
        column_name="Nhân viên",
        widget=resources.widgets.ForeignKeyWidget(NhanVien, "ho_ten"),
    )
    muc_tieu = resources.Field(
        attribute="vi_tri_chot__muc_tieu",
        column_name="Mục tiêu",
        widget=resources.widgets.ForeignKeyWidget(MucTieu, "ten_muc_tieu"),
    )
    vi_tri_chot = resources.Field(
        attribute="vi_tri_chot",
        column_name="Vị trí chốt",
        widget=resources.widgets.ForeignKeyWidget(ViTriChot, "ten_vi_tri"),
    )
    ca_lam_viec = resources.Field(
        attribute="ca_lam_viec",
        column_name="Ca làm việc",
        widget=resources.widgets.ForeignKeyWidget(CaLamViec, "ten_ca"),
    )
    ngay_truc = resources.Field(attribute="ngay_truc", column_name="Ngày trực")

    class Meta:
        model = PhanCongCaTruc
        fields = (
            "id",
            "ngay_truc",
            "nhan_vien",
            "muc_tieu",
            "vi_tri_chot",
            "ca_lam_viec",
        )
        export_order = (
            "id",
            "ngay_truc",
            "nhan_vien",
            "muc_tieu",
            "vi_tri_chot",
            "ca_lam_viec",
        )


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
class PhanCongCaTrucAdmin(admin.ModelAdmin):
    list_display = (
        "ngay_truc",
        "get_muc_tieu", # Hàm để lấy tên mục tiêu
        "vi_tri_chot",
        "nhan_vien",
        "ca_lam_viec",
    )
    list_filter = ("ngay_truc", "vi_tri_chot__muc_tieu", "ca_lam_viec")
    search_fields = ("nhan_vien__ho_ten", "vi_tri_chot__ten_vi_tri")
    autocomplete_fields = ["nhan_vien", "vi_tri_chot", "ca_lam_viec"]

    # --- DÒNG CẢI TIẾN QUAN TRỌNG NHẤT ---
    # Chỉ thị cho Django sử dụng JOIN để lấy các dữ liệu liên quan trong một lần truy vấn
    list_select_related = ("vi_tri_chot__muc_tieu", "nhan_vien", "ca_lam_viec")

    def get_muc_tieu(self, obj):
        return obj.vi_tri_chot.muc_tieu.ten_muc_tieu

    get_muc_tieu.short_description = "Mục tiêu"
    get_muc_tieu.admin_order_field = "vi_tri_chot__muc_tieu"

# ----- THÊM LỚP NÀY VÀO -----
class ChamCongResource(resources.ModelResource):
    nhan_vien = resources.Field(attribute="ca_truc__nhan_vien", column_name="Nhân viên")
    muc_tieu = resources.Field(
        attribute="ca_truc__vi_tri_chot__muc_tieu", column_name="Mục tiêu"
    )
    vi_tri_chot = resources.Field(
        attribute="ca_truc__vi_tri_chot", column_name="Vị trí chốt"
    )
    ca_lam_viec = resources.Field(
        attribute="ca_truc__ca_lam_viec", column_name="Ca làm việc"
    )
    ngay_truc = resources.Field(attribute="ca_truc__ngay_truc", column_name="Ngày trực")

    class Meta:
        model = ChamCong
        fields = (
            "id",
            "ngay_truc",
            "nhan_vien",
            "muc_tieu",
            "vi_tri_chot",
            "ca_lam_viec",
            "thoi_gian_check_in",
            "thoi_gian_check_out",
        )
        export_order = fields


@admin.register(ChamCong)
class ChamCongAdmin(ImportExportModelAdmin):
    resource_class = ChamCongResource
    list_display = (
        "ca_truc",
        "thoi_gian_check_in",
        "xem_anh_check_in",
        "thoi_gian_check_out",
        "xem_anh_check_out",
    )
    list_filter = ("ca_truc__ngay_truc", "ca_truc__vi_tri_chot__muc_tieu")
    search_fields = ("ca_truc__nhan_vien__ho_ten",)
    readonly_fields = ("xem_anh_check_in", "xem_anh_check_out")

    def xem_anh_check_in(self, obj):
        if obj.anh_check_in:
            return format_html(
                f'<a href="{obj.anh_check_in.url}" target="_blank"><img src="{obj.anh_check_in.url}" width="100" /></a>'
            )
        return "Chưa có ảnh"

    xem_anh_check_in.short_description = "Ảnh Check-in"

    def xem_anh_check_out(self, obj):
        if obj.anh_check_out:
            return format_html(
                f'<a href="{obj.anh_check_out.url}" target="_blank"><img src="{obj.anh_check_out.url}" width="100" /></a>'
            )
        return "Chưa có ảnh"

    xem_anh_check_out.short_description = "Ảnh Check-out"


@admin.register(BaoCaoSuCo)
class BaoCaoSuCoAdmin(admin.ModelAdmin):
    list_display = (
        "tieu_de",
        "ca_truc",
        "trang_thai",
        "nguoi_chiu_trach_nhiem",
        "thoi_gian_bao_cao",
    )
    list_filter = ("trang_thai", "nguoi_chiu_trach_nhiem")
    search_fields = ("tieu_de", "ca_truc__nhan_vien__ho_ten")
    readonly_fields = ("xem_hinh_anh", "ca_truc", "thoi_gian_bao_cao")

    fieldsets = (
        (
            "Thông tin Sự cố",
            {"fields": ("tieu_de", "noi_dung", "xem_hinh_anh", "ca_truc")},
        ),
        (
            "Luồng Xử lý",
            {"fields": ("trang_thai", "nguoi_chiu_trach_nhiem", "lich_su_xu_ly")},
        ),
    )

    def xem_hinh_anh(self, obj):
        if obj.hinh_anh:
            return format_html(
                f'<a href="{obj.hinh_anh.url}" target="_blank"><img src="{obj.hinh_anh.url}" width="100" /></a>'
            )
        return "Không có ảnh"

    xem_hinh_anh.short_description = "Hình ảnh"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            nhan_vien = request.user.nhanvien
            return qs.filter(nguoi_chiu_trach_nhiem=nhan_vien)
        except Exception as e:
            return qs.none()


@admin.register(BaoCaoDeXuat)
class BaoCaoDeXuatAdmin(admin.ModelAdmin):
    list_display = ("tieu_de", "nhan_vien", "loai_bao_cao", "ngay_gui", "da_doc")
    list_filter = ("loai_bao_cao", "da_doc")
    search_fields = ("tieu_de", "nhan_vien__ho_ten")
    readonly_fields = ("nhan_vien", "loai_bao_cao", "tieu_de", "noi_dung", "ngay_gui")
