# file: operations/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from users.models import NhanVien
from clients.models import MucTieu
from .models import ViTriChot # Sửa lại đây
from .models import PhanCongCaTruc, CaLamViec, ChamCong, BaoCaoSuCo, BaoCaoDeXuat
from inventory.models import CapPhatMucTieu
from datetime import date, timedelta
from django.db.models import Q

@login_required
def chi_tiet_muc_tieu_view(request: HttpRequest, muc_tieu_id: int) -> HttpResponse:
    muc_tieu = get_object_or_404(MucTieu.objects.select_related('chi_huy_truong'), id=muc_tieu_id)
    
    # Lấy danh sách vị trí chốt
    vi_tri_chot_list = ViTriChot.objects.filter(muc_tieu=muc_tieu)
    
    # Lấy danh sách nhân viên đang làm việc tại mục tiêu
    nhan_vien_list = NhanVien.objects.filter(muc_tieu_lam_viec=muc_tieu, trang_thai_lam_viec='CT')
    
    # Lấy danh sách CCDC đã cấp phát
    ccdc_list = CapPhatMucTieu.objects.filter(muc_tieu=muc_tieu).select_related('vat_tu')
    
    # Lấy lịch sử sự cố
    su_co_list = BaoCaoSuCo.objects.filter(ca_truc__vi_tri_chot__muc_tieu=muc_tieu).order_by('-thoi_gian_bao_cao')[:10]

    context = {
        'muc_tieu': muc_tieu,
        'vi_tri_chot_list': vi_tri_chot_list,
        'nhan_vien_list': nhan_vien_list,
        'ccdc_list': ccdc_list,
        'su_co_list': su_co_list,
    }
    return render(request, 'operations/chi_tiet_muc_tieu.html', context)

@login_required
def danh_sach_muc_tieu_view(request: HttpRequest) -> HttpResponse:
    muc_tieu_list = MucTieu.objects.all()
    return render(request, 'operations/danh_sach_muc_tieu.html', {'muc_tieu_list': muc_tieu_list})

@login_required
def chi_tiet_muc_tieu_view(request: HttpRequest, muc_tieu_id: int) -> HttpResponse:
    muc_tieu = get_object_or_404(MucTieu, id=muc_tieu_id)
    # Lấy các thông tin liên quan...
    # (Code để lấy CCDC, lỗi, phản hồi sẽ được thêm sau)
    context = {
        'muc_tieu': muc_tieu,
    }
    return render(request, 'operations/chi_tiet_muc_tieu.html', context)
@login_required
def xep_lich_view(request: HttpRequest) -> HttpResponse:
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    days_of_week = [(start_of_week + timedelta(days=i)) for i in range(7)]
    
    user = request.user
    all_muc_tieu = MucTieu.objects.all()
    if not user.is_superuser:
        try:
            current_nhan_vien = NhanVien.objects.get(user=user)
            all_muc_tieu = MucTieu.objects.filter(chi_huy_truong=current_nhan_vien)
        except NhanVien.DoesNotExist:
            all_muc_tieu = MucTieu.objects.none()

    schedule_data = []
    nhan_vien_san_sang = NhanVien.objects.none()
    current_muc_tieu = None
    
    current_muc_tieu_id = request.GET.get('muc_tieu_id')
    if current_muc_tieu_id:
        current_muc_tieu = get_object_or_404(MucTieu, id=current_muc_tieu_id)
        vi_tri_chot_list = ViTriChot.objects.filter(muc_tieu=current_muc_tieu)
        qs_nhan_vien = NhanVien.objects.filter(muc_tieu_lam_viec=current_muc_tieu, trang_thai_lam_viec='CT')

        lich_truc_trong_tuan = PhanCongCaTruc.objects.filter(
            ngay_truc__range=[start_of_week, days_of_week[-1]],
            vi_tri_chot__muc_tieu=current_muc_tieu
        ).select_related('nhan_vien', 'ca_lam_viec', 'vi_tri_chot')

        nhan_vien_da_co_lich_ids = lich_truc_trong_tuan.values_list('nhan_vien_id', flat=True)
        nhan_vien_san_sang = qs_nhan_vien.exclude(id__in=nhan_vien_da_co_lich_ids)
        
        ca_lam_viec_list = CaLamViec.objects.all()

        for vt in vi_tri_chot_list:
            for ca in ca_lam_viec_list:
                row = {'vi_tri': vt, 'ca': ca, 'lich_truc_theo_ngay': {}}
                for day in days_of_week:
                    phan_cong = lich_truc_trong_tuan.filter(vi_tri_chot=vt, ca_lam_viec=ca, ngay_truc=day).first()
                    row['lich_truc_theo_ngay'][day] = phan_cong
                schedule_data.append(row)

    context = {
        'nhan_vien_list': nhan_vien_san_sang,
        'days_of_week': days_of_week,
        'schedule_data': schedule_data,
        'all_muc_tieu': all_muc_tieu,
        'current_muc_tieu': current_muc_tieu,
    }
    
    return render(request, "operations/xep_lich.html", context)


