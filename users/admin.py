# file: users/admin.py

from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from .models import NhanVien, PhongBan, CauHinhMaNhanVien, ChungChi, LichSuCongTac
from inventory.models import TrangBiTieuChuan, CapPhatCaNhan
import qrcode
import io
import base64

class ChungChiInline(admin.TabularInline):
    model = ChungChi
    extra = 1

class CapPhatCaNhanInline(admin.TabularInline):
    model = CapPhatCaNhan
    extra = 0
    autocomplete_fields = ['vat_tu']

class LichSuCongTacInline(admin.TabularInline):
    model = LichSuCongTac
    extra = 1
    autocomplete_fields = ['muc_tieu']

@admin.register(CauHinhMaNhanVien)
class CauHinhMaNhanVienAdmin(admin.ModelAdmin):
    list_display = ('tien_to', 'do_dai_so', 'so_hien_tai')
    def has_add_permission(self, request):
        return CauHinhMaNhanVien.objects.count() == 0

@admin.register(PhongBan)
class PhongBanAdmin(admin.ModelAdmin):
    list_display = ('ten_phong_ban', 'mo_ta')
    search_fields = ('ten_phong_ban',)

@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    # Kích hoạt lại template tùy chỉnh
    change_form_template = 'admin/users/nhanvien/change_form.html'
    
    inlines = [ChungChiInline, CapPhatCaNhanInline, LichSuCongTacInline]
    search_fields = ('ho_ten', 'ma_nhan_vien')
    list_display = ('ma_nhan_vien', 'ho_ten', 'phong_ban', 'chuc_vu', 'sdt_chinh')
    list_filter = ('phong_ban', 'chuc_vu', 'trang_thai_lam_viec')
    
    actions = ['cap_phat_tieu_chuan']
    def cap_phat_tieu_chuan(self, request, queryset):
        # ... logic giữ nguyên ...
        pass

    # Cấu hình các tab cho Jazzmin
    jazzmin_form_tabs = [
        ('thong_tin_chung', 'Thông tin Chung'),
        ('bang_cap', 'Bằng cấp & Chứng chỉ'),
        ('lich_su_cong_tac', 'Lịch sử Công tác'),
        ('trang_bi', 'Trang bị Cấp phát'),
    ]

    # Hàm change_view để tạo mã QR và truyền ra template
    def change_view(self, request, object_id, form_url='', extra_context=None):
        nhan_vien = self.get_object(request, object_id)
        
        qr_image_base64 = None
        if nhan_vien and nhan_vien.ma_nhan_vien:
            qr_data = f"ID: {nhan_vien.ma_nhan_vien}\nName: {nhan_vien.ho_ten}\nPosition: {nhan_vien.get_chuc_vu_display()}"
            img = qrcode.make(qr_data)
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            qr_image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        extra_context = extra_context or {}
        extra_context['qr_image'] = qr_image_base64
        
        return super().change_view(request, object_id, form_url, extra_context=extra_context)