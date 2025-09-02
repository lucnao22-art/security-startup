# file: config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # --- URL Mặc định ---
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),

    # --- URL CÁC ỨNG DỤNG (Đảm bảo mỗi ứng dụng chỉ được nạp một lần) ---
    path("", include("main.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("operations/", include("operations.urls")),
    path("clients/", include("clients.urls")),
    path("users/", include("users.urls")), # Dòng này kết nối users/urls.py
    path("inspection/", include("inspection.urls")),
    path("inventory/", include("inventory.urls")),
    path("accounting/", include("accounting.urls")),
    path("backup/", include("backup_restore.urls")),
]

# --- Cấu hình để hiển thị các tệp media (như ảnh thẻ) ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)