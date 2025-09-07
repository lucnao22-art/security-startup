# file: inventory/forms.py

from django import forms
from .models import CapPhatCaNhan, VatTu
from users.models import NhanVien

class CapPhatCaNhanForm(forms.ModelForm):
    # Tùy chỉnh các trường để có giao diện đẹp hơn
    vat_tu = forms.ModelChoiceField(
        queryset=VatTu.objects.order_by('ten_vat_tu'),
        label="Chọn vật tư cấp phát",
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )
    nguoi_nhan = forms.ModelChoiceField(
        queryset=NhanVien.objects.filter(user__is_active=True).order_by('ho_ten'),
        label="Chọn nhân viên nhận",
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )
    so_luong = forms.IntegerField(
        label="Số lượng cấp phát",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'})
    )
    ghi_chu = forms.CharField(
        label="Ghi chú (nếu có)",
        required=False,
        widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3})
    )

    class Meta:
        model = CapPhatCaNhan
        fields = ['vat_tu', 'nguoi_nhan', 'so_luong', 'ghi_chu']

    # Logic kiểm tra tồn kho trước khi lưu
    def clean_so_luong(self):
        so_luong = self.cleaned_data.get('so_luong')
        vat_tu = self.cleaned_data.get('vat_tu')
        if vat_tu and so_luong:
            if so_luong > vat_tu.so_luong_ton:
                raise forms.ValidationError(
                    f"Số lượng tồn kho không đủ. Hiện chỉ còn {vat_tu.so_luong_ton} {vat_tu.don_vi_tinh}."
                )
        return so_luong