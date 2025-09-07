# file: config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('hub/', include('dashboard.urls')),
    path('users/', include('users.urls')),
    path('operations/', include('operations.urls')),
    path('clients/', include('clients.urls')),
    path('inventory/', include('inventory.urls')),
    path('inspection/', include('inspection.urls')),
    path('accounting/', include('accounting.urls')),
    path('workflow/', include('workflow.urls')),
    path('backup/', include('backup_restore.urls')),

    # --- Đảm bảo dòng này đã có và đúng ---
    path('reports/', include('reports.urls')),

    path("__debug__/", include("debug_toolbar.urls")),
    path('', include('main.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)