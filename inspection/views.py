# file: inspection/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

# Giữ nguyên các import từ file của bạn
from users.models import NhanVien, LichSuCongTac
from clients.models import MucTieu
from operations.models import PhanCongCaTruc
from .models import LoaiTuanTra, LuotTuanTra, DiemTuanTra, GhiNhanTuanTra

@login_required
def tuan_tra_mobile_view(request):
    """
    Hiển thị giao diện tuần tra, đã tối ưu lại logic tìm kiếm ca trực.
    """
    try:
        # Sửa lỗi truy cập thông tin nhân viên
        nhan_vien = request.user.nhan_vien
    except NhanVien.DoesNotExist:
        messages.error(request, "Tài khoản của bạn chưa được liên kết với hồ sơ nhân viên.")
        return redirect('operations:mobile_dashboard')

    ca_truc_hien_tai = None
    lo_trinh = None

    # === PHẦN SỬA LỖI VÀ NÂNG CẤP LOGIC ===
    # Tìm ca trực đang hoạt động dựa trên trạng thái Check-in thực tế.
    # Logic này đồng bộ với trang Dashboard, giải quyết được vấn đề bạn gặp phải.
    now = timezone.now()
    phan_congs_hom_nay = PhanCongCaTruc.objects.filter(
        nhan_vien=nhan_vien,
        ngay_truc=now.date()
    ).select_related(
        'chamcong', 
        'vi_tri_chot__muc_tieu'
    ).order_by('-ca_lam_viec__gio_bat_dau') # Sắp xếp để ưu tiên ca muộn hơn

    for pc in phan_congs_hom_nay:
        # Kiểm tra xem ca này đã được check-in và chưa check-out hay không
        if hasattr(pc, 'chamcong') and pc.chamcong.thoi_gian_check_in and not pc.chamcong.thoi_gian_check_out:
            ca_truc_hien_tai = pc
            break # Tìm thấy ca đang hoạt động, thoát khỏi vòng lặp

    if not ca_truc_hien_tai:
        messages.error(request, "Bạn không có ca trực nào đang diễn ra để thực hiện tuần tra.")
        return redirect('operations:mobile_dashboard')

    # Từ ca trực, lấy ra mục tiêu và lộ trình tuần tra
    muc_tieu_hien_tai = ca_truc_hien_tai.vi_tri_chot.muc_tieu
    lo_trinh = LoaiTuanTra.objects.filter(muc_tieu=muc_tieu_hien_tai).first()

    if not lo_trinh:
        messages.warning(request, "Mục tiêu của bạn hiện chưa được thiết lập lộ trình tuần tra.")
        return redirect('operations:mobile_dashboard')

    # Lấy hoặc tạo lượt tuần tra mới cho ca này
    luot_tuan_tra, created = LuotTuanTra.objects.get_or_create(
        ca_truc=ca_truc_hien_tai,
        loai_tuan_tra=lo_trinh,
        thoi_gian_ket_thuc__isnull=True,  # Chỉ lấy lượt chưa hoàn thành
        defaults={'thoi_gian_bat_dau': timezone.now()}
    )

    diem_da_quet = luot_tuan_tra.cac_ghi_nhan.all()

    context = {
        'lo_trinh': lo_trinh,
        'luot_tuan_tra': luot_tuan_tra,
        'diem_da_quet': diem_da_quet,
    }

    return render(request, 'inspection/mobile/tuan_tra.html', context)


@login_required
def chi_tiet_luot_tuan_tra_view(request, luot_tuan_tra_id):
    luot_tuan_tra = get_object_or_404(LuotTuanTra, id=luot_tuan_tra_id)
    # Sử dụng đúng related_name từ model GhiNhanTuanTra
    diem_da_quet = luot_tuan_tra.cac_ghi_nhan.all().order_by('thoi_gian_quet')
    
    context = {
        'luot_tuan_tra': luot_tuan_tra,
        'diem_da_quet': diem_da_quet
    }
    return render(request, 'inspection/mobile/chi_tiet_luot_tuan_tra.html', context)