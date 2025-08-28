# file: operations/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BaoCaoSuCo

@receiver(post_save, sender=BaoCaoSuCo)
def auto_assign_report(sender, instance, created, **kwargs):
    if created:
        nguoi_bao_cao = instance.ca_truc.nhan_vien
        if nguoi_bao_cao and nguoi_bao_cao.quan_ly_truc_tiep:
            instance.nguoi_chiu_trach_nhiem = nguoi_bao_cao.quan_ly_truc_tiep
            instance.save()