from django.db import models
from django.urls import reverse
from users.models import NhanVien
from operations.models import MucTieu

class Task(models.Model):
    """Model cho việc giao việc"""
    class Priority(models.TextChoices):
        THAP = 'Thấp', 'Thấp'
        TRUNG_BINH = 'Trung bình', 'Trung bình'
        CAO = 'Cao', 'Cao'

    class Status(models.TextChoices):
        MOI = 'Mới', 'Mới'
        DANG_TIEN_HANH = 'Đang tiến hành', 'Đang tiến hành'
        HOAN_THANH = 'Hoàn thành', 'Hoàn thành'
        DA_HUY = 'Đã hủy', 'Đã hủy'

    tieu_de = models.CharField(max_length=255, verbose_name="Tiêu đề Công việc")
    noi_dung = models.TextField(verbose_name="Nội dung chi tiết")
    nguoi_giao = models.ForeignKey(NhanVien, on_delete=models.CASCADE, related_name='giao_viec', verbose_name="Người giao")
    nguoi_nhan = models.ForeignKey(NhanVien, on_delete=models.CASCADE, related_name='nhan_viec', verbose_name="Người nhận")
    muc_tieu = models.ForeignKey(MucTieu, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Liên quan đến mục tiêu")
    
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    han_chot = models.DateTimeField(verbose_name="Hạn chót")
    
    uu_tien = models.CharField(max_length=20, choices=Priority.choices, default=Priority.TRUNG_BINH, verbose_name="Độ ưu tiên")
    trang_thai = models.CharField(max_length=20, choices=Status.choices, default=Status.MOI, verbose_name="Trạng thái")
    
    file_dinh_kem = models.FileField(upload_to='task_attachments/', blank=True, null=True, verbose_name="File đính kèm")

    def __str__(self):
        return self.tieu_de

    def get_absolute_url(self):
        return reverse('workflow:task_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Công việc"
        verbose_name_plural = "Các Công việc"

class Proposal(models.Model):
    """Model cho các đề xuất/kiến nghị"""
    class Status(models.TextChoices):
        CHO_DUYET = 'Chờ duyệt', 'Chờ duyệt'
        DA_DUYET = 'Đã duyệt', 'Đã duyệt'
        TU_CHOI = 'Từ chối', 'Từ chối'

    tieu_de = models.CharField(max_length=255, verbose_name="Tiêu đề Đề xuất")
    noi_dung = models.TextField(verbose_name="Nội dung")
    nguoi_de_xuat = models.ForeignKey(NhanVien, on_delete=models.CASCADE, related_name='de_xuat', verbose_name="Người đề xuất")
    nguoi_duyet = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True, blank=True, related_name='duyet_de_xuat', verbose_name="Người duyệt")
    
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    ngay_duyet = models.DateTimeField(null=True, blank=True, verbose_name="Ngày duyệt")
    
    trang_thai = models.CharField(max_length=20, choices=Status.choices, default=Status.CHO_DUYET, verbose_name="Trạng thái")
    phan_hoi = models.TextField(blank=True, verbose_name="Phản hồi của người duyệt")
    
    file_dinh_kem = models.FileField(upload_to='proposal_attachments/', blank=True, null=True, verbose_name="File đính kèm")

    def __str__(self):
        return self.tieu_de
    
    def get_absolute_url(self):
        return reverse('workflow:proposal_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Đề xuất"
        verbose_name_plural = "Các Đề xuất"