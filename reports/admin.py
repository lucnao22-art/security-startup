# file: reports/admin.py

from django.contrib import admin
from .models import BaoCao

@admin.register(BaoCao)
class BaoCaoAdmin(admin.ModelAdmin):
    # Tùy chỉnh để không hiển thị danh sách các bản ghi không có thật
    def changelist_view(self, request, extra_context=None):
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        # Tự động chuyển hướng đến trang báo cáo đầu tiên khi bấm vào
        return HttpResponseRedirect(reverse("reports:cham_cong_ca_nhan"))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False