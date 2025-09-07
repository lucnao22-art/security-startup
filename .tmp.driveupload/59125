# workflow/admin.py

from django.contrib import admin
from .models import Task, Proposal

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('tieu_de', 'nguoi_giao', 'nguoi_nhan', 'han_chot', 'trang_thai', 'uu_tien')
    list_filter = ('trang_thai', 'uu_tien', 'nguoi_giao', 'nguoi_nhan')
    search_fields = ('tieu_de', 'noi_dung')

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('tieu_de', 'nguoi_de_xuat', 'nguoi_duyet', 'trang_thai', 'ngay_tao')
    list_filter = ('trang_thai', 'nguoi_de_xuat', 'nguoi_duyet')
    search_fields = ('tieu_de', 'noi_dung')