# file: main/urls.py
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    # Sửa lại tên view ở đây từ homepage thành homepage_view
    path("", views.homepage_view, name="homepage"),
    path("hub/", views.dashboard_hub_view, name="dashboard-hub"),
]