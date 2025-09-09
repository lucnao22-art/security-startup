# file: inventory/urls.py

from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('bao-cao-ton-kho/', views.bao_cao_ton_kho_view, name='bao_cao_ton_kho'),
    path('phieu-cap-phat/<int:phieu_id>/in/', views.in_phieu_cap_phat_view, name='in_phieu_cap_phat'),
    path('phieu-xuat/<int:phieu_id>/in/', views.in_phieu_xuat_view, name='in_phieu_xuat'),
]