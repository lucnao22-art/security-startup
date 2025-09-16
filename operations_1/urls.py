# file: operations/urls.py

from django.urls import path
from . import views

app_name = "operations"

urlpatterns = [
    # --- CÁC URL HIỆN TẠI CỦA BẠN (GIỮ NGUYÊN) ---
    path("dashboard/", views.van_hanh_dashboard_view, name="dashboard-van-hanh"),
    path("xep-lich/", views.xep_lich_view, name="xep-lich"),
    path("chi-tiet-ca/<int:phan_cong_id>/", views.chi_tiet_ca, name="chi_tiet_ca"),
    path(
        "them-ca-form/<int:vi_tri_id>/<int:ca_id>/<str:ngay>/",
        views.them_ca_form_view,
        name="them_ca_form",
    ),
    path("luu-ca/", views.luu_ca_view, name="luu_ca"),
    path("sua-ca-form/<int:phan_cong_id>/", views.sua_ca_form_view, name="sua_ca_form"),
    path("xoa-ca/<int:phan_cong_id>/", views.xoa_ca_view, name="xoa_ca"),

    # === CÁC URL CHO GIAO DIỆN MOBILE (ĐÃ SỬA LẠI) ===
    path('mobile/dashboard/', views.mobile_dashboard, name='mobile_dashboard'),
    path('mobile/lich-truc/', views.mobile_lich_truc_view, name='mobile_lich_truc'), # URL MỚI
    path('mobile/check-in/<int:phan_cong_id>/', views.check_in_view, name='check_in'), 
    path('mobile/check-out/<int:phan_cong_id>/', views.check_out_view, name='check_out'),
    path('mobile/bao-cao-su-co/', views.bao_cao_su_co_mobile_view, name='bao_cao_su_co'), 
]