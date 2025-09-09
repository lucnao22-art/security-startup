# file: inspection/admin.py

from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect
import qrcode
from io import BytesIO
import base64

from .models import (
    LoaiTuanTra, DiemTuanTra, LuotTuanTra, GhiNhanTuanTra,
    HangMucKiemTra, BienBanThanhTra, KetQuaKiemTra, BuoiHuanLuyen
)


# ==============================================================================
# PHẦN 1: GIAO DIỆN QUẢN LÝ NGHIỆP VỤ TUẦN TRA (Giữ nguyên)
# ==============================================================================
class DiemTuanTraInline(admin.TabularInline):
    model = DiemTuanTra
    extra = 1
    fields = ('ten_diem', 'ma_qr', 'vi_tri_cu_the', 'thu_tu')
    ordering = ('thu_tu',)

class GhiNhanTuanTraInline(admin.TabularInline):
    model = GhiNhanTuanTra
    extra = 0
    can_delete = False
    fields = ('diem_tuan_tra', 'thoi_gian_quet', 'ghi_chu')
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(LoaiTuanTra)
class LoaiTuanTraAdmin(admin.ModelAdmin):
    list_display = ('ten_loai', 'muc_tieu', 'so_diem_tuan_tra')
    list_filter = ('muc_tieu',)
    search_fields = ('ten_loai',)
    inlines = [DiemTuanTraInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(diem_count=Count('cac_diem_tuan_tra'))

    @admin.display(description='Số điểm', ordering='diem_count')
    def so_diem_tuan_tra(self, obj):
        return obj.diem_count

@admin.register(DiemTuanTra)
class DiemTuanTraAdmin(admin.ModelAdmin):
    list_display = ('ten_diem', 'loai_tuan_tra', 'thu_tu', 'hien_thi_ma_qr')
    list_filter = ('loai_tuan_tra__muc_tieu', 'loai_tuan_tra')
    search_fields = ('ten_diem', 'ma_qr')
    list_select_related = ('loai_tuan_tra__muc_tieu',)

    @admin.display(description='Mã QR')
    def hien_thi_ma_qr(self, obj):
        qr = qrcode.QRCode(version=1, box_size=5, border=2)
        qr.add_data(obj.ma_qr)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return format_html(
            '<img src="data:image/png;base64,{}" title="{}" style="cursor:pointer;" onclick="navigator.clipboard.writeText(\'{}\')"/>',
            img_str,
            f"Click để copy mã: {obj.ma_qr}",
            obj.ma_qr
        )

@admin.register(LuotTuanTra)
class LuotTuanTraAdmin(admin.ModelAdmin):
    inlines = [GhiNhanTuanTraInline]
    list_display = ('__str__', 'get_nhan_vien', 'get_muc_tieu', 'trang_thai', 'ket_qua_tuan_tra')
    list_filter = ('trang_thai', 'ca_truc__vi_tri_chot__muc_tieu', 'thoi_gian_bat_dau')
    search_fields = ('loai_tuan_tra__ten_loai', 'ca_truc__nhan_vien__ho_ten')
    list_select_related = ('ca_truc__nhan_vien', 'ca_truc__vi_tri_chot__muc_tieu', 'loai_tuan_tra')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(so_diem_da_quet=Count('cac_ghi_nhan'))

    @admin.display(description='Kết quả', ordering='so_diem_da_quet')
    def ket_qua_tuan_tra(self, obj):
        if not obj.loai_tuan_tra: return "N/A"
        tong_so_diem = obj.loai_tuan_tra.cac_diem_tuan_tra.count()
        so_diem_da_quet = obj.so_diem_da_quet
        if so_diem_da_quet < tong_so_diem:
             return format_html('<b style="color: orange;">{}/{} điểm</b>', so_diem_da_quet, tong_so_diem)
        return format_html('<b style="color: green;">{}/{} điểm</b>', so_diem_da_quet, tong_so_diem)

    @admin.display(description='Nhân viên', ordering='ca_truc__nhan_vien')
    def get_nhan_vien(self, obj):
        return obj.ca_truc.nhan_vien if obj.ca_truc else "Không xác định"

    @admin.display(description='Mục tiêu', ordering='ca_truc__vi_tri_chot__muc_tieu')
    def get_muc_tieu(self, obj):
        return obj.ca_truc.vi_tri_chot.muc_tieu if obj.ca_truc else "Không xác định"

@admin.register(GhiNhanTuanTra)
class GhiNhanTuanTraAdmin(admin.ModelAdmin):
    list_display = ('diem_tuan_tra', 'luot_tuan_tra', 'thoi_gian_quet')
    list_filter = ('luot_tuan_tra__ca_truc__vi_tri_chot__muc_tieu',)
    search_fields = ('diem_tuan_tra__ten_diem',)


# ==============================================================================
# PHẦN 2: GIAO DIỆN QUẢN LÝ NGHIỆP VỤ THANH TRA (ĐÃ NÂNG CẤP)
# ==============================================================================

@admin.register(HangMucKiemTra)
class HangMucKiemTraAdmin(admin.ModelAdmin):
    list_display = ('noi_dung', 'nhom_kiem_tra', 'is_active')
    list_filter = ('nhom_kiem_tra', 'is_active')
    search_fields = ('noi_dung',)

class KetQuaKiemTraInline(admin.TabularInline):
    model = KetQuaKiemTra
    extra = 0
    fields = ('hang_muc', 'ket_qua', 'ghi_chu')
    readonly_fields = ('hang_muc',)
    
    def has_add_permission(self, request, obj):
        return False

@admin.register(BienBanThanhTra)
class BienBanThanhTraAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'loai_thanh_tra', 'thanh_tra_vien', 'nhan_vien_duoc_kiem_tra', 'muc_tieu')
    list_filter = ('loai_thanh_tra', 'thanh_tra_vien', 'muc_tieu')
    search_fields = ('muc_tieu__ten_muc_tieu', 'nhan_vien_duoc_kiem_tra__ho_ten')
    autocomplete_fields = ['thanh_tra_vien', 'nhan_vien_duoc_kiem_tra', 'muc_tieu']
    inlines = [KetQuaKiemTraInline]
    
    # Cải tiến: Tùy biến giao diện form thêm mới và chỉnh sửa
    def get_fieldsets(self, request, obj=None):
        if obj is None: # Đây là trang "Thêm mới"
            return (
                ('Thông tin chung', {
                    'fields': ('loai_thanh_tra', 'thanh_tra_vien', 'muc_tieu', 'nhan_vien_duoc_kiem_tra', 'thoi_gian_kiem_tra')
                }),
                ('QUAN TRỌNG: Quy trình tạo Checklist', {
                    'description': '''
                        <div class="alert alert-info">
                            <strong>Bước 1:</strong> Điền các thông tin chung ở trên.<br>
                            <strong>Bước 2:</strong> Nhấn nút <strong>"Lưu"</strong> hoặc <strong>"Lưu và tiếp tục sửa"</strong>.<br>
                            <strong>Bước 3:</strong> Hệ thống sẽ tự động tạo checklist chi tiết bên dưới để bạn điền kết quả.
                        </div>
                    ''',
                    'fields': (),
                }),
            )
        return ( # Đây là trang "Chỉnh sửa"
            ('Thông tin chung', {
                'fields': ('loai_thanh_tra', 'thanh_tra_vien', 'muc_tieu', 'nhan_vien_duoc_kiem_tra', 'thoi_gian_kiem_tra')
            }),
            ('Đánh giá chung & Biện pháp khắc phục', {
                'fields': ('danh_gia_chung',)
            }),
            # Thêm một fieldset trống chỉ để hiển thị inline dưới đây
            ('Kết quả Thanh tra Chi tiết', {
                'fields': (),
            }),
        )

    # Cải tiến: Ẩn bảng checklist rỗng khi tạo mới
    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        return self.inlines

    # Cải tiến: Tự động tạo checklist và luôn chuyển hướng về trang sửa
    def response_add(self, request, obj, post_url_continue=None):
        if 'NV_' in obj.loai_thanh_tra:
            nhom_can_loc = ['NV_TAC_PHONG', 'NV_NGHIEP_VU']
        elif 'MT_' in obj.loai_thanh_tra:
            nhom_can_loc = ['MT_NHAN_SU', 'MT_CONG_CU', 'MT_AN_NINH']
        else:
            nhom_can_loc = []
        
        hang_muc_list = HangMucKiemTra.objects.filter(
            nhom_kiem_tra__in=nhom_can_loc,
            is_active=True
        )

        for hang_muc in hang_muc_list:
            KetQuaKiemTra.objects.get_or_create(
                bien_ban=obj,
                hang_muc=hang_muc,
                defaults={'ket_qua': 'DAT'}
            )
        
        if hang_muc_list.exists():
            self.message_user(request, "Đã tạo biên bản. Checklist chi tiết đã được tạo, vui lòng điền kết quả.", messages.SUCCESS)
        else:
            self.message_user(request, "Không tìm thấy hạng mục nào phù hợp. Vui lòng vào mục 'Hạng mục Thanh tra' để tạo các tiêu chí kiểm tra trước.", messages.WARNING)

        # Luôn chuyển hướng người dùng trở lại trang chỉnh sửa
        return HttpResponseRedirect(reverse('admin:inspection_bienbanthanhtra_change', args=[obj.pk]))

# ==============================================================================
# PHẦN 3: GIAO DIỆN QUẢN LÝ NGHIỆP VỤ ĐÀO TẠO
# ==============================================================================

@admin.register(BuoiHuanLuyen)
class BuoiHuanLuyenAdmin(admin.ModelAdmin):
    list_display = ('ten_buoi_huan_luyen', 'ngay_to_chuc', 'giang_vien')
    list_filter = ('ngay_to_chuc', 'giang_vien')
    search_fields = ('ten_buoi_huan_luyen', 'noi_dung')
    autocomplete_fields = ['giang_vien']
    filter_horizontal = ('nhan_vien_tham_gia',)

