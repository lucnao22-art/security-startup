from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import NhanVien, PhongBan, ChucDanh, LichSuCongTac


@admin.register(ChucDanh)
class ChucDanhAdmin(admin.ModelAdmin):
    list_display = ("ten_chuc_danh", "link_den_nhom_quyen")

    def link_den_nhom_quyen(self, obj):
        if obj.nhom_quyen:
            url = reverse("admin:auth_group_change", args=[obj.nhom_quyen.id])
            return format_html('<a href="{}">Thiết lập Quyền</a>', url)
        return "Chưa gán"

    link_den_nhom_quyen.short_description = "Nhóm Quyền"


@admin.register(PhongBan)
class PhongBanAdmin(admin.ModelAdmin):
    list_display = ("ten_phong_ban", "link_den_nhom_quyen")

    def link_den_nhom_quyen(self, obj):
        if obj.nhom_quyen:
            url = reverse("admin:auth_group_change", args=[obj.nhom_quyen.id])
            return format_html('<a href="{}">Thiết lập Quyền chung</a>', url)
        return "Chưa gán"

    link_den_nhom_quyen.short_description = "Nhóm Quyền chung"


# Cho phép quản lý Lịch sử Công tác trực tiếp trên trang Nhân viên
class LichSuCongTacInline(admin.TabularInline):
    model = LichSuCongTac
    fk_name = "nhan_vien"
    extra = 1  # Hiển thị sẵn 1 dòng trống để thêm mới
    raw_id_fields = (
        "quan_ly_truc_tiep",
        "muc_tieu",
    )  # Giúp chọn quản lý và mục tiêu dễ hơn


@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    inlines = [LichSuCongTacInline]  # Thêm Lịch sử công tác vào đây
    list_display = ("ho_ten", "phong_ban", "chuc_danh")
    list_filter = ("phong_ban", "chuc_danh")
    search_fields = ("ho_ten", "ma_nhan_vien", "user__username")

    fieldsets = (
        ("Tài khoản & Phân quyền", {"fields": ("user", "phong_ban", "chuc_danh")}),
        (
            "Thông tin Cá nhân",
            {
                "fields": (
                    "ho_ten",
                    "ma_nhan_vien",
                    "anh_the",
                    "ngay_sinh",
                    "gioi_tinh",
                    "so_cccd",
                    "sdt_chinh",
                    "email",
                )
            },
        ),
        # Đã xóa fieldset "Thông tin công việc" vì các trường đã chuyển đi
    )

    # Chỉ còn 'user' là cần dùng raw_id_fields
    raw_id_fields = ("user",)
