# file: operations/signals.py

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import BaoCaoSuCo

# Lấy logger để ghi lại các hoạt động
logger = logging.getLogger(__name__)

@receiver(post_save, sender=BaoCaoSuCo)
def send_incident_notification(sender, instance, created, **kwargs):
    """
    Signal này được kích hoạt mỗi khi một đối tượng BaoCaoSuCo được lưu.
    Nếu đây là một sự cố MỚI (created=True), nó sẽ gửi thông báo real-time.
    """
    if created:
        channel_layer = get_channel_layer()
        group_name = 'admin_notifications'  # NÂNG CẤP 1: Đồng bộ tên group với consumer

        # NÂNG CẤP 2: Tạo một gói dữ liệu JSON có cấu trúc
        notification_data = {
            'title': 'Báo Cáo Sự Cố Mới',
            'body': f'Sự cố "{instance.tieu_de}" vừa được báo cáo tại mục tiêu {instance.ca_truc.vi_tri_chot.muc_tieu.ten_muc_tieu}.',
            # Cung cấp URL để người dùng có thể nhấp vào và xem chi tiết
            'url': f'/admin/operations/baocaosuco/{instance.id}/change/' 
        }

        try:
            # Gửi sự kiện đến group 'admin_notifications'
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'send_notification',  # Tên hàm trong consumer sẽ xử lý
                    'notification': notification_data  # Gửi đi gói dữ liệu đã cấu trúc
                }
            )
            # NÂNG CẤP 3: Ghi log khi gửi thông báo thành công
            logger.info(f"Sent real-time notification for new incident ID: {instance.id}")

        except Exception as e:
            # NÂNG CẤP 3: Ghi log nếu có lỗi xảy ra khi gửi
            logger.error(f"Failed to send notification for incident ID {instance.id}: {e}")