def them_ca_form_view(request: HttpRequest) -> HttpResponse:
    ngay_truc_str = request.GET.get('ngay')
    ca_lam_viec_id = request.GET.get('ca_id')
    vi_tri_chot_id = request.GET.get('vi_tri_id')

    vi_tri_chot = get_object_or_404(ViTriChot, id=vi_tri_chot_id)
    muc_tieu = vi_tri_chot.muc_tieu

    nhan_vien_ban_trong_ngay_ids = PhanCongCaTruc.objects.filter(ngay_truc=ngay_truc_str).values_list('nhan_vien_id', flat=True)
    danh_sach_nhan_vien = NhanVien.objects.filter(
        muc_tieu_lam_viec=muc_tieu, 
        trang_thai_lam_viec='CT'
    ).exclude(id__in=nhan_vien_ban_trong_ngay_ids)

    context = {
        'danh_sach_nhan_vien': danh_sach_nhan_vien,
        'ngay_truc': ngay_truc_str,
        'ca_lam_viec_id': ca_lam_viec_id,
        'vi_tri_chot_id': vi_tri_chot_id,
    }
    return render(request, "operations/partials/them_ca_form.html", context)


def luu_ca_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        nhan_vien_id = request.POST.get('nhan_vien_id')
        ngay_truc_str = request.POST.get('ngay_truc')
        ca_lam_viec_id = request.POST.get('ca_lam_viec_id')
        vi_tri_chot_id = request.POST.get('vi_tri_chot_id')
        
        if nhan_vien_id:
            nhan_vien = get_object_or_404(NhanVien, id=nhan_vien_id)
            ca_lam_viec = get_object_or_404(CaLamViec, id=ca_lam_viec_id)
            vi_tri_chot = get_object_or_404(ViTriChot, id=vi_tri_chot_id)

            PhanCongCaTruc.objects.update_or_create(
                ngay_truc=ngay_truc_str,
                ca_lam_viec=ca_lam_viec,
                vi_tri_chot=vi_tri_chot,
                defaults={'nhan_vien': nhan_vien}
            )
            
    response = HttpResponse(status=204)
    response['HX-Refresh'] = 'true'
    return response

def sua_ca_form_view(request: HttpRequest, phan_cong_id: int) -> HttpResponse:
    phan_cong = get_object_or_404(PhanCongCaTruc, id=phan_cong_id)
    muc_tieu = phan_cong.vi_tri_chot.muc_tieu
    danh_sach_nhan_vien = NhanVien.objects.filter(muc_tieu_lam_viec=muc_tieu, trang_thai_lam_viec='CT')
    
    context = {
        'phan_cong': phan_cong,
        'danh_sach_nhan_vien': danh_sach_nhan_vien,
    }
    return render(request, 'operations/partials/sua_ca_form.html', context)

def cap_nhat_ca_view(request: HttpRequest, phan_cong_id: int) -> HttpResponse:
    if request.method == 'POST':
        phan_cong = get_object_or_404(PhanCongCaTruc, id=phan_cong_id)
        nhan_vien_moi_id = request.POST.get('nhan_vien_id')
        
        if nhan_vien_moi_id:
            nhan_vien_moi = get_object_or_404(NhanVien, id=nhan_vien_moi_id)
            phan_cong.nhan_vien = nhan_vien_moi
            phan_cong.save()
            
    response = HttpResponse(status=204)
    response['HX-Refresh'] = 'true'
    return response

