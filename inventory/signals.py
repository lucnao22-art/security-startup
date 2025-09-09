# file: inventory/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# Thêm ChiTietPhieuXuat
from .models import PhieuNhap, PhieuXuat, VatTu, ChiTietPhieuXuat, ChiTietCapPhat

# ... (giữ nguyên signal cho PhieuNhap) ...

# XÓA HOÀN TOÀN signal `update_stock_on_export` cũ

# Signal mới cho ChiTietPhieuXuat
@receiver(post_save, sender=ChiTietPhieuXuat)
def update_stock_on_detail_export_save(sender, instance, created, **kwargs):
    if created:
        instance.vat_tu.so_luong_ton -= instance.so_luong
        instance.vat_tu.save()

@receiver(post_delete, sender=ChiTietPhieuXuat)
def update_stock_on_detail_export_delete(sender, instance, **kwargs):
    # Hoàn lại kho khi một dòng chi tiết bị xóa
    instance.vat_tu.so_luong_ton += instance.so_luong
    instance.vat_tu.save()

# Signal tương tự cho cấp phát cá nhân (để đảm bảo tính nhất quán)
@receiver(post_save, sender=ChiTietCapPhat)
def update_stock_on_detail_alloc_save(sender, instance, created, **kwargs):
    if created:
        instance.vat_tu.so_luong_ton -= instance.so_luong
        instance.vat_tu.save()

@receiver(post_delete, sender=ChiTietCapPhat)
def update_stock_on_detail_alloc_delete(sender, instance, **kwargs):
    instance.vat_tu.so_luong_ton += instance.so_luong
    instance.vat_tu.save()