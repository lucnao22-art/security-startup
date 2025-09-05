# file: inspection/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

# Sửa lại import cho đúng
from users.models import NhanVien, LichSuCongTac 
from .models import LoaiTuanTra, LuotTuanTra, DiemTuanTra, GhiNhanTuanTra

@login_required
def tuan_tra_mobile_view(request):
    try:
        nhan_vien = request.user.nhanvien
        
        # --- PHẦN SỬA LỖI VÀ NÂNG CẤP ---
        # 1. Tìm bản ghi công tác hiện tại của nhân viên
        lich_su_hien_tai = LichSuCongTac.objects.filter(
            nhan_vien=nhan_vien, 
            la_vi_tri_hien_tai=True
        ).select_related('muc_tieu').first()

        if not lich_su_hien_tai:
            messages.error(request, "Bạn chưa được phân công vào mục tiêu nào.")
            return render(request, "inspection/mobile/tuan_tra.html", {'error': True})

        # 2. Lấy mục tiêu từ lịch sử công tác
        muc_tieu_hien_tai = lich_su_hien_tai.muc_tieu
        
        # --- KẾT THÚC PHẦN SỬA LỖI ---

        cac_loai_tuan_tra = LoaiTuanTra.objects.filter(muc_tieu=muc_tieu_hien_tai)

    except NhanVien.DoesNotExist:
        messages.error(request, "Không tìm thấy thông tin nhân viên của bạn.")
        return render(request, "inspection/mobile/tuan_tra.html", {'error': True})

    context = {
        'muc_tieu': muc_tieu_hien_tai,
        'cac_loai_tuan_tra': cac_loai_tuan_tra
    }
    return render(request, "inspection/mobile/tuan_tra.html", context)


@login_required
def chi_tiet_luot_tuan_tra_view(request, luot_tuan_tra_id):
    luot_tuan_tra = get_object_or_404(LuotTuanTra, id=luot_tuan_tra_id)
    diem_da_quet = GhiNhanTuanTra.objects.filter(luot_tuan_tra=luot_tuan_tra).values_list('diem_tuan_tra_id', flat=True)
    
    context = {
        'luot_tuan_tra': luot_tuan_tra,
        'diem_da_quet': list(diem_da_quet)
    }
    return render(request, 'inspection/mobile/chi_tiet_luot_tuan_tra.html', context)