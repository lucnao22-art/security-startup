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
# ----- CÁC TASK MỚI CHO HỆ THỐNG CẢNH BÁO -----

@shared_task
def check_expired_certificates():
    """Quét các chứng chỉ sắp hết hạn trong 30 ngày tới."""
    thirty_days_later = date.today() + timedelta(days=30)
    expiring_certs = ChungChi.objects.filter(
        ngay_het_han__lte=thirty_days_later,
        ngay_het_han__gte=date.today()
    )
    for cert in expiring_certs:
        print(f"[CẢNH BÁO PHÁP LÝ] Chứng chỉ '{cert.ten_chung_chi}' của NV {cert.nhan_vien.ho_ten} sẽ hết hạn vào ngày {cert.ngay_het_han.strftime('%d/%m/%Y')}.")
    return f"Đã kiểm tra {expiring_certs.count()} chứng chỉ sắp hết hạn."

@shared_task
def check_unassigned_shifts():
    """Quét các vị trí chốt chưa được phân công cho ngày mai."""
    tomorrow = date.today() + timedelta(days=1)
    # Lấy ID của các vị trí đã có người trực vào ngày mai
    assigned_posts_ids = PhanCongCaTruc.objects.filter(ngay_truc=tomorrow).values_list('vi_tri_chot_id', flat=True)
    # Tìm các vị trí chưa có trong danh sách trên
    unassigned_posts = ViTriChot.objects.exclude(id__in=assigned_posts_ids)
    
    for post in unassigned_posts:
        print(f"[CẢNH BÁO VẬN HÀNH] Vị trí '{post.ten_vi_tri}' tại mục tiêu '{post.muc_tieu.ten_muc_tieu}' chưa có người trực cho ngày mai ({tomorrow.strftime('%d/%m/%Y')}).")
    return f"Đã kiểm tra {unassigned_posts.count()} vị trí chưa được phân công."