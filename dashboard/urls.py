# file: dashboard/urls.py

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dòng này đảm bảo rằng có một URL tên là 'dashboard_view'
    # trỏ đến view xử lý dashboard chính của bạn.
    path('', views.dashboard_view, name='dashboard_view'),
]