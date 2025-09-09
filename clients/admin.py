from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count

from .models import KhachHangTiemNang, CoHoiKinhDoanh, HopDong, MucTieu

# --- Inline ModelAdmins ---
# Inline này cho phép xem và thêm Mục tiêu ngay trên trang Hợp đồng
class MucTieuInline(admin.TabularInline):
    model = MucTieu
    extra = 1
    fields = ('ten_muc_tieu', 'dia_chi', 'quan_ly_muc_tieu')
    verbose_name = "Mục tiêu triển khai"
    verbose_name_plural = "Các mục tiêu triển khai theo Hợp đồng"
    show_change_link = True
    autocomplete_fields = ['quan_ly_muc_tieu']

# --- Main ModelAdmins ---

@admin.register(KhachHangTiemNang)
class KhachHangTiemNangAdmin(admin.ModelAdmin):
    list_display = ("ten_cong_ty", "nguoi_lien_he", "email", "sdt", "nguon")
    search_fields = ("ten_cong_ty", "nguoi_lien_he", "email")
    list_filter = ("nguon",)

@admin.register(CoHoiKinhDoanh)
class CoHoiKinhDoanhAdmin(admin.ModelAdmin):
    list_display = (
        "ten_co_hoi",
        "get_khach_hang_link", # Cải tiến: Hiển thị link
        "gia_tri_uoc_tinh",
        "trang_thai",
        "nguoi_phu_trach",
        "link_to_hop_dong", # Cải tiến: Hiển thị link tới hợp đồng
    )
    list_filter = ("trang_thai", "nguoi_phu_trach")
    search_fields = ("ten_co_hoi", "khach_hang_tiem_nang__ten_cong_ty")
    raw_id_fields = ("khach_hang_tiem_nang", "nguoi_phu_trach")
    
    @admin.display(description="Khách hàng", ordering='khach_hang_tiem_nang__ten_cong_ty')
    def get_khach_hang_link(self, obj):
        if obj.khach_hang_tiem_nang:
            url = reverse("admin:clients_khachhangtiemnang_change", args=[obj.khach_hang_tiem_nang.id])
            return format_html('<a href="{}">{}</a>', url, obj.khach_hang_tiem_nang.ten_cong_ty)
        return "N/A"

    @admin.display(description="Hợp đồng")
    def link_to_hop_dong(self, obj):
        # Kiểm tra xem cơ hội này đã có hợp đồng liên kết chưa
        if hasattr(obj, 'hopdong') and obj.hopdong:
            url = reverse("admin:clients_hopdong_change", args=[obj.hopdong.id])
            return format_html('<a href="{}" class="button">Xem HĐ {}</a>', url, obj.hopdong.so_hop_dong)
        # Nếu chưa, hiển thị nút để tạo mới
        else:
            url = reverse("admin:clients_hopdong_add") + f"?co_hoi={obj.id}"
            return format_html('<a href="{}" class="button">Tạo Hợp đồng</a>', url)

@admin.register(HopDong)
class HopDongAdmin(admin.ModelAdmin):
    inlines = [MucTieuInline] # Cải tiến: Thêm inline Mục tiêu
    list_display = (
        "so_hop_dong",
        "get_khach_hang", # Cải tiến: Hiển thị tên khách hàng
        "gia_tri",
        "ngay_ky",
        "ngay_het_han",
        "so_luong_muc_tieu", # Cải tiến: Hiển thị số mục tiêu
    )
    search_fields = ("so_hop_dong", "co_hoi__khach_hang_tiem_nang__ten_cong_ty")
    list_filter = ('ngay_ky', 'ngay_het_han')
    autocomplete_fields = ("co_hoi",)

    def get_queryset(self, request):
        # Tối ưu hóa truy vấn CSDL
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(muc_tieu_count=Count('muc_tieu'))
        return queryset

    @admin.display(description="Khách hàng", ordering='co_hoi__khach_hang_tiem_nang__ten_cong_ty')
    def get_khach_hang(self, obj):
        if obj.co_hoi and obj.co_hoi.khach_hang_tiem_nang:
            return obj.co_hoi.khach_hang_tiem_nang.ten_cong_ty
        return "Không xác định"

    @admin.display(description="Số Mục tiêu", ordering='muc_tieu_count')
    def so_luong_muc_tieu(self, obj):
        return obj.muc_tieu_count

@admin.register(MucTieu)
class MucTieuAdmin(admin.ModelAdmin):
    list_display = (
        "ten_muc_tieu",
        "get_hop_dong_link", # Cải tiến: Hiển thị link hợp đồng
        "get_khach_hang", # Cải tiến: Hiển thị khách hàng
        "quan_ly_muc_tieu",
    )
    search_fields = ("ten_muc_tieu", "hop_dong__so_hop_dong", "hop_dong__co_hoi__khach_hang_tiem_nang__ten_cong_ty")
    list_filter = ('hop_dong__co_hoi__khach_hang_tiem_nang',)
    autocomplete_fields = ("hop_dong", "quan_ly_muc_tieu")

    @admin.display(description="Hợp đồng", ordering='hop_dong__so_hop_dong')
    def get_hop_dong_link(self, obj):
        if obj.hop_dong:
            url = reverse("admin:clients_hopdong_change", args=[obj.hop_dong.id])
            return format_html('<a href="{}">{}</a>', url, obj.hop_dong.so_hop_dong)
        return "N/A"

    @admin.display(description="Khách hàng", ordering='hop_dong__co_hoi__khach_hang_tiem_nang__ten_cong_ty')
    def get_khach_hang(self, obj):
        if obj.hop_dong and obj.hop_dong.co_hoi and obj.hop_dong.co_hoi.khach_hang_tiem_nang:
            return obj.hop_dong.co_hoi.khach_hang_tiem_nang.ten_cong_ty
        return "Không xác định"
