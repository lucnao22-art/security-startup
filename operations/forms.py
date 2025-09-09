# file: operations/forms.py

from django import forms
from .models import BaoCaoSuCo, ChamCong

class CheckInForm(forms.ModelForm):
    """
    Form đơn giản cho việc check-in, chỉ yêu cầu ảnh.
    """
    class Meta:
        model = ChamCong
        fields = ['anh_check_in']
        widgets = {
            'anh_check_in': forms.ClearableFileInput(attrs={
                'class': 'file-input file-input-bordered w-full',
                'accept': 'image/*',
                'capture': 'user' # Ưu tiên mở camera trước trên di động
            })
        }
        labels = {
            'anh_check_in': 'Chụp ảnh selfie của bạn'
        }

class CheckOutForm(forms.ModelForm):
    """
    Form đơn giản cho việc check-out, chỉ yêu cầu ảnh.
    """
    class Meta:
        model = ChamCong
        fields = ['anh_check_out']
        widgets = {
            'anh_check_out': forms.ClearableFileInput(attrs={
                'class': 'file-input file-input-bordered w-full',
                'accept': 'image/*',
                'capture': 'user' # Ưu tiên mở camera trước trên di động
            })
        }
        labels = {
            'anh_check_out': 'Chụp ảnh selfie của bạn'
        }

class BaoCaoSuCoForm(forms.ModelForm):
    """
    Form để nhân viên báo cáo sự cố từ giao diện mobile.
    """
    class Meta:
        model = BaoCaoSuCo
        fields = ['tieu_de', 'noi_dung', 'hinh_anh', 'nguoi_nhan']
        widgets = {
            'tieu_de': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'noi_dung': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 5}),
            'hinh_anh': forms.ClearableFileInput(attrs={'class': 'file-input file-input-bordered w-full'}),
            'nguoi_nhan': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }
        labels = {
            'tieu_de': 'Tiêu đề sự cố',
            'noi_dung': 'Mô tả chi tiết',
            'hinh_anh': 'Hình ảnh minh họa (nếu có)',
            'nguoi_nhan': 'Báo cáo cho',
        }