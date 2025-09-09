# file: main/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "main"

urlpatterns = [
    # Đây là URL sẽ render trang đăng nhập của bạn
    path("", auth_views.LoginView.as_view(template_name="main/homepage.html"), name="homepage"),
    
    path("hub/", views.dashboard_hub_view, name="dashboard-hub"),
    path("logout/", views.logout_view, name="logout"),
]