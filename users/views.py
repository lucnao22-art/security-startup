# file: users/views.py
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.template import Context, Template
from weasyprint import HTML
from .models import NhanVien, HopDongLaoDong, QuyetDinh
from pathlib import Path
from django.contrib.auth.decorators import login_required, permission_required
from main.models import CompanyProfile

@login_required
def export_ly_lich_options_view(request, nhan_vien_id):
    nhan_vien = get_object_or_404(NhanVien, pk=nhan_vien_id)
    return render(request, "users/ly_lich_options.html", {"nhan_vien": nhan_vien})

@login_required
# @permission_required('users.view_nhanvien', raise_exception=True)
def export_ly_lich_pdf(request, nhan_vien_id):
    nhan_vien = get_object_or_404(NhanVien, pk=nhan_vien_id)
    options = {
        "bao_gom_anh_the": request.POST.get("bao_gom_anh_the") == "on",
        "bao_gom_thong_tin_ca_nhan": request.POST.get("bao_gom_thong_tin_ca_nhan") == "on",
        "bao_gom_bang_cap": request.POST.get("bao_gom_bang_cap") == "on",
        "bao_gom_lich_su_cong_tac": request.POST.get("bao_gom_lich_su_cong_tac") == "on",
    }
    avatar_uri = ""
    if options["bao_gom_anh_the"] and nhan_vien.anh_the:
        avatar_path = Path(nhan_vien.anh_the.path)
        avatar_uri = avatar_path.as_uri()
    context = {
        "nhan_vien": nhan_vien, "avatar_uri": avatar_uri, "options": options,
        "lich_su_cong_tac": nhan_vien.lich_su_cong_tac.all(),
        "bang_cap": nhan_vien.bang_cap.all(),
    }
    html_string = render_to_string("users/ly_lich_pdf.html", context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri("/")).write_pdf()
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="LLTN_{nhan_vien.ma_nhan_vien}.pdf"'
    return response

def render_document_to_pdf(template_content, context, request):
    """Hàm pomocniczy do renderowania szablonu i generowania PDF."""
    template = Template(template_content)
    html_string = template.render(Context(context))
    
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    return pdf_file

@login_required
def in_hop_dong_view(request, hop_dong_id):
    hop_dong = get_object_or_404(HopDongLaoDong, pk=hop_dong_id)
    nhan_vien = hop_dong.nhan_vien
    cong_ty = CompanyProfile.objects.first()
    
    context = {
        'nhan_vien': nhan_vien,
        'hop_dong': hop_dong,
        'cong_ty': cong_ty,
    }
    
    pdf_file = render_document_to_pdf(hop_dong.mau_hop_dong.noi_dung, context, request)
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="HD_{nhan_vien.ma_nhan_vien}.pdf"'
    return response

@login_required
def in_quyet_dinh_view(request, quyet_dinh_id):
    quyet_dinh = get_object_or_404(QuyetDinh, pk=quyet_dinh_id)
    nhan_vien = quyet_dinh.nhan_vien
    cong_ty = CompanyProfile.objects.first()
    
    context = {
        'nhan_vien': nhan_vien,
        'quyet_dinh': quyet_dinh,
        'cong_ty': cong_ty,
    }
    
    pdf_file = render_document_to_pdf(quyet_dinh.mau_quyet_dinh.noi_dung, context, request)

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="QD_{nhan_vien.ma_nhan_vien}.pdf"'
    return response