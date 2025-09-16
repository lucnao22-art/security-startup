# file: operations/forms.py

from django import forms
from .models import BaoCaoSuCo

# ==============================================================================
# FORM ĐĂNG NHẬP CHO GIAO DIỆN MOBILE (BỔ SUNG)
# ==============================================================================
class MobileLoginForm(forms.Form):
    """
    Form đăng nhập dành cho giao diện mobile.
    """
    username = forms.CharField(
        label="Tên đăng nhập hoặc Mã nhân viên",
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full', 
            'placeholder': 'Nhập tài khoản',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full', 
            'placeholder': '••••••••'
        })
    )


# ==============================================================================
# FORM BÁO CÁO SỰ CỐ (TỐI ƯU TỪ CODE CỦA BẠN)
# ==============================================================================
class BaoCaoSuCoForm(forms.ModelForm):
    """
    Form báo cáo sự cố dành cho nhân viên trên giao diện mobile.
    """
    class Meta:
        model = BaoCaoSuCo
        fields = ["tieu_de", "noi_dung", "hinh_anh"]
        labels = {
            "tieu_de": "Tiêu đề sự cố",
            "noi_dung": "Mô tả chi tiết",
            "hinh_anh": "Hình ảnh minh họa (nếu có)",
        }
        widgets = {
            "tieu_de": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Ví dụ: Phát hiện cửa kho bị mở",
                }
            ),
            "noi_dung": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 5,
                    "placeholder": "Mô tả chi tiết sự việc, thời gian, địa điểm...",
                }
            ),
            "hinh_anh": forms.ClearableFileInput(
                attrs={"class": "file-input file-input-bordered w-full"}
            ),
        }