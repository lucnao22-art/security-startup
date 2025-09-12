# file: config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('operations/', include('operations.urls')),
    path('clients/', include('clients.urls')),
    path('inventory/', include('inventory.urls')),
    path('inspection/', include('inspection.urls')),
    path('accounting/', include('accounting.urls')),
    path('workflow/', include('workflow.urls')),
    path('backup/', include('backup_restore.urls')),
    path('reports/', include('reports.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("", include("main.urls", namespace="main")), # Đảm bảo main.urls được include cuối cùng cho trang chủ
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])