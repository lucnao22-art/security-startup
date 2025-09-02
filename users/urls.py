# file: users/urls.py
from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    # URL cho form tùy chọn
    path(
        "<int:nhan_vien_id>/export-options/",
        # SỬA LẠI TÊN HÀM Ở ĐÂY
        views.export_ly_lich_options_view,
        name="export-ly-lich-options",
    ),
    # URL xử lý việc tạo PDF
    path(
        "<int:nhan_vien_id>/export-pdf/",
        views.export_ly_lich_pdf,
        name="export-ly-lich",
    ),
]