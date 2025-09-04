from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from users.models import NhanVien

from .models import Proposal, Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "workflow/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        """
        Hiển thị các công việc mà người dùng này đã giao hoặc được nhận.
        An toàn hơn bằng cách kiểm tra sự tồn tại của `nhanvien`.
        """
        try:
            nhan_vien = self.request.user.nhanvien
            return Task.objects.filter(
                Q(nguoi_giao=nhan_vien) | Q(nguoi_nhan=nhan_vien)
            ).order_by("-ngay_tao")
        except NhanVien.DoesNotExist:
            return Task.objects.none()  # Trả về danh sách rỗng nếu không có hồ sơ nhân viên


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "workflow/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "workflow/task_form.html"
    fields = [
        "tieu_de",
        "noi_dung",
        "nguoi_nhan",
        "muc_tieu",
        "han_chot",
        "uu_tien",
        "file_dinh_kem",
    ]

    def form_valid(self, form):
        """Tự động gán người giao là người dùng hiện tại."""
        form.instance.nguoi_giao = self.request.user.nhanvien
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "workflow/task_form.html"
    fields = ["trang_thai"]  # Người nhận chỉ được phép cập nhật trạng thái
    success_url = reverse_lazy("workflow:task_list")


class ProposalListView(LoginRequiredMixin, ListView):
    model = Proposal
    template_name = "workflow/proposal_list.html"
    context_object_name = "proposals"

    def get_queryset(self):
        """
        Hiển thị các đề xuất mà người dùng này tạo hoặc cần duyệt.
        """
        try:
            nhan_vien = self.request.user.nhanvien
            return Proposal.objects.filter(
                Q(nguoi_de_xuat=nhan_vien) | Q(nguoi_duyet=nhan_vien)
            ).order_by("-ngay_tao")
        except NhanVien.DoesNotExist:
            return Proposal.objects.none()


class ProposalDetailView(LoginRequiredMixin, DetailView):
    model = Proposal
    template_name = "workflow/proposal_detail.html"
    context_object_name = "proposal"


class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = Proposal
    template_name = "workflow/proposal_form.html"
    fields = ["tieu_de", "noi_dung", "nguoi_duyet", "file_dinh_kem"]

    def form_valid(self, form):
        """Tự động gán người đề xuất là người dùng hiện tại."""
        form.instance.nguoi_de_xuat = self.request.user.nhanvien
        return super().form_valid(form)

    def get_form(self, form_class=None):
        """Lọc danh sách người duyệt, chỉ hiển thị các quản lý."""
        form = super().get_form(form_class)
        form.fields["nguoi_duyet"].queryset = NhanVien.objects.filter(
            user__is_staff=True
        )
        return form


class ProposalReviewView(LoginRequiredMixin, UpdateView):
    model = Proposal
    template_name = "workflow/proposal_review_form.html"
    fields = ["trang_thai", "phan_hoi"]

    def form_valid(self, form):
        """Tự động cập nhật ngày duyệt khi quản lý thực hiện phê duyệt."""
        form.instance.ngay_duyet = timezone.now()
        return super().form_valid(form)