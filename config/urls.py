# file: config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/ops/mobile/login/', permanent=True)),
    path('admin/', admin.site.urls),
    path('ops/', include('operations.urls', namespace='operations')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('users/', include('users.urls', namespace='users')),
    path('backup/', include('backup_restore.urls', namespace='backup')),
]

# Thêm dòng này vào cuối file để phục vụ file media trong môi trường development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)