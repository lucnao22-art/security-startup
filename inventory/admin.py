# file: inventory/admin.py

from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse

# Import các model cần thiết
from .models import (
    LoaiVatTu, NhaCungCap, VatTu, PhieuNhap, PhieuXuat, 
    PhieuCapPhat, ChiTietCapPhat, ChiTietPhieuXuat
)

@admin.register(LoaiVatTu)
class LoaiVatTuAdmin(admin.ModelAdmin):
    list_display = ('ten_loai',)
    search_fields = ('ten_loai',)

@admin.register(NhaCungCap)
class NhaCungCapAdmin(admin.ModelAdmin):
    list_display = ('ten_nha_cung_cap', 'so_dien_thoai', 'email')
    search_fields = ('ten_nha_cung_cap',)

# --- GIAO DIỆN QUẢN LÝ VẬT TƯ (ĐÃ NÂNG CẤP TOÀN DIỆN) ---

@admin.register(VatTu)
class VatTuAdmin(admin.ModelAdmin):
    # 1. CẢI TIẾN HIỂN THỊ: Thêm các cột hữu ích và cột "Tình trạng" tùy chỉnh
    list_display = (
        'ten_vat_tu', 
        'ma_vat_tu', 
        'loai', 
        'so_luong_ton_kho', 
        'dinh_muc_toi_thieu',
        'tinh_trang_ton_kho', # Cột mới được tạo từ phương thức bên dưới
        'don_vi_tinh'
    )
    # 2. CẢI TIẾN BỘ LỌC: Thêm bộ lọc theo tình trạng và nhà cung cấp
    list_filter = ('loai', 'trang_thai', 'nha_cung_cap')
    search_fields = ('ten_vat_tu', 'ma_vat_tu')
    
    # 3. CẢI TIẾN HÀNH ĐỘNG: Thêm action để cập nhật hàng loạt
    actions = ['danh_dau_can_nhap_hang']

    @admin.display(description='Số lượng tồn', ordering='so_luong_ton')
    def so_luong_ton_kho(self, obj):
        # Định dạng màu sắc dựa trên số lượng tồn
        if obj.so_luong_ton <= 0:
            color = "red"
        elif obj.so_luong_ton < obj.dinh_muc_toi_thieu:
            color = "orange"
        else:
            color = "green"
        return format_html(f'<b style="color: {color};">{obj.so_luong_ton}</b>')

    @admin.display(description='Tình trạng', ordering='trang_thai')
    def tinh_trang_ton_kho(self, obj):
        # Hiển thị trạng thái bằng tag màu sắc
        if obj.so_luong_ton <= 0:
            obj.trang_thai = 'HET_HANG'
            obj.save(update_fields=['trang_thai'])
            return format_html('<span style="color: white; background-color: red; padding: 3px 8px; border-radius: 5px;">Hết hàng</span>')
        elif obj.so_luong_ton < obj.dinh_muc_toi_thieu:
            obj.trang_thai = 'YEU_CAU_NHAP'
            obj.save(update_fields=['trang_thai'])
            return format_html('<span style="color: black; background-color: orange; padding: 3px 8px; border-radius: 5px;">Cần nhập</span>')
        else:
            obj.trang_thai = 'SAN_SANG'
            obj.save(update_fields=['trang_thai'])
            return format_html('<span style="color: white; background-color: green; padding: 3px 8px; border-radius: 5px;">An toàn</span>')

    @admin.action(description='Đánh dấu "Yêu cầu nhập" cho các vật tư đã chọn')
    def danh_dau_can_nhap_hang(self, request, queryset):
        updated_count = queryset.update(trang_thai='YEU_CAU_NHAP')
        self.message_user(
            request,
            f'Đã cập nhật thành công {updated_count} vật tư sang trạng thái "Yêu cầu nhập".',
            messages.SUCCESS
        )

# --- CÁC PHẦN CÒN LẠI GIỮ NGUYÊN ---

# (Các lớp PhieuCapPhatAdmin, PhieuXuatAdmin, PhieuNhapAdmin... giữ nguyên như cũ)
# --- GIAO DIỆN MỚI CHO CHỨC NĂNG CẤP PHÁT (Sử dụng PhieuCapPhat) ---
class ChiTietCapPhatInline(admin.TabularInline):
    model = ChiTietCapPhat
    extra = 1
    autocomplete_fields = ['vat_tu']

@admin.register(PhieuCapPhat)
class PhieuCapPhatAdmin(admin.ModelAdmin):
    inlines = [ChiTietCapPhatInline]
    list_display = ('so_phieu', 'nguoi_nhan', 'nguoi_cap_phat', 'ngay_cap_phat', 'in_phieu')
    list_filter = ('ngay_cap_phat', 'nguoi_nhan')
    search_fields = ('so_phieu', 'nguoi_nhan__ho_ten')
    autocomplete_fields = ['nguoi_nhan']
    readonly_fields = ('so_phieu',)

    def save_model(self, request, obj, form, change):
        if not obj.pk: # Khi tạo mới
            obj.nguoi_cap_phat = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            # Logic trừ kho sẽ được xử lý bằng signals
            instance.save()
        formset.save_m2m()

    @admin.display(description='In Phiếu')
    def in_phieu(self, obj):
        url = reverse('inventory:in_phieu_cap_phat', args=[obj.id])
        return format_html(f'<a href="{url}" class="button" target="_blank">In Phiếu</a>')

# Đăng ký các model còn lại
@admin.register(PhieuNhap)
class PhieuNhapAdmin(admin.ModelAdmin):
    list_display = ('vat_tu', 'so_luong', 'nguoi_nhap', 'ngay_nhap')
    autocomplete_fields = ['vat_tu', 'nguoi_nhap']

class ChiTietPhieuXuatInline(admin.TabularInline):
    model = ChiTietPhieuXuat
    extra = 1
    autocomplete_fields = ['vat_tu']
    verbose_name = "Vật tư xuất kho"
    verbose_name_plural = "Chi tiết các vật tư xuất kho"

@admin.register(PhieuXuat)
class PhieuXuatAdmin(admin.ModelAdmin):
    inlines = [ChiTietPhieuXuatInline]
    list_display = ('so_phieu', 'muc_tieu', 'nguoi_xuat', 'ngay_xuat', 'in_phieu')
    list_filter = ('ngay_xuat', 'muc_tieu')
    search_fields = ('so_phieu', 'muc_tieu__ten_muc_tieu')
    autocomplete_fields = ['muc_tieu']
    readonly_fields = ('so_phieu', 'nguoi_xuat')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.nguoi_xuat = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if instance.so_luong > instance.vat_tu.so_luong_ton:
                raise ValidationError(f"Số lượng tồn kho của '{instance.vat_tu.ten_vat_tu}' không đủ (chỉ còn {instance.vat_tu.so_luong_ton}).")
            instance.save()
        formset.save_m2m()

    @admin.display(description='In Phiếu')
    def in_phieu(self, obj):
        url = reverse('inventory:in_phieu_xuat', args=[obj.id])
        return format_html(f'<a href="{url}" class="button" target="_blank">In Phiếu</a>')