from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    # Dòng này đã định nghĩa URL gốc ("") là 'homepage', đây là cấu hình chính xác.
    path("", views.homepage_view, name="homepage"),
    
    path("hub/", views.dashboard_hub_view, name="dashboard-hub"),
    path("logout/", views.logout_view, name="logout"),
]