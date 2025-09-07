# file: reports/urls.py

from django.urls import path
from . import views

app_name = 'reports' # Dòng này rất quan trọng để đăng ký namespace

urlpatterns = [
    path('cham-cong/ca-nhan/', views.bang_cham_cong_ca_nhan_view, name='cham_cong_ca_nhan'),
    path('cham-cong/muc-tieu/', views.bang_cham_cong_muc_tieu_view, name='cham_cong_muc_tieu'),
]