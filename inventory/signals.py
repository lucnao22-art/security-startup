# file: inventory/signals.py
from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CapPhatCaNhan, CapPhatMucTieu

@receiver(post_save, sender=CapPhatCaNhan)
@receiver(post_save, sender=CapPhatMucTieu)
def tru_kho_khi_cap_phat(sender, instance, created, **kwargs):
    """
    Tự động trừ kho khi một phiếu cấp phát mới được tạo.
    """
    if created: # Chỉ chạy khi phiếu được TẠO MỚI
        vat_tu = instance.vat_tu
        with transaction.atomic():
            # Lock a row to prevent race conditions
            vt = vat_tu.__class__.objects.select_for_update().get(pk=vat_tu.pk)
            vt.so_luong_ton_kho -= instance.so_luong
            vt.save()

@receiver(post_delete, sender=CapPhatCaNhan)
@receiver(post_delete, sender=CapPhatMucTieu)
def hoan_kho_khi_xoa(sender, instance, **kwargs):
    """
    Tự động hoàn trả lại kho khi một phiếu cấp phát bị XÓA.
    """
    vat_tu = instance.vat_tu
    with transaction.atomic():
        vt = vat_tu.__class__.objects.select_for_update().get(pk=vat_tu.pk)
        vt.so_luong_ton_kho += instance.so_luong
        vt.save()