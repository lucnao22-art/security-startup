# workflow/admin.py

from django.contrib import admin, messages
from django.utils import timezone
from django.utils.html import format_html
from .models import Task, Proposal

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'tieu_de', 
        'nguoi_giao', 
        'nguoi_nhan', 
        'get_han_chot_display', # Cải tiến: Hiển thị hạn chót có màu
        'trang_thai', 
        'uu_tien'
    )
    list_filter = ('trang_thai', 'uu_tien', 'nguoi_giao', 'nguoi_nhan', 'han_chot')
    search_fields = ('tieu_de', 'noi_dung', 'nguoi_nhan__ho_ten')
    list_select_related = ('nguoi_giao', 'nguoi_nhan')
    actions = ['mark_as_completed']

    @admin.display(description='Hạn chót', ordering='han_chot')
    def get_han_chot_display(self, obj):
        now = timezone.now()
        if obj.trang_thai != 'Hoàn thành' and obj.han_chot < now:
            # Nếu trễ hạn và chưa hoàn thành, bôi đỏ
            return format_html('<b style="color: red;">{}</b>', obj.han_chot.strftime('%d/%m/%Y %H:%M'))
        return obj.han_chot.strftime('%d/%m/%Y %H:%M')

    @admin.action(description='Đánh dấu là "Hoàn thành"')
    def mark_as_completed(self, request, queryset):
        updated_count = queryset.update(trang_thai='Hoàn thành')
        self.message_user(
            request,
            f'Đã cập nhật trạng thái cho {updated_count} công việc.',
            messages.SUCCESS
        )

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = (
        'tieu_de', 
        'nguoi_de_xuat', 
        'nguoi_duyet', 
        'trang_thai', 
        'ngay_tao',
        'thoi_gian_cho_duyet' # Cải tiến: Thêm cột thời gian chờ
    )
    list_filter = ('trang_thai', 'nguoi_de_xuat', 'nguoi_duyet')
    search_fields = ('tieu_de', 'noi_dung', 'nguoi_de_xuat__ho_ten')
    list_select_related = ('nguoi_de_xuat', 'nguoi_duyet')
    actions = ['approve_proposals', 'reject_proposals']

    @admin.display(description='Thời gian chờ')
    def thoi_gian_cho_duyet(self, obj):
        if obj.trang_thai == 'Chờ duyệt':
            delta = timezone.now() - obj.ngay_tao
            if delta.days > 0:
                return f"{delta.days} ngày"
            else:
                return "Mới"
        return '-'

    def _update_proposal_status(self, request, queryset, status, success_message):
        # Hàm nội bộ để tránh lặp code
        updated_count = 0
        for proposal in queryset:
            if proposal.trang_thai == 'Chờ duyệt':
                proposal.trang_thai = status
                proposal.nguoi_duyet = proposal.nguoi_de_xuat.user # Gán người duyệt là người dùng hiện tại
                proposal.ngay_duyet = timezone.now()
                proposal.save()
                updated_count += 1
        
        if updated_count > 0:
            self.message_user(
                request,
                f'Đã {success_message} {updated_count} đề xuất.',
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                'Chỉ có thể thực hiện hành động này trên các đề xuất đang "Chờ duyệt".',
                messages.WARNING
            )

    @admin.action(description='Phê duyệt các đề xuất đã chọn')
    def approve_proposals(self, request, queryset):
        self._update_proposal_status(request, queryset, 'Đã duyệt', 'phê duyệt')

    @admin.action(description='Từ chối các đề xuất đã chọn')
    def reject_proposals(self, request, queryset):
        self._update_proposal_status(request, queryset, 'Từ chối', 'từ chối')
