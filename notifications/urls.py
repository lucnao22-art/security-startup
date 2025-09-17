# notifications/urls.py

from django.urls import path
from . import views

# app_name giúp Django phân biệt các URL của ứng dụng này với các ứng dụng khác.
# Điều này rất quan trọng để tránh xung đột tên URL và giúp mã nguồn dễ quản lý hơn.
# Ví dụ, trong template bạn có thể gọi URL một cách tường minh: {% url 'notifications:ten_url' %}
app_name = 'notifications'

urlpatterns = [
    # Hiện tại, ứng dụng 'notifications' của bạn được thiết kế cho WebSocket
    # và chưa có view nào để xử lý các yêu cầu HTTP.
    #
    # Do đó, danh sách urlpatterns này có thể để trống.
    # Việc có tệp này sẽ khắc phục được lỗi ModuleNotFoundError khi Django khởi chạy.
    #
    # DƯỚI ĐÂY LÀ VÍ DỤ NẾU BẠN MUỐN THÊM CÁC TRANG WEB CHO ỨNG DỤNG NÀY TRONG TƯƠNG LAI:
    #
    # path('', views.danh_sach_thong_bao, name='danh-sach'),
    # path('<int:pk>/', views.chi_tiet_thong_bao, name='chi-tiet'),
    # path('<int:pk>/danh-dau-da-doc/', views.danh_dau_da_doc, name='danh-dau-da-doc'),
]