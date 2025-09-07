# file: dashboard/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import json

# Import các model cần thiết từ các app khác
from users.models import NhanVien
from clients.models import KhachHangTiemNang
from operations.models import BaoCaoSuCo, PhanCongCaTruc
from inspection.models import LuotTuanTra

@login_required
def dashboard_view(request):
    # --- DỮ LIỆU CHO CÁC THẺ KPI ---
    total_nhan_vien = NhanVien.objects.filter(user__is_active=True).count()
    
    # --- PHẦN SỬA LỖI: Bỏ filter theo 'trang_thai' không tồn tại ---
    total_khach_hang = KhachHangTiemNang.objects.count()
    
    thirty_days_ago = timezone.now() - timedelta(days=30)
    su_co_gan_day = BaoCaoSuCo.objects.filter(thoi_gian_bao_cao__gte=thirty_days_ago).count()

    ca_truc_hom_nay = PhanCongCaTruc.objects.filter(ngay_truc=timezone.now().date()).count()

    # --- DỮ LIỆU CHO BẢNG "SỰ CỐ GẦN ĐÂY" ---
    cac_su_co_moi = BaoCaoSuCo.objects.select_related(
        'ca_truc__nhan_vien', 
        'ca_truc__vi_tri_chot__muc_tieu'
    ).order_by('-thoi_gian_bao_cao')[:5]

    # --- DỮ LIỆU CHO BIỂU ĐỒ HOẠT ĐỘNG 7 NGÀY GẦN NHẤT ---
    labels = []
    tuan_tra_data = []
    su_co_data = []

    for i in range(6, -1, -1):
        day = timezone.now().date() - timedelta(days=i)
        labels.append(day.strftime('%d/%m'))
        
        completed_patrols = LuotTuanTra.objects.filter(
            thoi_gian_bat_dau__date=day, 
            trang_thai='COMPLETED'
        ).count()
        tuan_tra_data.append(completed_patrols)
        
        incidents = BaoCaoSuCo.objects.filter(thoi_gian_bao_cao__date=day).count()
        su_co_data.append(incidents)

    context = {
        'section': 'dashboard',
        'total_nhan_vien': total_nhan_vien,
        'total_khach_hang': total_khach_hang,
        'su_co_gan_day': su_co_gan_day,
        'ca_truc_hom_nay': ca_truc_hom_nay,
        'cac_su_co_moi': cac_su_co_moi,
        'chart_labels': json.dumps(labels),
        'tuan_tra_data': json.dumps(tuan_tra_data),
        'su_co_data': json.dumps(su_co_data),
    }
    return render(request, "dashboard/main.html", context)