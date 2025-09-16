# file: operations/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Chỉ cho phép admin hoặc người có quyền quản lý kết nối
        if self.scope["user"].is_staff:
            self.room_group_name = "manager_notifications"

            # Tham gia vào nhóm (room)
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Rời khỏi nhóm khi ngắt kết nối
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    # Nhận tin nhắn từ group và gửi xuống cho client (trình duyệt)
    async def send_notification(self, event):
        message = event["message"]

        # Gửi tin nhắn đến WebSocket
        await self.send(text_data=json.dumps({"message": message}))
