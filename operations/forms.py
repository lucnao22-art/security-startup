# file: operations/forms.py

from django import forms
from .models import BaoCaoSuCo


class BaoCaoSuCoForm(forms.ModelForm):
    class Meta:
        model = BaoCaoSuCo
        # Chỉ lấy các trường cần cho nhân viên nhập liệu
        fields = ["tieu_de", "noi_dung", "hinh_anh"]
        widgets = {
            "tieu_de": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ví dụ: Phát hiện cửa kho bị mở",
                }
            ),
            "noi_dung": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Mô tả chi tiết sự việc...",
                }
            ),
            "hinh_anh": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "tieu_de": "Tiêu đề sự cố",
            "noi_dung": "Mô tả chi tiết",
            "hinh_anh": "Hình ảnh minh họa (nếu có)",
        }
