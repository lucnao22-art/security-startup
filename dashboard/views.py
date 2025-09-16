# file: dashboard/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from datetime import timedelta
from django.contrib.auth import logout

# Import models sẽ được thực hiện bên trong view để tối ưu và tránh lỗi import vòng.

@login_required
def dashboard_view(request):
    """
    View này đóng vai trò là trung tâm điều phối sau khi đăng nhập.
    - Superuser và Quản lý sẽ xem dashboard chính.
    - Nhân viên sẽ được chuyển hướng đến mobile dashboard.
    """
    user = request.user

    # Di chuyển các lệnh import vào đây để chỉ load khi cần thiết
    from users.models import NhanVien
    
    # 1. KIỂM TRA VAI TRÒ VÀ CHUYỂN HƯỚNG
    
    # Superuser luôn có quyền truy cập dashboard chính
    if user.is_superuser:
        pass  # Để code chạy tiếp và render dashboard của quản lý

    # Kiểm tra xem user có phải là nhân viên không
    elif hasattr(user, 'nhan_vien'):
        nhan_vien = user.nhan_vien
        
        # Các chức danh được phép xem dashboard chính
        manager_roles = ["Quản lý", "Giám đốc", "Admin", "Trưởng phòng"]

        # Nếu chức danh không thuộc nhóm quản lý -> chuyển hướng
        if not (nhan_vien.chuc_danh and nhan_vien.chuc_danh.ten_chuc_danh in manager_roles):
            return redirect('operations:mobile_dashboard')
    
    else:
        # Nếu user đã đăng nhập nhưng không có hồ sơ nhân viên, đây là trường hợp bất thường.
        # Đăng xuất và đưa về trang login để tránh lỗi.
        logout(request)
        return redirect('operations:mobile_login')

    # 2. THU THẬP DỮ LIỆU (CHỈ DÀNH CHO QUẢN LÝ)
    # Phần code này chỉ chạy khi người dùng được phép xem dashboard chính.
    from clients.models import KhachHangTiemNang
    from operations.models import PhanCongCaTruc, BaoCaoSuCo
    from inspection.models import LuotTuanTra

    # === THU THẬP SỐ LIỆU THỐNG KÊ (Dạng thẻ) ===
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
        target_date = today - timedelta(days=i)
        labels.append(f"{target_date.day}/{target_date.month}")

        patrols = LuotTuanTra.objects.filter(thoi_gian_bat_dau__date=target_date).count()
        tuan_tra_data.append(patrols)

        incidents = BaoCaoSuCo.objects.filter(thoi_gian_bao_cao__date=target_date).count()
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
        'section': 'dashboard', # Thêm section để sidebar có thể highlight đúng mục
    }
    
    return render(request, 'dashboard/main.html', context)