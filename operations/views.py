# file: operations/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseBadRequest
# Bỏ dòng import thừa
# from django.contrib.auth.decorators import login_required 
# Import các model cần thiết
from clients.models import MucTieu
from users.models import NhanVien
# Thêm ChamCong vào import
from .models import ViTriChot, CaLamViec, PhanCongCaTruc, BaoCaoSuCo, ChamCong 

# Import form
from .forms import BaoCaoSuCoForm


# --- CÁC VIEW HIỆN TẠI CỦA BẠN (GIỮ NGUYÊN) ---
@login_required
def xep_lich_view(request):
    # ... (giữ nguyên toàn bộ code của hàm này) ...
    all_muc_tieu = MucTieu.objects.all().order_by("ten_muc_tieu")
    current_muc_tieu = None
    nhan_vien_list = []
    schedule_data = []
    days_of_week = [(date.today() + timedelta(days=i)) for i in range(7)]

    muc_tieu_id = request.GET.get("muc_tieu_id")
    if muc_tieu_id:
        current_muc_tieu = get_object_or_404(MucTieu, id=muc_tieu_id)
        nhan_vien_list = (
            NhanVien.objects.filter(
                lich_su_cong_tac__muc_tieu=current_muc_tieu,
                lich_su_cong_tac__la_vi_tri_hien_tai=True,
            )
            .distinct()
            .select_related("user")
        )

        start_date = days_of_week[0]
        end_date = days_of_week[-1]
        phan_congs_in_week = PhanCongCaTruc.objects.filter(
            vi_tri_chot__muc_tieu=current_muc_tieu,
            ngay_truc__range=[start_date, end_date]
        ).select_related('nhan_vien', 'vi_tri_chot', 'ca_lam_viec')

        phan_cong_map = {}
        for pc in phan_congs_in_week:
            key = (pc.vi_tri_chot_id, pc.ca_lam_viec_id, pc.ngay_truc)
            phan_cong_map[key] = pc

        vi_tri_chots = ViTriChot.objects.filter(muc_tieu=current_muc_tieu)
        ca_lam_viecs = CaLamViec.objects.all()

        for vi_tri in vi_tri_chots:
            for ca in ca_lam_viecs:
                lich_truc_theo_ngay = {}
                for day in days_of_week:
                    phan_cong = phan_cong_map.get((vi_tri.id, ca.id, day))
                    lich_truc_theo_ngay[day] = phan_cong
                
                schedule_data.append({
                    "vi_tri": vi_tri,
                    "ca": ca,
                    "lich_truc_theo_ngay": lich_truc_theo_ngay,
                })

    context = {
        "all_muc_tieu": all_muc_tieu,
        "current_muc_tieu": current_muc_tieu,
        "nhan_vien_list": nhan_vien_list,
        "schedule_data": schedule_data,
        "days_of_week": days_of_week,
        "section": "xep_lich",
    }
    return render(request, "operations/xep_lich.html", context)

# ... (Các view xep_lich, chi_tiet_ca, luu_ca... giữ nguyên) ...
@login_required
def chi_tiet_ca(request, phan_cong_id):
    phan_cong = get_object_or_404(
        PhanCongCaTruc.objects.select_related(
            "nhan_vien", "vi_tri_chot", "vi_tri_chot__muc_tieu", "ca_lam_viec"
        ),
        id=phan_cong_id,
    )
    context = {"phan_cong": phan_cong}
    return render(request, "operations/partials/chi_tiet_ca.html", context)


@login_required
def them_ca_form_view(request, vi_tri_id, ca_id, ngay):
    vi_tri = get_object_or_404(ViTriChot, id=vi_tri_id)
    ca = get_object_or_404(CaLamViec, id=ca_id)
    nhan_vien_list = NhanVien.objects.filter(
        lich_su_cong_tac__muc_tieu=vi_tri.muc_tieu,
        lich_su_cong_tac__la_vi_tri_hien_tai=True,
    ).distinct()
    context = {
        "vi_tri": vi_tri,
        "ca": ca,
        "ngay_truc": ngay,
        "nhan_vien_list": nhan_vien_list,
    }
    return render(request, "operations/partials/them_ca_form.html", context)


@login_required
def luu_ca_view(request):
    if request.method == "POST":
        nhan_vien_id = request.POST.get("nhan_vien_id")
        vi_tri_id = request.POST.get("vi_tri_id")
        ca_id = request.POST.get("ca_id")
        ngay_truc_str = request.POST.get("ngay_truc")
        old_phan_cong_id = request.POST.get("delete_old")
        if old_phan_cong_id:
            PhanCongCaTruc.objects.filter(id=old_phan_cong_id).delete()
        if nhan_vien_id:
            phan_cong = PhanCongCaTruc.objects.create(
                nhan_vien_id=nhan_vien_id,
                vi_tri_chot_id=vi_tri_id,
                ca_lam_viec_id=ca_id,
                ngay_truc=ngay_truc_str,
            )
        else:
            phan_cong = None
        context = {
            "phan_cong": phan_cong,
            "vi_tri": get_object_or_404(ViTriChot, id=vi_tri_id),
            "ca": get_object_or_404(CaLamViec, id=ca_id),
            "day": date.fromisoformat(ngay_truc_str),
        }
        return render(request, "operations/partials/ca_truc_cell.html", context)
    return HttpResponseBadRequest("Yêu cầu không hợp lệ")


