# file: operations/urls.py

from django.urls import path
from . import views

app_name = "operations"

urlpatterns = [
    path("dashboard/", views.van_hanh_dashboard_view, name="dashboard-van-hanh"),
    # Định nghĩa URL cho trang xếp lịch
    path("xep-lich/", views.xep_lich_view, name="xep-lich"),
    # URL cho HTMX để lấy chi tiết ca
    path("chi-tiet-ca/<int:phan_cong_id>/", views.chi_tiet_ca, name="chi_tiet_ca"),
    path(
        "them-ca-form/<int:vi_tri_id>/<int:ca_id>/<str:ngay>/",
        views.them_ca_form_view,
        name="them_ca_form",
    ),
    path("luu-ca/", views.luu_ca_view, name="luu_ca"),
    path("sua-ca-form/<int:phan_cong_id>/", views.sua_ca_form_view, name="sua_ca_form"),
    path("xoa-ca/<int:phan_cong_id>/", views.xoa_ca_view, name="xoa_ca"),
]
