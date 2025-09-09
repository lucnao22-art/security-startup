# file: operations/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta, datetime
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.db.models import Q, F  # SỬA LỖI: Thêm import F
import qrcode
from io import BytesIO
import base64

# Import các model và form cần thiết
from clients.models import MucTieu
from users.models import NhanVien
from .models import ViTriChot, CaLamViec, PhanCongCaTruc, BaoCaoSuCo, ChamCong
from .forms import BaoCaoSuCoForm, CheckInForm, CheckOutForm


# ==============================================================================
# VIEWS CHO GIAO DIỆN WEB ADMIN
# ==============================================================================
# (Các view cho web admin không thay đổi)
@login_required
def xep_lich_view(request):
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
            phan_cong, _ = PhanCongCaTruc.objects.update_or_create(
                vi_tri_chot_id=vi_tri_id,
                ca_lam_viec_id=ca_id,
                ngay_truc=ngay_truc_str,
                defaults={'nhan_vien_id': nhan_vien_id}
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
def van_hanh_dashboard_view(request):
    context = {
        'section': 'dashboard_vanhanh',
    }
    return render(request, "operations/dashboard_vanhanh.html", context)


# ==============================================================================
# VIEWS CHO GIAO DIỆN MOBILE (ĐÃ FIX LỖI & TỐI ƯU)
# ==============================================================================

@login_required
def mobile_dashboard(request):
    try:
        nhan_vien = request.user.nhanvien
    except NhanVien.DoesNotExist:
        messages.error(request, "Tài khoản của bạn chưa được liên kết với hồ sơ nhân viên.")
        return render(request, 'operations/mobile/dashboard.html', {'error': True})

    now = timezone.now()
    today = now.date()
    yesterday = today - timedelta(days=1)

    # === SỬA LỖI LOGIC TÌM CA TRỰC HIỆN TẠI (XỬ LÝ CA ĐÊM) ===
    phan_cong_qs = PhanCongCaTruc.objects.filter(
        Q(nhan_vien=nhan_vien) & 
        (
            Q(ngay_truc=today) | 
            (Q(ngay_truc=yesterday) & Q(ca_lam_viec__gio_ket_thuc__lt=F('ca_lam_viec__gio_bat_dau')))
        )
    ).select_related(
        'chamcong', 'ca_lam_viec', 'vi_tri_chot', 'vi_tri_chot__muc_tieu'
    ).order_by('-ngay_truc', '-ca_lam_viec__gio_bat_dau')

    ca_truc_hien_tai = None
    for pc in phan_cong_qs:
        start_datetime = datetime.combine(pc.ngay_truc, pc.ca_lam_viec.gio_bat_dau)
        
        end_date = pc.ngay_truc
        if pc.ca_lam_viec.gio_ket_thuc < pc.ca_lam_viec.gio_bat_dau:
            end_date += timedelta(days=1)
        end_datetime = datetime.combine(end_date, pc.ca_lam_viec.gio_ket_thuc)

        start_datetime = timezone.make_aware(start_datetime)
        end_datetime = timezone.make_aware(end_datetime)

        if start_datetime <= now < end_datetime:
            ca_truc_hien_tai = pc
            break
    
    hour = now.hour
    loi_chao = "Chào bạn,"
    if 5 <= hour < 12: loi_chao = "Chào buổi sáng,"
    elif 12 <= hour < 18: loi_chao = "Chào buổi chiều,"
    else: loi_chao = "Chào buổi tối,"

    qr_data = f"NV:{nhan_vien.ma_nhan_vien};TEN:{nhan_vien.ho_ten}"
    img = qrcode.make(qr_data)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    context = {
        'nhan_vien': nhan_vien,
        'ca_truc_hien_tai': ca_truc_hien_tai,
        'loi_chao': loi_chao,
        'qr_code_base64': qr_code_base64,
        'checkin_form': CheckInForm(),
        'checkout_form': CheckOutForm(),
    }
    return render(request, 'operations/mobile/dashboard.html', context)


@login_required
def mobile_lich_truc_view(request):
    nhan_vien = get_object_or_404(NhanVien, user=request.user)
    today = timezone.now().date()
    sap_toi_7_ca = PhanCongCaTruc.objects.filter(
        nhan_vien=nhan_vien, 
        ngay_truc__gte=today
    ).select_related(
        'ca_lam_viec', 
        'vi_tri_chot__muc_tieu'
    ).order_by('ngay_truc', 'ca_lam_viec__gio_bat_dau')[:7]
    context = {'danh_sach_ca_truc': sap_toi_7_ca}
    return render(request, 'operations/mobile/lich_truc.html', context)


@login_required
def bao_cao_su_co_mobile_view(request):
    nhan_vien = get_object_or_404(NhanVien, user=request.user)
    
    # Sử dụng lại logic tìm ca trực từ dashboard để đảm bảo tính nhất quán
    now = timezone.now()
    today = now.date()
    yesterday = today - timedelta(days=1)
    phan_cong_qs = PhanCongCaTruc.objects.filter(
        Q(nhan_vien=nhan_vien) & 
        (Q(ngay_truc=today) | 
         (Q(ngay_truc=yesterday) & Q(ca_lam_viec__gio_ket_thuc__lt=F('ca_lam_viec__gio_bat_dau'))))
    ).order_by('-ngay_truc', '-ca_lam_viec__gio_bat_dau')

    ca_truc_hien_tai = None
    for pc in phan_cong_qs:
        start_datetime = timezone.make_aware(datetime.combine(pc.ngay_truc, pc.ca_lam_viec.gio_bat_dau))
        end_date = pc.ngay_truc + timedelta(days=1) if pc.ca_lam_viec.gio_ket_thuc < pc.ca_lam_viec.gio_bat_dau else pc.ngay_truc
        end_datetime = timezone.make_aware(datetime.combine(end_date, pc.ca_lam_viec.gio_ket_thuc))
        if start_datetime <= now < end_datetime:
            ca_truc_hien_tai = pc
            break

    if not ca_truc_hien_tai:
        messages.error(request, "Bạn không trong ca trực nào để gửi báo cáo.")
        return render(request, "operations/mobile/bao_cao_su_co.html", {"form": None})

    if request.method == "POST":
        form = BaoCaoSuCoForm(request.POST, request.FILES)
        if form.is_valid():
            bao_cao = form.save(commit=False)
            bao_cao.ca_truc = ca_truc_hien_tai
            bao_cao.save()
            messages.success(request, "Đã gửi báo cáo sự cố thành công!")
            return redirect("operations:bao_cao_su_co")
    else:
        form = BaoCaoSuCoForm()

    context = {"form": form, "ca_truc": ca_truc_hien_tai}
    return render(request, "operations/mobile/bao_cao_su_co.html", context)


@login_required
def check_in_view(request, phan_cong_id):
    if request.method == 'POST':
        phan_cong = get_object_or_404(PhanCongCaTruc, id=phan_cong_id, nhan_vien=request.user.nhanvien)
        cham_cong, created = ChamCong.objects.get_or_create(ca_truc=phan_cong)
        
        form = CheckInForm(request.POST, request.FILES, instance=cham_cong)
        if form.is_valid():
            if not cham_cong.thoi_gian_check_in:
                cham_cong.thoi_gian_check_in = timezone.now()
                form.save()
                messages.success(request, f"Check-in thành công lúc {cham_cong.thoi_gian_check_in.strftime('%H:%M %d/%m')}.")
            else:
                messages.warning(request, "Bạn đã check-in cho ca này rồi.")
        else:
            # Lấy lỗi cụ thể từ form để thông báo cho người dùng
            error_msg = form.errors.get('anh_check_in', ["Vui lòng chụp ảnh selfie để check-in."])[0]
            messages.error(request, error_msg)

    return redirect('operations:mobile_dashboard')


@login_required
def check_out_view(request, phan_cong_id):
    if request.method == 'POST':
        phan_cong = get_object_or_404(PhanCongCaTruc, id=phan_cong_id, nhan_vien=request.user.nhanvien)
        
        try:
            cham_cong = ChamCong.objects.get(ca_truc=phan_cong)
        except ChamCong.DoesNotExist:
            messages.error(request, "Bạn phải check-in trước khi check-out.")
            return redirect('operations:mobile_dashboard')

        form = CheckOutForm(request.POST, request.FILES, instance=cham_cong)
        if form.is_valid():
            if cham_cong.thoi_gian_check_in and not cham_cong.thoi_gian_check_out:
                cham_cong.thoi_gian_check_out = timezone.now()
                form.save()
                messages.success(request, f"Check-out thành công lúc {cham_cong.thoi_gian_check_out.strftime('%H:%M %d/%m')}.")
            elif not cham_cong.thoi_gian_check_in:
                 messages.error(request, "Bạn phải check-in trước khi check-out.")
            else:
                messages.warning(request, "Bạn đã check-out cho ca này rồi.")
        else:
            error_msg = form.errors.get('anh_check_out', ["Vui lòng chụp ảnh selfie để check-out."])[0]
            messages.error(request, error_msg)

    return redirect('operations:mobile_dashboard')