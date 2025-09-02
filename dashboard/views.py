# file: dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
import json # Import thư viện json

from users.models import NhanVien
from clients.models import MucTieu
from operations.models import PhanCongCaTruc, BaoCaoSuCo

@login_required
def dashboard_view(request):
    hom_nay = timezone.now().date()
    
    # --- DỮ LIỆU THỐNG KÊ CŨ (GIỮ NGUYÊN) ---
    so_nhan_vien = NhanVien.objects.filter(lich_su_cong_tac__la_vi_tri_hien_tai=True).distinct().count()
    so_muc_tieu = MucTieu.objects.count()
    so_ca_truc_hom_nay = PhanCongCaTruc.objects.filter(ngay_truc=hom_nay).count()
    su_co_gan_day = BaoCaoSuCo.objects.order_by("-thoi_gian_bao_cao")[:5]

    # --- LOGIC MỚI: CHUẨN BỊ DỮ LIỆU CHO BIỂU ĐỒ SỰ CỐ ---
    ngay_bat_dau = hom_nay - timedelta(days=6)
    
    # Tạo một danh sách các ngày trong 7 ngày qua
    labels = [(ngay_bat_dau + timedelta(days=i)).strftime("%d/%m") for i in range(7)]
    
    # Đếm số sự cố theo ngày
    su_co_theo_ngay = (
        BaoCaoSuCo.objects.filter(thoi_gian_bao_cao__date__gte=ngay_bat_dau)
        .values("thoi_gian_bao_cao__date")
        .annotate(total=Count("id"))
        .order_by("thoi_gian_bao_cao__date")
    )
    
    # Tạo một dict để dễ dàng tra cứu
    su_co_data_dict = {
        item["thoi_gian_bao_cao__date"].strftime("%d/%m"): item["total"]
        for item in su_co_theo_ngay
    }
    
    # Tạo danh sách dữ liệu cuối cùng, ngày nào không có sự cố thì giá trị là 0
    data = [su_co_data_dict.get(label, 0) for label in labels]
    
    context = {
        "so_nhan_vien": so_nhan_vien,
        "so_muc_tieu": so_muc_tieu,
        "so_ca_truc_hom_nay": so_ca_truc_hom_nay,
        "su_co_gan_day": su_co_gan_day,
        "section": "dashboard",
        # --- BIẾN MỚI CHO BIỂU ĐỒ ---
        # Chuyển dữ liệu Python thành chuỗi JSON an toàn để dùng trong JavaScript
        "incident_chart_labels": json.dumps(labels),
        "incident_chart_data": json.dumps(data),
    }

    return render(request, "dashboard/main.html", context)