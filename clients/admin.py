from django.contrib import admin
from .models import KhachHangTiemNang, CoHoiKinhDoanh, HopDong, MucTieu


@admin.register(KhachHangTiemNang)
class KhachHangTiemNangAdmin(admin.ModelAdmin):
    list_display = ("ten_cong_ty", "nguoi_lien_he", "email", "sdt")
    search_fields = ("ten_cong_ty", "nguoi_lien_he")


@admin.register(CoHoiKinhDoanh)
class CoHoiKinhDoanhAdmin(admin.ModelAdmin):
    list_display = (
        "ten_co_hoi",
        "khach_hang_tiem_nang",
        "gia_tri_uoc_tinh",
        "trang_thai",
        "nguoi_phu_trach",
    )
    list_filter = ("trang_thai", "nguoi_phu_trach")
    search_fields = ("ten_co_hoi", "khach_hang_tiem_nang__ten_cong_ty")
    raw_id_fields = ("khach_hang_tiem_nang", "nguoi_phu_trach")


@admin.register(HopDong)
class HopDongAdmin(admin.ModelAdmin):
    list_display = ("so_hop_dong", "co_hoi", "ngay_ky", "ngay_het_han", "gia_tri")
    search_fields = ("so_hop_dong", "co_hoi__ten_co_hoi")
    raw_id_fields = ("co_hoi",)


@admin.register(MucTieu)
class MucTieuAdmin(admin.ModelAdmin):
    list_display = ("ten_muc_tieu", "hop_dong", "quan_ly_muc_tieu")
    search_fields = ("ten_muc_tieu", "hop_dong__so_hop_dong")
    raw_id_fields = ("hop_dong", "quan_ly_muc_tieu")
