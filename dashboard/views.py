# dashboard/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Q, Prefetch
from datetime import timedelta, date
import json

# Import models từ các app liên quan
from users.models import NhanVien
from clients.models import MucTieu
from operations.models import PhanCongCaTruc, BaoCaoSuCo
from workflow.models import Task, Proposal

# --- CÁC HÀM HỖ TRỢ (HELPERS) ---

def get_incident_chart_data(days=7):
    """
    Lấy dữ liệu cho biểu đồ thống kê sự cố trong một khoảng thời gian.
    """
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days - 1)
    
    # Tạo danh sách các ngày trong khoảng thời gian
    date_range = [start_date + timedelta(days=i) for i in range(days)]
    labels = [day.strftime("%d/%m") for day in date_range]
    
    # Truy vấn dữ liệu sự cố, nhóm theo ngày
    incidents_by_day = (
        BaoCaoSuCo.objects.filter(thoi_gian_bao_cao__date__range=[start_date, end_date])
        .values("thoi_gian_bao_cao__date")
        .annotate(total=Count("id"))
        .order_by("thoi_gian_bao_cao__date")
    )
    
    # Tạo một dictionary để tra cứu số lượng sự cố theo ngày
    incident_map = {item["thoi_gian_bao_cao__date"]: item["total"] for item in incidents_by_day}
    
    # Tạo danh sách dữ liệu cuối cùng, điền 0 cho những ngày không có sự cố
    data = [incident_map.get(day, 0) for day in date_range]
    
    return json.dumps(labels), json.dumps(data)


def get_user_related_data(nhan_vien):
    """
    Lấy dữ liệu cá nhân (công việc, đề xuất) liên quan đến nhân viên.
    """
    if not nhan_vien:
        return [], []

    # Lấy danh sách ID các mục tiêu mà nhân viên được phân công
    # distinct() đảm bảo mỗi ID chỉ xuất hiện một lần
    assigned_muc_tieu_ids = PhanCongCaTruc.objects.filter(
        nhan_vien=nhan_vien
    ).values_list('vi_tri_chot__muc_tieu_id', flat=True).distinct()

    # Lấy các công việc chưa hoàn thành tại các mục tiêu đó
    # Sử dụng prefetch_related để tối ưu việc truy cập thông tin 'muc_tieu'
    my_tasks = Task.objects.filter(
        muc_tieu_id__in=assigned_muc_tieu_ids
    ).exclude(
        trang_thai='Hoàn thành'
    ).select_related('muc_tieu').order_by('han_chot')[:5]

    # Lấy các đề xuất cần nhân viên này duyệt
    # Sử dụng select_related để tối ưu truy vấn thông tin người tạo
    proposals_to_review = Proposal.objects.filter(
        nguoi_duyet=nhan_vien, 
        trang_thai='Chờ duyệt'
    ).select_related('nguoi_tao').order_by('-ngay_tao')[:5]

    return my_tasks, proposals_to_review

# --- VIEW CHÍNH ---

@login_required
def dashboard_view(request):
    """
    Hiển thị trang dashboard chính với các thông tin tổng quan.
    """
    # --- PHẦN 1: XÁC THỰC VÀ LẤY THÔNG TIN NHÂN VIÊN ---
    try:
        current_user_nhanvien = request.user.nhanvien
    except NhanVien.DoesNotExist:
        # Nếu là superuser mà chưa có profile NhanVien, chuyển đến trang admin để tạo
        if request.user.is_superuser:
            # Có thể thêm một thông báo ở đây để giải thích
            # from django.contrib import messages
            # messages.warning(request, 'Tài khoản của bạn chưa được liên kết với một hồ sơ Nhân Viên.')
            return redirect('admin:users_nhanvien_add') 
        # Với người dùng thường, đây là một lỗi. Có thể render một trang lỗi hoặc redirect.
        # Ở đây tạm thời gán là None để trang vẫn tải được các thông tin chung.
        current_user_nhanvien = None

    # --- PHẦN 2: LẤY DỮ LIỆU THỐNG KÊ TỔNG QUAN ---
    today = timezone.now().date()
    
    # Tổng hợp các truy vấn để giảm thiểu query
    so_nhan_vien = NhanVien.objects.filter(trang_thai_lam_viec='Đang làm việc').count()
    so_muc_tieu = MucTieu.objects.count()
    so_ca_truc_hom_nay = PhanCongCaTruc.objects.filter(ngay_truc=today).count()
    su_co_moi_count = BaoCaoSuCo.objects.filter(trang_thai='Mới').count()
    
    # Lấy 5 sự cố gần nhất, tối ưu bằng select_related
    su_co_gan_day = BaoCaoSuCo.objects.select_related(
        'ca_truc__vi_tri_chot__muc_tieu', 'nguoi_bao_cao'
    ).order_by("-thoi_gian_bao_cao")[:5]

    # --- PHẦN 3: LẤY DỮ LIỆU CHO BIỂU ĐỒ VÀ DỮ LIỆU CÁ NHÂN ---
    incident_chart_labels, incident_chart_data = get_incident_chart_data()
    my_tasks, proposals_to_review = get_user_related_data(current_user_nhanvien)

    # --- PHẦN 4: TỔNG HỢP CONTEXT VÀ RENDER TEMPLATE ---
    context = {
        # Dữ liệu thống kê
        "so_nhan_vien": so_nhan_vien,
        "so_muc_tieu": so_muc_tieu,
        "so_ca_truc_hom_nay": so_ca_truc_hom_nay,
        "su_co_moi": su_co_moi_count,
        "su_co_gan_day": su_co_gan_day,
        
        # Dữ liệu biểu đồ
        "incident_chart_labels": incident_chart_labels,
        "incident_chart_data": incident_chart_data,
        
        # Dữ liệu cá nhân
        "my_tasks": my_tasks,
        "proposals_to_review": proposals_to_review,
        
        # Biến điều hướng
        "section": "dashboard",
    }
    
    return render(request, "dashboard/main.html", context)