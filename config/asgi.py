# file: config/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import notifications.routing  # Import routing của app notifications

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Lấy ứng dụng Django HTTP truyền thống
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # Xử lý các request HTTP bằng ứng dụng Django
    "http": django_asgi_app,

    # Xử lý các request WebSocket
    "websocket": AuthMiddlewareStack(
        URLRouter(
            notifications.routing.websocket_urlpatterns
        )
    ),
})