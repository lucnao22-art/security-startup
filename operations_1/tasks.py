# file: operations/tasks.py
import logging # Thêm import
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import BaoCaoSuCo
from datetime import date, timedelta
from users.models import NhanVien  # SỬA LẠI DÒNG NÀY
from .models import PhanCongCaTruc, ViTriChot, BaoCaoSuCo
from .models import PhanCongCaTruc, ViTriChot


logger = logging.getLogger("my_project_logger") # Lấy logger

@shared_task
def check_and_escalate_reports():
    logger.info("Bắt đầu tác vụ kiểm tra và leo thang báo cáo sự cố...")
    try:
        time_threshold = timezone.now() - timedelta(minutes=5)
        overdue_reports = BaoCaoSuCo.objects.filter(...)
        
        count = 0
        for report in overdue_reports:
            # ... (logic) ...
            report.save()
            logger.info(f"Báo cáo #{report.id} đã được leo thang thành công đến {next_manager.ho_ten}.")
            count += 1
        
        logger.info(f"Hoàn thành tác vụ. Đã leo thang {count} báo cáo.")
        return f"Đã kiểm tra {overdue_reports.count()} báo cáo quá hạn."
        
    except Exception as e:
        logger.error("Lỗi nghiêm trọng trong tác vụ check_and_escalate_reports!", exc_info=True)
        # Báo lỗi để Celery có thể thử lại nếu được cấu hình
        raise


# ----- CÁC TASK MỚI CHO HỆ THỐNG CẢNH BÁO -----


@shared_task
def check_expired_certificates():
    """Quét các chứng chỉ sắp hết hạn trong 30 ngày tới."""
    thirty_days_later = date.today() + timedelta(days=30)
    expiring_certs = ChungChi.objects.filter(
        ngay_het_han__lte=thirty_days_later, ngay_het_han__gte=date.today()
    )
    for cert in expiring_certs:
        print(
            f"[CẢNH BÁO PHÁP LÝ] Chứng chỉ '{cert.ten_chung_chi}' của NV {cert.nhan_vien.ho_ten} sẽ hết hạn vào ngày {cert.ngay_het_han.strftime('%d/%m/%Y')}."
        )
    return f"Đã kiểm tra {expiring_certs.count()} chứng chỉ sắp hết hạn."


@shared_task
def check_unassigned_shifts():
    """Quét các vị trí chốt chưa được phân công cho ngày mai."""
    tomorrow = date.today() + timedelta(days=1)
    # Lấy ID của các vị trí đã có người trực vào ngày mai
    assigned_posts_ids = PhanCongCaTruc.objects.filter(ngay_truc=tomorrow).values_list(
        "vi_tri_chot_id", flat=True
    )
    # Tìm các vị trí chưa có trong danh sách trên
    unassigned_posts = ViTriChot.objects.exclude(id__in=assigned_posts_ids)

    for post in unassigned_posts:
        print(
            f"[CẢNH BÁO VẬN HÀNH] Vị trí '{post.ten_vi_tri}' tại mục tiêu '{post.muc_tieu.ten_muc_tieu}' chưa có người trực cho ngày mai ({tomorrow.strftime('%d/%m/%Y')})."
        )
    return f"Đã kiểm tra {unassigned_posts.count()} vị trí chưa được phân công."
