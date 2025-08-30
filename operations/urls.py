# file: operations/urls.py

from django.urls import path
from . import views

app_name = 'operations'

urlpatterns = [
    # Định nghĩa URL cho trang xếp lịch
    path('xep-lich/', views.xep_lich_view, name='xep-lich'),
    path('them-ca-form/', views.them_ca_form_view, name='them-ca-form'),
    # Thêm dòng này:
    path('luu-ca/', views.luu_ca_view, name='luu-ca'),
    path('xoa-ca/<int:phan_cong_id>/', views.xoa_ca_view, name='xoa-ca'),
    path('sua-ca-form/<int:phan_cong_id>/', views.sua_ca_form_view, name='sua-ca-form'),
]