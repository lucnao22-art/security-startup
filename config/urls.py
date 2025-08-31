# file: config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("main.urls")),
    path("admin/", admin.site.urls),
    path("ops/", include("operations.urls", namespace="operations")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("users/", include("users.urls", namespace="users")),
    path("backup/", include("backup_restore.urls", namespace="backup_restore")),
    path("clients/", include("clients.urls", namespace="clients")),
    path("inspection/", include("inspection.urls", namespace="inspection")),
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
