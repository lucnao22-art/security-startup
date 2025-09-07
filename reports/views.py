# file: reports/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, time
from django.db.models import Sum, F, ExpressionWrapper, fields
from collections import defaultdict
import calendar

from users.models import NhanVien
from operations.models import ChamCong
from clients.models import MucTieu

@login_required
def bang_cham_cong_ca_nhan_view(request):
    nhan_vien_list = NhanVien.objects.filter(user__is_active=True).order_by('ho_ten')
    selected_nhan_vien = None
    cham_cong_data = []
    summary_data = {}

    nhan_vien_id = request.GET.get('nhan_vien_id')
    thang_str = request.GET.get('thang', str(timezone.now().month))
    nam_str = request.GET.get('nam', str(timezone.now().year))

    if nhan_vien_id and thang_str and nam_str:
        try:
            selected_nhan_vien = NhanVien.objects.get(id=nhan_vien_id)
            thang = int(thang_str)
            nam = int(nam_str)
            
            cham_congs = ChamCong.objects.filter(
                ca_truc__nhan_vien=selected_nhan_vien,
                ca_truc__ngay_truc__month=thang,
                ca_truc__ngay_truc__year=nam,
                thoi_gian_check_in__isnull=False,
                thoi_gian_check_out__isnull=False,
            ).select_related(
                'ca_truc__ca_lam_viec', 
                'ca_truc__vi_tri_chot__muc_tieu'
            ).order_by('ca_truc__ngay_truc')

            total_duration = timezone.timedelta()
            so_lan_di_tre = 0
            so_lan_ve_som = 0
            gio_lam_theo_muc_tieu = defaultdict(timezone.timedelta)
            
            for cc in cham_congs:
                duration = cc.thoi_gian_check_out - cc.thoi_gian_check_in
                total_duration += duration
                muc_tieu_ten = cc.ca_truc.vi_tri_chot.muc_tieu.ten_muc_tieu
                gio_lam_theo_muc_tieu[muc_tieu_ten] += duration

                trang_thai = "Đúng giờ"
                if cc.thoi_gian_check_in.time() > cc.ca_truc.ca_lam_viec.gio_bat_dau:
                    trang_thai = "Đi trễ"
                    so_lan_di_tre += 1
                if cc.thoi_gian_check_out.time() < cc.ca_truc.ca_lam_viec.gio_ket_thuc:
                    trang_thai = "Về sớm"
                    so_lan_ve_som += 1

                cham_cong_data.append({
                    'ngay': cc.ca_truc.ngay_truc,
                    'thu': cc.ca_truc.ngay_truc.strftime('%A'),
                    'ca_truc': cc.ca_truc.ca_lam_viec.ten_ca,
                    'muc_tieu': muc_tieu_ten,
                    'vi_tri': cc.ca_truc.vi_tri_chot.ten_vi_tri,
                    'check_in': cc.thoi_gian_check_in,
                    'check_out': cc.thoi_gian_check_out,
                    'tong_gio_lam': duration,
                    'trang_thai': trang_thai,
                })
            
            # --- NÂNG CẤP: Làm tròn giờ trước khi gửi sang template ---
            summary_data = {
                'tong_ngay_cong': len(cham_congs),
                'tong_gio_lam': f"{total_duration.total_seconds() / 3600:.2f}",
                'so_lan_di_tre': so_lan_di_tre,
                'so_lan_ve_som': so_lan_ve_som,
                'gio_lam_theo_muc_tieu': {
                    muc_tieu: f"{tong_gio.total_seconds() / 3600:.2f}"
                    for muc_tieu, tong_gio in gio_lam_theo_muc_tieu.items()
                }
            }

        except (ValueError, NhanVien.DoesNotExist):
            pass

    context = {
        'section': 'reports',
        'nhan_vien_list': nhan_vien_list,
        'selected_nhan_vien': selected_nhan_vien,
        'cham_cong_data': cham_cong_data,
        'summary_data': summary_data,
        'selected_thang': int(thang_str),
        'selected_nam': int(nam_str),
        'thang_range': range(1, 13),
        'nam_range': range(timezone.now().year - 2, timezone.now().year + 1)
    }
    return render(request, 'reports/cham_cong_ca_nhan.html', context)


