# file: dashboard/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from datetime import timedelta

# Import các model cần thiết sẽ được di chuyển vào trong view
# để tránh các lỗi import vòng lặp (circular import).

@login_required
def dashboard_view(request):
    """
    View này chịu trách nhiệm thu thập dữ liệu thống kê
    và hiển thị lên trang dashboard chính.
    """
    # Di chuyển các lệnh import vào đây để tránh lỗi circular import
    from users.models import NhanVien
    from clients.models import KhachHangTiemNang, MucTieu
    from operations.models import PhanCongCaTruc, BaoCaoSuCo
    from inspection.models import LuotTuanTra

    # === THU THẬP SỐ LIỆU THỐNG KÊ (Dạng thẻ) ===

    # SỬA LỖI CUỐI CÙNG: Lọc nhân viên đang hoạt động, bao gồm cả "Chính thức" và "Thử việc"
    active_statuses = [NhanVien.TrangThaiLamViec.CHINH_THUC, NhanVien.TrangThaiLamViec.THU_VIEC]
    total_nhanvien = NhanVien.objects.filter(trang_thai_lam_viec__in=active_statuses).count()
    
    total_khachhang = KhachHangTiemNang.objects.count()
    
    thirty_days_ago = timezone.now() - timedelta(days=30)
    su_co_gan_day = BaoCaoSuCo.objects.filter(thoi_gian_bao_cao__gte=thirty_days_ago).count()
    
    today = timezone.now().date()
    ca_truc_hom_nay = PhanCongCaTruc.objects.filter(ngay_truc=today).count()

    # === DỮ LIỆU CHO BẢNG "SỰ CỐ GẦN ĐÂY" ===
    cac_su_co_moi = BaoCaoSuCo.objects.order_by('-thoi_gian_bao_cao')[:5]

    # === DỮ LIỆU CHO BIỂU ĐỒ "HOẠT ĐỘNG 7 NGÀY QUA" ===
    labels = []
    tuan_tra_data = []
    su_co_data = []

    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        labels.append(f"{date.day}/{date.month}")

        patrols = LuotTuanTra.objects.filter(thoi_gian_bat_dau__date=date).count()
        tuan_tra_data.append(patrols)

        incidents = BaoCaoSuCo.objects.filter(thoi_gian_bao_cao__date=date).count()
        su_co_data.append(incidents)

    # === TỔNG HỢP DỮ LIỆU GỬI ĐẾN TEMPLATE ===
    context = {
        'total_nhanvien': total_nhanvien,
        'total_khachhang': total_khachhang,
        'su_co_gan_day': su_co_gan_day,
        'ca_truc_hom_nay': ca_truc_hom_nay,
        'cac_su_co_moi': cac_su_co_moi,
        'chart_labels': json.dumps(labels),
        'tuan_tra_data': json.dumps(tuan_tra_data),
        'su_co_data': json.dumps(su_co_data),
    }
    
    return render(request, 'dashboard/main.html', context)