# file: main/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# --- View trang chủ và xử lý đăng nhập (Giữ nguyên cấu trúc) ---
def homepage(request):
    """
    Hiển thị trang chủ/đăng nhập.
    - Nếu người dùng đã đăng nhập, chuyển hướng họ tới hub.
    - Xử lý form đăng nhập khi người dùng gửi thông tin (POST request).
    """
    if request.user.is_authenticated:
        return redirect('main:dashboard_hub')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:dashboard_hub')
            else:
                messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
    
    form = AuthenticationForm()
    return render(request, "main/homepage.html", {'form': form})


# --- NÂNG CẤP: Tái cấu trúc view điều phối để dễ mở rộng ---
@login_required
def dashboard_hub_view(request):
    """
    Hoạt động như một trung tâm điều phối, chuyển hướng người dùng đến dashboard phù hợp
    dựa trên vai trò và phòng ban của họ.
    """
    user = request.user

    # Superuser luôn được ưu tiên vào dashboard quản trị tổng quan
    if user.is_superuser:
        return redirect("dashboard:dashboard_view")

    # Ánh xạ tên phòng ban tới URL dashboard tương ứng.
    # -> Dễ dàng thêm phòng ban mới ở đây trong tương lai.
    PHONG_BAN_DASHBOARDS = {
        "Phòng Vận hành": "operations:mobile_dashboard",
        "Phòng Kinh doanh": "clients:dashboard-kinh-doanh",
        # Ví dụ: "Phòng Kế toán": "accounting:dashboard_ketoan",
    }
    
    # URL mặc định cho nhân viên không thuộc các phòng ban trên
    DEFAULT_NHANVIEN_DASHBOARD = "operations:mobile_dashboard"
    
    # URL mặc định chung nếu không có điều kiện nào khớp
    DEFAULT_DASHBOARD = "dashboard:dashboard_view"

    # Kiểm tra an toàn xem user có phải là nhân viên không
    if hasattr(user, 'nhanvien'):
        nhan_vien = user.nhanvien
        
        # Nếu nhân viên có phòng ban và phòng ban đó có trong danh sách ánh xạ
        if nhan_vien.phong_ban and nhan_vien.phong_ban.ten_phong_ban in PHONG_BAN_DASHBOARDS:
            url_name = PHONG_BAN_DASHBOARDS[nhan_vien.phong_ban.ten_phong_ban]
            return redirect(url_name)
        
        # Nếu không, chuyển đến dashboard mặc định của nhân viên
        return redirect(DEFAULT_NHANVIEN_DASHBOARD)

    # Nếu user không phải superuser và cũng không liên kết với nhân viên nào
    return redirect(DEFAULT_DASHBOARD)


# --- View xử lý đăng xuất (Giữ nguyên cấu trúc) ---
def logout_view(request):
    """
    Xử lý yêu cầu đăng xuất của người dùng và hiển thị thông báo.
    """
    logout(request)
    messages.success(request, "Bạn đã đăng xuất thành công.")
    return redirect('main:homepage')
# --- THÊM VIEW MỚI CHO TRANG THÔNG BÁO QUÊN MẬT KHẨU ---
def password_reset_notice_view(request):
    """
    Hiển thị trang thông báo hướng dẫn người dùng liên hệ quản lý.
    """
    return render(request, 'main/password_reset_notice.html')