@login_required
def bang_cham_cong_muc_tieu_view(request):
    muc_tieu_list = MucTieu.objects.all()
    selected_muc_tieu = None
    report_data = []
    summary_data = {}

    muc_tieu_id = request.GET.get('muc_tieu_id')
    thang_str = request.GET.get('thang', str(timezone.now().month))
    nam_str = request.GET.get('nam', str(timezone.now().year))

    if muc_tieu_id and thang_str and nam_str:
        try:
            selected_muc_tieu = MucTieu.objects.get(id=muc_tieu_id)
            thang = int(thang_str)
            nam = int(nam_str)
            
            _, num_days = calendar.monthrange(nam, thang)

            cham_congs = ChamCong.objects.filter(
                ca_truc__vi_tri_chot__muc_tieu=selected_muc_tieu,
                ca_truc__ngay_truc__month=thang,
                ca_truc__ngay_truc__year=nam,
                thoi_gian_check_in__isnull=False,
                thoi_gian_check_out__isnull=False,
            ).annotate(
                duration=ExpressionWrapper(F('thoi_gian_check_out') - F('thoi_gian_check_in'), output_field=fields.DurationField())
            ).select_related('ca_truc__nhan_vien', 'ca_truc__vi_tri_chot', 'ca_truc__ca_lam_viec')

            tong_gio_toan_muc_tieu = cham_congs.aggregate(total=Sum('duration'))['total'] or timezone.timedelta()
            gio_theo_vitri = defaultdict(timezone.timedelta)
            canh_bao_vuot_24h = {}

            gio_theo_vitri_ngay = defaultdict(timezone.timedelta)
            for cc in cham_congs:
                gio_theo_vitri[cc.ca_truc.vi_tri_chot.ten_vi_tri] += cc.duration
                key = (cc.ca_truc.vi_tri_chot.ten_vi_tri, cc.ca_truc.ngay_truc)
                gio_theo_vitri_ngay[key] += cc.duration
            
            for (vitri, ngay), tong_gio in gio_theo_vitri_ngay.items():
                if tong_gio.total_seconds() > 24 * 3600:
                    canh_bao_vuot_24h[f"{vitri} - {ngay.strftime('%d/%m')}"] = f"{tong_gio.total_seconds() / 3600:.1f}h"

            so_vi_tri = selected_muc_tieu.vi_tri_chot.count()
            gio_dinh_muc = timezone.timedelta(hours=so_vi_tri * 24 * num_days)
            canh_bao_vuot_dinhmuc = tong_gio_toan_muc_tieu > gio_dinh_muc

            # --- NÂNG CẤP: Làm tròn giờ trước khi gửi sang template ---
            summary_data = {
                'tong_gio_hoat_dong': f"{tong_gio_toan_muc_tieu.total_seconds() / 3600:.2f}",
                'gio_dinh_muc': f"{gio_dinh_muc.total_seconds() / 3600:.2f}",
                'gio_theo_vitri': {
                    vitri: f"{tong_gio.total_seconds() / 3600:.2f}"
                    for vitri, tong_gio in gio_theo_vitri.items()
                },
                'canh_bao_vuot_24h': canh_bao_vuot_24h,
                'canh_bao_vuot_dinhmuc': canh_bao_vuot_dinhmuc,
            }
            report_data = cham_congs.order_by('ca_truc__ngay_truc', 'ca_truc__vi_tri_chot__ten_vi_tri', 'ca_truc__ca_lam_viec__gio_bat_dau')

        except (ValueError, MucTieu.DoesNotExist):
            pass

    context = {
        'section': 'reports',
        'muc_tieu_list': muc_tieu_list,
        'selected_muc_tieu': selected_muc_tieu,
        'report_data': report_data,
        'summary_data': summary_data,
        'selected_thang': int(thang_str),
        'selected_nam': int(nam_str),
        'thang_range': range(1, 13),
        'nam_range': range(timezone.now().year - 2, timezone.now().year + 1)
    }
    return render(request, 'reports/cham_cong_muc_tieu.html', context)