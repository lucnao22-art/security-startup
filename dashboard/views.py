# file: dashboard/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
import json

# Import models từ các app liên quan
from users.models import NhanVien
from clients.models import MucTieu
from operations.models import PhanCongCaTruc, BaoCaoSuCo
from workflow.models import Task, Proposal

@login_required
def dashboard_view(request):
    # --- PHẦN 1: XỬ LÝ LỖI "User has no nhanvien" ---
    current_user_nhanvien = None
    try:
        current_user_nhanvien = request.user.nhanvien
    except NhanVien.DoesNotExist:
        if request.user.is_superuser:
            return redirect('/admin/')
        pass

    # --- PHẦN 2: LẤY DỮ LIỆU THỐNG KÊ VÀ BIỂU ĐỒ ---
    hom_nay = timezone.now().date()
    
    so_nhan_vien = NhanVien.objects.filter(trang_thai_lam_viec='Đang làm việc').count()
    so_muc_tieu = MucTieu.objects.count()
    so_ca_truc_hom_nay = PhanCongCaTruc.objects.filter(ngay_truc=hom_nay).count()
    su_co_gan_day = BaoCaoSuCo.objects.order_by("-thoi_gian_bao_cao")[:5]
    su_co_moi = BaoCaoSuCo.objects.filter(trang_thai='Mới').count()
    
    # Dữ liệu cho biểu đồ sự cố 7 ngày qua (giữ nguyên)
    ngay_bat_dau = hom_nay - timedelta(days=6)
    labels = [(ngay_bat_dau + timedelta(days=i)).strftime("%d/%m") for i in range(7)]
    su_co_theo_ngay = (
        BaoCaoSuCo.objects.filter(thoi_gian_bao_cao__date__gte=ngay_bat_dau)
        .values("thoi_gian_bao_cao__date")
        .annotate(total=Count("id"))
        .order_by("thoi_gian_bao_cao__date")
    )
    su_co_data_dict = {
        item["thoi_gian_bao_cao__date"].strftime("%d/%m"): item["total"]
        for item in su_co_theo_ngay
    }
    data = [su_co_data_dict.get(label, 0) for label in labels]

    # --- PHẦN 3: LẤY DỮ LIỆU CÔNG VIỆC VÀ ĐỀ XUẤT CÁ NHÂN ---
    my_tasks = []
    proposals_to_review = []
    if current_user_nhanvien:
        # === SỬA LỖI Ở ĐÂY: Sửa lại đường dẫn truy vấn cho đúng cấu trúc model mới ===
        cac_muc_tieu_cua_nv = PhanCongCaTruc.objects.filter(nhan_vien=current_user_nhanvien).values_list('vi_tri_chot__muc_tieu', flat=True).distinct()
        # ============================================================================
        
        my_tasks = Task.objects.filter(
            muc_tieu__in=cac_muc_tieu_cua_nv
        ).exclude(
            trang_thai='Hoàn thành'
        ).order_by('han_chot')[:5]
        
        proposals_to_review = Proposal.objects.filter(
            nguoi_duyet=current_user_nhanvien,
            trang_thai='Chờ duyệt'
        ).order_by('-ngay_tao')[:5]

    # --- PHẦN 4: TỔNG HỢP CONTEXT VÀ RENDER TEMPLATE ---
    context = {
        "so_nhan_vien": so_nhan_vien,
        "so_muc_tieu": so_muc_tieu,
        "so_ca_truc_hom_nay": so_ca_truc_hom_nay,
        "su_co_gan_day": su_co_gan_day,
        "su_co_moi": su_co_moi,
        "section": "dashboard",
        "incident_chart_labels": json.dumps(labels),
        "incident_chart_data": json.dumps(data),
        "my_tasks": my_tasks,
        "proposals_to_review": proposals_to_review,
    }
    
    return render(request, "dashboard/main.html", context)