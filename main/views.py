# file: main/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.models import CompanyProfile

def homepage_view(request):
    return render(request, "main/homepage.html")

@login_required
def dashboard_hub_view(request):
    """
    View này hoạt động như một trung tâm điều phối.
    Nó kiểm tra phòng ban của người dùng và chuyển hướng đến dashboard phù hợp.
    """
    user = request.user
    
    # Ưu tiên Superuser, sẽ luôn thấy dashboard tổng quan
    if user.is_superuser:
        return redirect("dashboard:dashboard_view")

    try:
        # Lấy thông tin nhân viên từ tài khoản user
        nhan_vien = user.nhanvien
        
        # Kiểm tra phòng ban (sử dụng tên phòng ban bạn đã định nghĩa)
        if nhan_vien.phong_ban:
            if nhan_vien.phong_ban.ten_phong_ban == "Phòng Vận hành":
                return redirect("operations:dashboard-van-hanh")
            elif nhan_vien.phong_ban.ten_phong_ban == "Phòng Kinh doanh":
                return redirect("clients:dashboard-kinh-doanh")
            # Bạn có thể thêm các điều kiện elif khác cho các phòng ban khác ở đây

    except AttributeError:
        # Xử lý trường hợp tài khoản user không liên kết với nhân viên nào
        # (ví dụ: tài khoản admin được tạo nhưng chưa có hồ sơ nhân viên)
        pass

    # Mặc định: Nếu không thuộc phòng ban nào đặc biệt, hiển thị dashboard tổng quan
    return redirect("dashboard:dashboard_view")