def xoa_ca_view(request: HttpRequest, phan_cong_id: int) -> HttpResponse:
    if request.method == 'POST':
        phan_cong = get_object_or_404(PhanCongCaTruc, id=phan_cong_id)
        phan_cong.delete()
    response = HttpResponse(status=204)
    response['HX-Refresh'] = 'true'
    return response

def chi_tiet_ca_view(request: HttpRequest, phan_cong_id: int) -> HttpResponse:
    phan_cong = get_object_or_404(PhanCongCaTruc.objects.select_related('nhan_vien', 'vi_tri_chot', 'ca_lam_viec'), id=phan_cong_id)
    return render(request, 'operations/partials/chi_tiet_ca.html', {'phan_cong': phan_cong})

def tim_kiem_nhan_vien_view(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('q', '')
    lich_truc = PhanCongCaTruc.objects.values_list('nhan_vien_id', flat=True)
    results = NhanVien.objects.filter(
        Q(ho_ten__icontains=query) | Q(ma_nhan_vien__icontains=query),
        trang_thai_lam_viec='CT'
    ).exclude(id__in=lich_truc)
    
    return render(request, 'operations/partials/danh_sach_nhan_vien.html', {'nhan_vien_list': results})

# ----- CÁC HÀM CHO GIAO DIỆN DI ĐỘNG -----

def mobile_login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                if user.is_superuser:
                    return redirect('/admin/')

                try:
                    nhan_vien = NhanVien.objects.get(user=user)
                    
                    if nhan_vien.phong_ban and nhan_vien.phong_ban.ten_phong_ban == 'Ban Giám đốc':
                        return redirect('dashboard:main')
                        
                    quan_ly_roles = [
                        NhanVien.ChucVu.CHI_HUY_TRUONG,
                        NhanVien.ChucVu.QUAN_LY_VUNG,
                        NhanVien.ChucVu.TRUONG_PHONG
                    ]
                    if nhan_vien.chuc_vu in quan_ly_roles:
                        return redirect('operations:xep-lich')

                except NhanVien.DoesNotExist:
                    return redirect('operations:mobile-dashboard')
                
                return redirect('operations:mobile-dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'operations/mobile/login.html', {'form': form})

@login_required(login_url='/ops/mobile/login/')
def mobile_dashboard_view(request: HttpRequest) -> HttpResponse:
    try:
        nhan_vien = NhanVien.objects.get(user=request.user)
        today = date.today()
        one_week_later = today + timedelta(days=7)
        
        ca_truc_hom_nay = PhanCongCaTruc.objects.filter(
            nhan_vien=nhan_vien,
            ngay_truc=today
        ).first()
        
        lich_truc_tuan_toi = PhanCongCaTruc.objects.filter(
            nhan_vien=nhan_vien,
            ngay_truc__range=[today, one_week_later]
        ).order_by('ngay_truc', 'ca_lam_viec__gio_bat_dau')
        
        cham_cong = None
        if ca_truc_hom_nay:
            cham_cong = ChamCong.objects.filter(ca_truc=ca_truc_hom_nay).first()

    except NhanVien.DoesNotExist:
        nhan_vien = None
        ca_truc_hom_nay = None
        cham_cong = None
        lich_truc_tuan_toi = []

    context = {
        'nhan_vien': nhan_vien,
        'ca_truc_hom_nay': ca_truc_hom_nay,
        'cham_cong': cham_cong,
        'lich_truc_tuan_toi': lich_truc_tuan_toi,
    }
    return render(request, 'operations/mobile/dashboard.html', context)

@login_required(login_url='/ops/mobile/login/')
def mobile_cham_cong_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        ca_truc_id = request.POST.get('ca_truc_id')
        loai_cham_cong = request.POST.get('loai_cham_cong')
        anh_selfie = request.FILES.get('anh_selfie')
        
        ca_truc = get_object_or_404(PhanCongCaTruc, id=ca_truc_id)
        
        cham_cong, created = ChamCong.objects.get_or_create(ca_truc=ca_truc)
        
        if loai_cham_cong == 'check_in':
            cham_cong.thoi_gian_check_in = timezone.now()
            cham_cong.anh_check_in = anh_selfie
        elif loai_cham_cong == 'check_out':
            cham_cong.thoi_gian_check_out = timezone.now()
            cham_cong.anh_check_out = anh_selfie
            
        cham_cong.save()

    return redirect('operations:mobile-dashboard')

@login_required(login_url='/ops/mobile/login/')
def mobile_bao_cao_su_co_view(request: HttpRequest) -> HttpResponse:
    ca_truc_hom_nay = None
    try:
        nhan_vien = NhanVien.objects.get(user=request.user)
        ca_truc_hom_nay = PhanCongCaTruc.objects.filter(
            nhan_vien=nhan_vien, 
            ngay_truc=date.today()
        ).first()
    except NhanVien.DoesNotExist:
        pass

    if request.method == 'POST' and ca_truc_hom_nay:
        tieu_de = request.POST.get('tieu_de')
        noi_dung = request.POST.get('noi_dung')
        hinh_anh = request.FILES.get('hinh_anh')
        
        BaoCaoSuCo.objects.create(
            ca_truc=ca_truc_hom_nay,
            tieu_de=tieu_de,
            noi_dung=noi_dung,
            hinh_anh=hinh_anh
        )
        return redirect('operations:mobile-dashboard')

    return render(request, 'operations/mobile/bao_cao_su_co.html', {'ca_truc_hom_nay': ca_truc_hom_nay})

@login_required(login_url='/ops/mobile/login/')
def mobile_bao_cao_de_xuat_view(request: HttpRequest) -> HttpResponse:
    try:
        nhan_vien = NhanVien.objects.get(user=request.user)
    except NhanVien.DoesNotExist:
        return redirect('operations:mobile-login')

    if request.method == 'POST':
        loai_bao_cao = request.POST.get('loai_bao_cao')
        tieu_de = request.POST.get('tieu_de')
        noi_dung = request.POST.get('noi_dung')
        
        BaoCaoDeXuat.objects.create(
            nhan_vien=nhan_vien,
            loai_bao_cao=loai_bao_cao,
            tieu_de=tieu_de,
            noi_dung=noi_dung,
        )
        return redirect('operations:mobile-dashboard')

    context = { 'loai_bao_cao_choices': BaoCaoDeXuat.LoaiBaoCao.choices }
    return render(request, 'operations/mobile/bao_cao_de_xuat.html', context)

def mobile_logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('operations:mobile-login')
@login_required
def danh_sach_muc_tieu_view(request: HttpRequest) -> HttpResponse:
    muc_tieu_list = MucTieu.objects.all()
    return render(request, 'operations/danh_sach_muc_tieu.html', {'muc_tieu_list': muc_tieu_list})

@login_required
def chi_tiet_muc_tieu_view(request: HttpRequest, muc_tieu_id: int) -> HttpResponse:
    muc_tieu = get_object_or_404(MucTieu.objects.select_related('chi_huy_truong'), id=muc_tieu_id)
    
    # Lấy danh sách vị trí chốt
    vi_tri_chot_list = ViTriChot.objects.filter(muc_tieu=muc_tieu)
    
    # Lấy danh sách nhân viên đang làm việc tại mục tiêu
    nhan_vien_list = NhanVien.objects.filter(muc_tieu_lam_viec=muc_tieu, trang_thai_lam_viec='CT')
    
    # Lấy danh sách CCDC đã cấp phát cho mục tiêu
    ccdc_list = CapPhatMucTieu.objects.filter(muc_tieu=muc_tieu).select_related('vat_tu')
    
    # Lấy lịch sử sự cố của mục tiêu (10 sự cố gần nhất)
    su_co_list = BaoCaoSuCo.objects.filter(ca_truc__vi_tri_chot__muc_tieu=muc_tieu).order_by('-thoi_gian_bao_cao')[:10]

    context = {
        'muc_tieu': muc_tieu,
        'vi_tri_chot_list': vi_tri_chot_list,
        'nhan_vien_list': nhan_vien_list,
        'ccdc_list': ccdc_list,
        'su_co_list': su_co_list,
    }
    return render(request, 'operations/chi_tiet_muc_tieu.html', context)