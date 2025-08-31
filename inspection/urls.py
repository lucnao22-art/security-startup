# file: inspection/urls.py

from django.urls import path
from . import views

app_name = "inspection"

urlpatterns = [
    # URL cho trang bắt đầu tuần tra của nhân viên
    path("mobile/tuan-tra/", views.tuan_tra_mobile_view, name="mobile_tuan_tra"),
    # URL để xem chi tiết một lượt tuần tra đang diễn ra
    path(
        "mobile/luot-tuan-tra/<int:luot_tuan_tra_id>/",
        views.chi_tiet_luot_tuan_tra_view,
        name="mobile_chi_tiet_luot_tuan_tra",
    ),
]
