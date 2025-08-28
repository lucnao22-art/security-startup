# file: dashboard/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from users.models import NhanVien
from clients.models import MucTieu
from operations.models import BaoCaoSuCo
from datetime import timedelta
import json

@login_required
def dashboard_view(request):
    context = {}
    user = request.user
    
    # 1. Lấy hồ sơ nhân viên (nếu có)
    try:
        current_nhan_vien = NhanVien.objects.get(user=user)
    except NhanVien.DoesNotExist:
        current_nhan_vien = None

    # 2. Lấy dữ liệu cho Ban Giám đốc và Superuser
    if user.is_superuser or (current_nhan_vien and current_nhan_vien.phong_ban and current_nhan_vien.phong_ban.ten_phong_ban == 'Ban Giám đốc'):
        # Các chỉ số KPI chính
        so_luong_nhan_vien = NhanVien.objects.filter(trang_thai_lam_viec='CT').count()
        so_luong_muc_tieu = MucTieu.objects.count()
        now = timezone.now()
        start_of_month = now.replace(day=1)
        so_luong_su_co_thang_nay = BaoCaoSuCo.objects.filter(thoi_gian_bao_cao__gte=start_of_month).count()
        so_su_co_moi = BaoCaoSuCo.objects.filter(trang_thai='MOI').count()

        # Dữ liệu cho biểu đồ
        seven_days_ago = now - timedelta(days=7)
        incidents_by_day = (
            BaoCaoSuCo.objects.filter(thoi_gian_bao_cao__gte=seven_days_ago)
            .annotate(date=TruncDate('thoi_gian_bao_cao')).values('date')
            .annotate(count=Count('id')).order_by('date')
        )
        
        context.update({
            'is_bod': True, # Đánh dấu là Ban Giám đốc
            'so_luong_nhan_vien': so_luong_nhan_vien,
            'so_luong_muc_tieu': so_luong_muc_tieu,
            'so_luong_su_co_thang_nay': so_luong_su_co_thang_nay,
            'so_su_co_moi': so_su_co_moi,
            'line_chart_labels': json.dumps([item['date'].strftime('%d/%m') for item in incidents_by_day]),
            'line_chart_data': json.dumps([item['count'] for item in incidents_by_day]),
        })

    # 3. Lấy dữ liệu cho Cấp quản lý (Chỉ huy trưởng, Quản lý Vùng...)
    if current_nhan_vien:
        bao_cao_duoc_giao = BaoCaoSuCo.objects.filter(
            nguoi_chiu_trach_nhiem=current_nhan_vien
        ).exclude(
            trang_thai=BaoCaoSuCo.TrangThaiBaoCao.DA_GIAI_QUYET
        ).order_by('-thoi_gian_bao_cao')
        context['bao_cao_list'] = bao_cao_duoc_giao
        
    return render(request, 'dashboard/main.html', context)