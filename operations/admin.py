# file: operations/admin.py

from django.contrib import admin, messages
from django.utils.html import format_html
from datetime import time
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

# --- Các lớp Resource để xuất Excel (Giữ nguyên) ---
class PhanCongCaTrucResource(resources.ModelResource):
    # ... (giữ nguyên)
    pass

class ChamCongResource(resources.ModelResource):
    # ... (giữ nguyên)
    pass


# --- CÁC LỚP ADMIN CHO TỪNG MODEL (ĐÃ NÂNG CẤP) ---

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
class PhanCongCaTrucAdmin(ImportExportModelAdmin):
    resource_class = PhanCongCaTrucResource
    list_display = ("ngay_truc", "get_muc_tieu", "vi_tri_chot", "nhan_vien", "ca_lam_viec")
    list_filter = ("ngay_truc", "vi_tri_chot__muc_tieu", "ca_lam_viec")
    search_fields = ("nhan_vien__ho_ten", "vi_tri_chot__ten_vi_tri", "nhan_vien__ma_nhan_vien")
    autocomplete_fields = ["nhan_vien", "vi_tri_chot", "ca_lam_viec"]
    list_select_related = ("vi_tri_chot__muc_tieu", "nhan_vien", "ca_lam_viec")

    @admin.display(description="Mục tiêu", ordering="vi_tri_chot__muc_tieu")
    def get_muc_tieu(self, obj):
        return obj.vi_tri_chot.muc_tieu.ten_muc_tieu


@admin.register(ChamCong)
class ChamCongAdmin(ImportExportModelAdmin):
    resource_class = ChamCongResource
    list_display = (
        "get_nhan_vien",
        "get_muc_tieu",
        "get_ngay_truc",
        "thoi_gian_check_in",
        "thoi_gian_check_out",
        "trang_thai_cham_cong",  # Cải tiến: Thêm cột trạng thái
        "xem_anh_check_in",
    )
    list_filter = ("ca_truc__ngay_truc", "ca_truc__vi_tri_chot__muc_tieu", "ca_truc__nhan_vien")
    search_fields = ("ca_truc__nhan_vien__ho_ten", "ca_truc__nhan_vien__ma_nhan_vien")
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'ca_truc__nhan_vien', 
            'ca_truc__vi_tri_chot__muc_tieu', 
            'ca_truc__ca_lam_viec'
        )

    @admin.display(description='Trạng thái')
    def trang_thai_cham_cong(self, obj):
        # Logic tính toán và hiển thị trạng thái chấm công
        if not obj.thoi_gian_check_in:
            return format_html('<span class="badge bg-secondary">Chưa chấm công</span>')
        
        di_tre = obj.thoi_gian_check_in.time() > obj.ca_truc.ca_lam_viec.gio_bat_dau
        ve_som = obj.thoi_gian_check_out and obj.thoi_gian_check_out.time() < obj.ca_truc.ca_lam_viec.gio_ket_thuc
        
        if di_tre:
            return format_html('<span class="badge bg-warning text-dark">Đi trễ</span>')
        if ve_som:
            return format_html('<span class="badge bg-info text-dark">Về sớm</span>')
        if obj.thoi_gian_check_in and obj.thoi_gian_check_out:
            return format_html('<span class="badge bg-success">Hoàn thành</span>')
        return format_html('<span class="badge bg-primary">Đã check-in</span>')

    # ... các hàm get_... và xem_anh_... khác giữ nguyên ...
    @admin.display(description='Nhân viên', ordering='ca_truc__nhan_vien__ho_ten')
    def get_nhan_vien(self, obj):
        return obj.ca_truc.nhan_vien

    @admin.display(description='Mục tiêu', ordering='ca_truc__vi_tri_chot__muc_tieu')
    def get_muc_tieu(self, obj):
        return obj.ca_truc.vi_tri_chot.muc_tieu
        
    @admin.display(description='Ngày trực', ordering='ca_truc__ngay_truc')
    def get_ngay_truc(self, obj):
        return obj.ca_truc.ngay_truc

    @admin.display(description='Ảnh Check-in')
    def xem_anh_check_in(self, obj):
        if obj.anh_check_in:
            return format_html('<a href="{0}" target="_blank"><img src="{0}" width="70" /></a>', obj.anh_check_in.url)
        return "Chưa có"

@admin.register(BaoCaoSuCo)
class BaoCaoSuCoAdmin(admin.ModelAdmin):
    list_display = (
        "tieu_de",
        "get_muc_tieu",  # Cải tiến: Hiển thị mục tiêu
        "get_nhan_vien_bao_cao",
        "trang_thai",
        "thoi_gian_bao_cao",
    )
    # Cải tiến: Thêm bộ lọc theo ngày và mục tiêu
    list_filter = ("trang_thai", "thoi_gian_bao_cao", "ca_truc__vi_tri_chot__muc_tieu")
    search_fields = ("tieu_de", "ca_truc__nhan_vien__ho_ten")
    list_select_related = ('ca_truc__nhan_vien', 'ca_truc__vi_tri_chot__muc_tieu', 'nguoi_chiu_trach_nhiem')
    actions = ['danh_dau_da_xem'] # Cải tiến: Thêm action

    @admin.display(description='Mục tiêu', ordering='ca_truc__vi_tri_chot__muc_tieu')
    def get_muc_tieu(self, obj):
        return obj.ca_truc.vi_tri_chot.muc_tieu

    @admin.display(description='Người báo cáo', ordering='ca_truc__nhan_vien')
    def get_nhan_vien_bao_cao(self, obj):
        return obj.ca_truc.nhan_vien

    @admin.action(description='Đánh dấu là "Đã xem"')
    def danh_dau_da_xem(self, request, queryset):
        updated_count = queryset.update(trang_thai='DAXEM')
        self.message_user(
            request,
            f'Đã cập nhật trạng thái cho {updated_count} báo cáo sự cố.',
            messages.SUCCESS
        )

@admin.register(BaoCaoDeXuat)
class BaoCaoDeXuatAdmin(admin.ModelAdmin):
    list_display = ("tieu_de", "nhan_vien", "loai_bao_cao", "ngay_gui", "da_doc")
    list_filter = ("loai_bao_cao", "da_doc")
    search_fields = ("tieu_de", "nhan_vien__ho_ten")
    readonly_fields = ("nhan_vien", "loai_bao_cao", "tieu_de", "noi_dung", "ngay_gui")
