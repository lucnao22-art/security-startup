from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from users.models import NhanVien
from clients.models import MucTieu
from operations.models import PhanCongCaTruc, BaoCaoSuCo


@login_required
def dashboard_view(request):
    # --- DÒNG TRUY VẤN ĐÃ SỬA LỖI ---
    # Logic mới: Đếm số nhân viên có ít nhất một Lịch sử công tác đang ở trạng thái "Vị trí hiện tại"
    so_nhan_vien = (
        NhanVien.objects.filter(lich_su_cong_tac__la_vi_tri_hien_tai=True)
        .distinct()
        .count()
    )

    so_muc_tieu = MucTieu.objects.count()

    hom_nay = timezone.now().date()

    so_ca_truc_hom_nay = PhanCongCaTruc.objects.filter(ngay_truc=hom_nay).count()

    su_co_gan_day = BaoCaoSuCo.objects.order_by("-thoi_gian_bao_cao")[:5]

    context = {
        "so_nhan_vien": so_nhan_vien,
        "so_muc_tieu": so_muc_tieu,
        "so_ca_truc_hom_nay": so_ca_truc_hom_nay,
        "su_co_gan_day": su_co_gan_day,
        "section": "dashboard",
    }

    return render(request, "dashboard/main.html", context)
