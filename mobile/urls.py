# mobile/urls.py

from django.urls import path
# Giả sử bạn sẽ tạo các view trong mobile/views.py
# from . import views

# app_name giúp Django phân biệt URL của các ứng dụng khác nhau.
# Đây là một phương pháp tối ưu để quản lý URL trong các dự án lớn.
# Khi cần gọi URL trong template, bạn có thể dùng: {% url 'mobile:ten_url' %}
app_name = 'mobile'

urlpatterns = [
    # Hiện tại, ứng dụng 'mobile' chưa có view nào được định nghĩa.
    # Danh sách này có thể để trống để sửa lỗi ModuleNotFoundError.
    #
    # Dưới đây là ví dụ để bạn có thể thêm URL trong tương lai:
    # Ví dụ:
    # path('dashboard/', views.mobile_dashboard, name='dashboard'),
    # path('profile/', views.user_profile, name='profile'),
]