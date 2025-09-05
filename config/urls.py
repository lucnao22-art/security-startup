# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # --- URL CHO CÁC CHỨC NĂNG CỐT LÕI & ADMIN ---
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),

    # --- URL CHO CÁC APP CHỨC NĂNG (THEO TỪNG MODULE) ---
    path("hub/", include("dashboard.urls")),
    path("operations/", include("operations.urls")),
    path("clients/", include("clients.urls")),
    path("users/", include("users.urls")),
    path("inspection/", include("inspection.urls")),
    path("inventory/", include("inventory.urls")),
    path("accounting/", include("accounting.urls")),
    path("backup/", include("backup_restore.urls")),
    path('workflow/', include('workflow.urls')),
    
    # --- URL CHO CÁC CÔNG CỤ PHÁT TRIỂN ---
    path("__debug__/", include("debug_toolbar.urls")),

    # --- URL GỐC CỦA TRANG WEB (ĐẶT CUỐI CÙNG) ---
    # Nạp tất cả các URL từ app 'main', bao gồm cả trang chủ ('homepage').
    path("", include("main.urls")), 
]

# --- Cấu hình để hiển thị các tệp media trong môi trường DEBUG ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)