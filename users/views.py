# file: users/views.py
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import NhanVien
from pathlib import Path

def export_ly_lich_options_view(request, nhan_vien_id):
    """
    Hiển thị form cho người dùng chọn các thông tin cần xuất.
    """
    nhan_vien = get_object_or_404(NhanVien, pk=nhan_vien_id)
    return render(request, 'users/ly_lich_options.html', {'nhan_vien': nhan_vien})

def export_ly_lich_pdf(request, nhan_vien_id):
    """
    Tạo file PDF dựa trên các tùy chọn được gửi từ form.
    """
    nhan_vien = get_object_or_404(NhanVien, pk=nhan_vien_id)
    
    # Lấy các tùy chọn từ form
    options = {
        'bao_gom_anh_the': request.POST.get('bao_gom_anh_the') == 'on',
        'bao_gom_thong_tin_ca_nhan': request.POST.get('bao_gom_thong_tin_ca_nhan') == 'on',
        'bao_gom_bang_cap': request.POST.get('bao_gom_bang_cap') == 'on',
        'bao_gom_lich_su_cong_tac': request.POST.get('bao_gom_lich_su_cong_tac') == 'on',
    }

    avatar_uri = ''
    if options['bao_gom_anh_the'] and nhan_vien.anh_the:
        avatar_path = Path(nhan_vien.anh_the.path)
        avatar_uri = avatar_path.as_uri()

    context = {
        'nhan_vien': nhan_vien,
        'avatar_uri': avatar_uri,
        'options': options,
    }
    
    html_string = render_to_string('users/ly_lich_pdf.html', context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="LLTN_{nhan_vien.ma_nhan_vien}.pdf"'
    
    return response