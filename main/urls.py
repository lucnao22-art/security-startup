# file: main/urls.py

from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    # URL cho trang chủ và đăng nhập
    path("", views.homepage, name="homepage"),

    # URL cho trang điều phối (hub) sau khi đăng nhập
    path("hub/", views.dashboard_hub_view, name="dashboard_hub"),

    # URL cho đăng xuất
    path("logout/", views.logout_view, name="logout"),

    # URL cho trang thông báo quên mật khẩu (ĐÃ ĐƠN GIẢN HÓA)
    path('password-reset-notice/', views.password_reset_notice_view, name='password_reset'),
]