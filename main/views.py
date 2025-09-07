# file: main/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.models import CompanyProfile

# --- PHẦN NÀY ĐƯỢC GIỮ NGUYÊN ---
def homepage_view(request):
    return render(request, "main/homepage.html")

# --- PHẦN NÀY ĐÃ ĐƯỢC CHỈNH SỬA ---
@login_required
def dashboard_hub_view(request):
    """
    View này hoạt động như một trung tâm điều phối.
    Nó kiểm tra vai trò và phòng ban của người dùng để chuyển hướng đến dashboard phù hợp.
    """
    user = request.user
    
    # Ưu tiên Superuser, sẽ luôn thấy dashboard tổng quan (Giữ nguyên)
    if user.is_superuser:
        return redirect("dashboard:dashboard_view")

    try:
        # Lấy thông tin nhân viên từ tài khoản user (Giữ nguyên)
        nhan_vien = user.nhanvien
        
        # Kiểm tra phòng ban để điều hướng tới các dashboard chuyên biệt (Giữ nguyên)
        if nhan_vien.phong_ban:
            # SỬA ĐỔI: Chuyển hướng nhân viên "Phòng Vận hành" về giao diện mobile theo yêu cầu.
            # Bạn có thể thay 'operations:mobile_dashboard' bằng tên URL đúng của giao diện mobile.
            if nhan_vien.phong_ban.ten_phong_ban == "Phòng Vận hành":
                return redirect("operations:mobile_dashboard")
                
            elif nhan_vien.phong_ban.ten_phong_ban == "Phòng Kinh doanh":
                return redirect("clients:dashboard-kinh-doanh")
            
            # Bạn có thể thêm các điều kiện elif khác cho các phòng ban khác ở đây

        # **THÊM MỚI:** Nếu là nhân viên nhưng không thuộc các phòng ban trên,
        # chuyển hướng đến giao diện mobile mặc định.
        # Đây là logic cốt lõi để giải quyết vấn đề của bạn.
        return redirect("operations:mobile_dashboard")

    except AttributeError:
        # Xử lý trường hợp tài khoản user không liên kết với nhân viên nào (Giữ nguyên)
        pass

    # Mặc định: Nếu không phải superuser và không phải nhân viên, hiển thị dashboard tổng quan (Giữ nguyên)
    return redirect("dashboard:dashboard_view")
# --- HÀM MỚI ĐỂ XỬ LÝ ĐĂNG XUẤT ---
def logout_view(request):
    """
    Xử lý yêu cầu đăng xuất của người dùng.
    """
    logout(request)
    messages.success(request, "Bạn đã đăng xuất thành công.")
    return redirect('main:homepage') # Chuyển hướng về trang chủ