# file: inventory/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Sửa lại các import cho gọn gàng và chính xác
from .models import VatTu, PhieuCapPhat, PhieuXuat

@login_required
def in_phieu_cap_phat_view(request, phieu_id):
    phieu = get_object_or_404(PhieuCapPhat.objects.select_related('nguoi_nhan', 'nguoi_cap_phat'), id=phieu_id)
    context = {'phieu': phieu}
    return render(request, 'inventory/print/phieu_cap_phat.html', context)

@login_required
def bao_cao_ton_kho_view(request):
    query = request.GET.get('q', '')
    vat_tu_list = VatTu.objects.select_related('loai', 'nha_cung_cap').all()
    
    if query:
        vat_tu_list = vat_tu_list.filter(
            Q(ten_vat_tu__icontains=query) | 
            Q(ma_vat_tu__icontains=query)
        )
        
    context = {
        'section': 'inventory',
        'vat_tu_list': vat_tu_list,
        'query': query,
    }
    return render(request, 'inventory/bao_cao_ton_kho.html', context)

@login_required
def in_phieu_xuat_view(request, phieu_id):
    """
    Tạo trang in cho một Phiếu Xuất Kho.
    """
    phieu = get_object_or_404(
        # Tối ưu hóa: Thêm 'muc_tieu__quan_ly_muc_tieu' để lấy thông tin chỉ huy trưởng
        PhieuXuat.objects.select_related(
            'muc_tieu', 
            'nguoi_xuat', 
            'muc_tieu__quan_ly_muc_tieu'
        ), 
        id=phieu_id
    )
    context = {'phieu': phieu}
    return render(request, 'inventory/print/phieu_xuat.html', context)