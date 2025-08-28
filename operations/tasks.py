# file: operations/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import BaoCaoSuCo

@shared_task
def check_and_escalate_reports():
    time_threshold = timezone.now() - timedelta(minutes=5)
    overdue_reports = BaoCaoSuCo.objects.filter(
        trang_thai__in=[BaoCaoSuCo.TrangThaiBaoCao.MOI, BaoCaoSuCo.TrangThaiBaoCao.DA_XEM],
        thoi_gian_bao_cao__lte=time_threshold
    )
    
    for report in overdue_reports:
        current_manager = report.nguoi_chiu_trach_nhiem
        if current_manager and current_manager.quan_ly_truc_tiep:
            next_manager = current_manager.quan_ly_truc_tiep
            report.nguoi_chiu_trach_nhiem = next_manager
            report.trang_thai = BaoCaoSuCo.TrangThaiBaoCao.LEO_THANG
            report.lich_su_xu_ly += f"\n[{timezone.now().strftime('%d/%m %H:%M')}] Tự động leo thang đến {next_manager.ho_ten}."
            report.save()
            print(f"Báo cáo #{report.id} đã được leo thang đến {next_manager.ho_ten}")
    
    return f"Đã kiểm tra {overdue_reports.count()} báo cáo quá hạn."