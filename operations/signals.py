# file: operations/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import BaoCaoSuCo


@receiver(post_save, sender=BaoCaoSuCo)
def send_incident_notification(sender, instance, created, **kwargs):
    """
    Gửi thông báo real-time khi có báo cáo sự cố mới được tạo.
    """
    if created:
        channel_layer = get_channel_layer()
        message = f"Sự cố mới: '{instance.tieu_de}' tại mục tiêu {instance.ca_truc.vi_tri_chot.muc_tieu.ten_muc_tieu}."

        async_to_sync(channel_layer.group_send)(
            "manager_notifications",
            {
                "type": "send.notification",  # Sẽ gọi đến hàm send_notification trong consumer
                "message": message,
            },
        )
