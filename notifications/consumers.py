# file: notifications/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Lấy user ID từ scope, nếu user đã đăng nhập
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        # Mỗi user sẽ có một "phòng" riêng để nhận thông báo
        self.room_group_name = f'user_{self.user.id}_notifications'

        # Tham gia vào group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Rời khỏi group khi ngắt kết nối
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Hàm này được gọi khi có thông báo mới được gửi tới group
    async def send_notification(self, event):
        message = event['message']

        # Gửi tin nhắn tới WebSocket client
        await self.send(text_data=json.dumps({
            'message': message
        }))