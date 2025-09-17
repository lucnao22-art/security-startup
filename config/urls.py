# file: config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from operations import views as operations_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('users/', include('users.urls')),
    path('clients/', include('clients.urls')),
    path('operations/', include('operations.urls')),
    path('inspection/', include('inspection.urls')),
    path('inventory/', include('inventory.urls')),
    path('accounting/', include('accounting.urls')),
    path('reports/', include('reports.urls')),
    path('workflow/', include('workflow.urls')),
    path('notifications/', include('notifications.urls')),
    path('backup/', include('backup_restore.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('mobile/', include('mobile.urls')),

    # URL đăng nhập cho mobile
    path('mobile/login/', operations_views.mobile_login_view, name='mobile_login'),
]
# === BẮT ĐẦU PHẦN SỬA LỖI ===
# Chỉ thêm URL của Debug Toolbar khi ở chế độ DEBUG
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
# === KẾT THÚC PHẦN SỬA LỖI ===
# ==============================================================================
# BỔ SUNG CẤU HÌNH CHO STATIC VÀ MEDIA FILES
# ==============================================================================
if settings.DEBUG:
    # Thêm dòng sau để phục vụ static files (logo, css, js)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Dòng này để phục vụ media files (ảnh người dùng tải lên)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)