@login_required
def sua_ca_form_view(request, phan_cong_id):
    phan_cong = get_object_or_404(PhanCongCaTruc, id=phan_cong_id)
    nhan_vien_list = NhanVien.objects.filter(
        lich_su_cong_tac__muc_tieu=phan_cong.vi_tri_chot.muc_tieu,
        lich_su_cong_tac__la_vi_tri_hien_tai=True,
    ).distinct()
    context = {"phan_cong": phan_cong, "nhan_vien_list": nhan_vien_list}
    return render(request, "operations/partials/sua_ca_form.html", context)


@login_required
def xoa_ca_view(request, phan_cong_id):
    phan_cong = get_object_or_404(PhanCongCaTruc, id=phan_cong_id)
    if request.method == "POST":
        vi_tri = phan_cong.vi_tri_chot
        ca = phan_cong.ca_lam_viec
        day = phan_cong.ngay_truc
        phan_cong.delete()
        context = {"phan_cong": None, "vi_tri": vi_tri, "ca": ca, "day": day}
        return render(request, "operations/partials/ca_truc_cell.html", context)
    return HttpResponseBadRequest("Yêu cầu không hợp lệ")


@login_required
def bao_cao_su_co_mobile_view(request):
    try:
        nhan_vien = request.user.nhanvien
        ca_truc_hien_tai = PhanCongCaTruc.objects.filter(
            nhan_vien=nhan_vien, ngay_truc=timezone.now().date()
        ).latest("ca_lam_viec__gio_bat_dau")
    except (NhanVien.DoesNotExist, PhanCongCaTruc.DoesNotExist):
        ca_truc_hien_tai = None

    if not ca_truc_hien_tai:
        messages.error(request, "Bạn không có ca trực nào được phân công cho hôm nay.")
        return render(request, "operations/mobile/bao_cao_su_co.html", {"form": None})

    initial_data = {}
    if hasattr(nhan_vien, 'quan_ly_truc_tiep') and nhan_vien.quan_ly_truc_tiep:
        initial_data['nguoi_nhan'] = nhan_vien.quan_ly_truc_tiep

    if request.method == "POST":
        form = BaoCaoSuCoForm(request.POST, request.FILES)
        if form.is_valid():
            bao_cao = form.save(commit=False)
            bao_cao.ca_truc = ca_truc_hien_tai
            bao_cao.nguoi_nhan = form.cleaned_data.get('nguoi_nhan')
            bao_cao.save()
            messages.success(request, "Đã gửi báo cáo sự cố thành công!")
            return redirect("operations:bao_cao_su_co")
    else:
        form = BaoCaoSuCoForm(initial=initial_data)

    context = {"form": form, "ca_truc": ca_truc_hien_tai}
    return render(request, "operations/mobile/bao_cao_su_co.html", context)


@login_required
def van_hanh_dashboard_view(request):
    """
    Dashboard dành riêng cho Phòng Vận hành.
    """
    context = {
        'section': 'dashboard_vanhanh',
    }
    return render(request, "operations/dashboard_vanhanh.html", context)


@login_required
def mobile_dashboard(request):
    nhan_vien = request.user.nhanvien
    today = timezone.now().date()
    phan_congs = PhanCongCaTruc.objects.filter(
        nhan_vien=nhan_vien, ngay_truc=today
    ).prefetch_related('chamcong')
    
    ca_truc_hom_nay = phan_congs.order_by('ca_lam_viec__gio_bat_dau').first()

    context = {
        'nhan_vien': nhan_vien,
        'ca_truc_hom_nay': ca_truc_hom_nay,
    }
    return render(request, 'operations/mobile/dashboard.html', context)

# --- CÁC VIEW MỚI CHO CHỨC NĂNG CHECK-IN/CHECK-OUT ---
@login_required
def check_in_view(request, phan_cong_id):
    # Lấy đúng ca trực cần check-in, đảm bảo nó thuộc về user đang đăng nhập
    phan_cong = get_object_or_404(PhanCongCaTruc, id=phan_cong_id, nhan_vien=request.user.nhanvien)
    
    # Lấy hoặc tạo mới đối tượng Chấm công liên quan đến ca trực này
    cham_cong, created = ChamCong.objects.get_or_create(ca_truc=phan_cong)
    
    # Chỉ check-in nếu chưa có
    if not cham_cong.thoi_gian_check_in:
        cham_cong.thoi_gian_check_in = timezone.now()
        cham_cong.save()
        messages.success(request, f"Check-in thành công lúc {cham_cong.thoi_gian_check_in.strftime('%H:%M %d/%m')}.")
    else:
        messages.warning(request, "Bạn đã check-in cho ca này rồi.")

    return redirect('operations:mobile_dashboard')

@login_required
def check_out_view(request, phan_cong_id):
    phan_cong = get_object_or_404(PhanCongCaTruc, id=phan_cong_id, nhan_vien=request.user.nhanvien)
    
    # Lấy hoặc tạo mới đối tượng Chấm công
    cham_cong, created = ChamCong.objects.get_or_create(ca_truc=phan_cong)

    # Chỉ check-out nếu đã check-in và chưa check-out
    if cham_cong.thoi_gian_check_in and not cham_cong.thoi_gian_check_out:
        cham_cong.thoi_gian_check_out = timezone.now()
        cham_cong.save()
        messages.success(request, f"Check-out thành công lúc {cham_cong.thoi_gian_check_out.strftime('%H:%M %d/%m')}.")
    elif not cham_cong.thoi_gian_check_in:
        messages.error(request, "Bạn phải check-in trước khi check-out.")
    else:
        messages.warning(request, "Bạn đã check-out cho ca này rồi.")

    return redirect('operations:mobile_dashboard')