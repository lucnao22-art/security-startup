from django.contrib import admin
from .models import TuyenTuanTra, DiemKiemTra, LuotTuanTra, KetQuaKiemTra


class DiemKiemTraInline(admin.TabularInline):
    model = DiemKiemTra
    extra = 1


@admin.register(TuyenTuanTra)
class TuyenTuanTraAdmin(admin.ModelAdmin):
    list_display = ("ten_tuyen", "muc_tieu", "is_active")
    list_filter = ("muc_tieu", "is_active")
    search_fields = ("ten_tuyen", "muc_tieu__ten_muc_tieu")
    inlines = [DiemKiemTraInline]


@admin.register(DiemKiemTra)
class DiemKiemTraAdmin(admin.ModelAdmin):
    list_display = ("ten_diem", "tuyen_tuan_tra", "thu_tu", "qr_code_id")
    list_filter = ("tuyen_tuan_tra__muc_tieu", "tuyen_tuan_tra")
    search_fields = ("ten_diem",)
    readonly_fields = ("qr_code_id",)


class KetQuaKiemTraInline(admin.TabularInline):
    model = KetQuaKiemTra
    extra = 0
    readonly_fields = (
        "diem_kiem_tra",
        "thoi_gian_quet",
        "trang_thai",
        "ghi_chu",
        "hinh_anh",
    )


@admin.register(LuotTuanTra)
class LuotTuanTraAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "nhan_vien",
        "tuyen_tuan_tra",
        "trang_thai",
        "thoi_gian_bat_dau",
        "thoi_gian_ket_thuc",
    )
    list_filter = ("trang_thai", "tuyen_tuan_tra__muc_tieu", "nhan_vien")
    search_fields = ("nhan_vien__ho_ten", "tuyen_tuan_tra__ten_tuyen")
    readonly_fields = ("thoi_gian_bat_dau", "thoi_gian_ket_thuc")
    inlines = [KetQuaKiemTraInline]
