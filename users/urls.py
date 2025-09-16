# file: users/urls.py
from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    # URL cho form tùy chọn xuất lý lịch
    path(
        "<int:nhan_vien_id>/export-options/",
        views.export_ly_lich_options_view,
        name="export-ly-lich-options",
    ),
    # URL xử lý việc tạo PDF lý lịch
    path(
        "<int:nhan_vien_id>/export-pdf/",
        views.export_ly_lich_pdf,
        name="export-ly-lich",
    ),
    # URL mới cho việc in hợp đồng
    path(
        "hop-dong/<int:hop_dong_id>/print/",
        views.in_hop_dong_view,
        name="in-hop-dong"
    ),
    # URL mới cho việc in quyết định
    path(
        "quyet-dinh/<int:quyet_dinh_id>/print/",
        views.in_quyet_dinh_view,
        name="in-quyet-dinh"
    ),
]