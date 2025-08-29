# file: operations/urls.py
from django.urls import path
from . import views

app_name = 'operations'

urlpatterns = [
    path('xep-lich/', views.xep_lich_view, name='xep-lich'),
    path('them-ca-form/', views.them_ca_form_view, name='them-ca-form'),
    path('luu-ca/', views.luu_ca_view, name='luu-ca'),
    path('xoa-ca/<int:phan_cong_id>/', views.xoa_ca_view, name='xoa-ca'),
    path('sua-ca-form/<int:phan_cong_id>/', views.sua_ca_form_view, name='sua-ca-form'),
    path('cap-nhat-ca/<int:phan_cong_id>/', views.cap_nhat_ca_view, name='cap-nhat-ca'),
    path('chi-tiet-ca/<int:phan_cong_id>/', views.chi_tiet_ca_view, name='chi-tiet-ca'),
    path('tim-kiem-nhan-vien/', views.tim_kiem_nhan_vien_view, name='tim-kiem-nhan-vien'),
    path('muc-tieu/', views.danh_sach_muc_tieu_view, name='danh-sach-muc-tieu'),
    path('muc-tieu/<int:muc_tieu_id>/', views.chi_tiet_muc_tieu_view, name='chi-tiet-muc-tieu'),
   

    # URLs CHO GIAO DIỆN DI ĐỘNG
    path('mobile/login/', views.mobile_login_view, name='mobile-login'),
    path('mobile/dashboard/', views.mobile_dashboard_view, name='mobile-dashboard'),
    path('mobile/logout/', views.mobile_logout_view, name='mobile-logout'),
    path('mobile/cham-cong/', views.mobile_cham_cong_view, name='mobile-cham-cong'),
    path('mobile/bao-cao-su-co/', views.mobile_bao_cao_su_co_view, name='mobile-bao-cao-su-co'),
    path('mobile/bao-cao-de-xuat/', views.mobile_bao_cao_de_xuat_view, name='mobile-bao-cao-de-xuat'),
]