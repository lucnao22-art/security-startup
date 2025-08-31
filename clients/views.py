from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CoHoiKinhDoanh
from django.db.models import Sum, Count


@login_required
def pipeline_view(request):
    """
    Hiển thị pipeline kinh doanh dưới dạng bảng Kanban.
    - Dữ liệu được nhóm theo từng giai đoạn.
    - Tính toán tổng giá trị và số lượng cơ hội cho mỗi giai đoạn.
    """
    # Lấy tất cả các lựa chọn giai đoạn từ model
    stages = CoHoiKinhDoanh.TrangThai.choices
    pipeline_stages = {}

    for stage_key, stage_name in stages:
        # Lấy tất cả cơ hội thuộc giai đoạn hiện tại
        opportunities = CoHoiKinhDoanh.objects.filter(
            trang_thai=stage_key
        ).select_related("khach_hang_tiem_nang")

        # Sử dụng aggregate để tính toán tổng giá trị và số lượng một cách hiệu quả
        summary = opportunities.aggregate(
            total_value=Sum("gia_tri_uoc_tinh"), deal_count=Count("id")
        )

        pipeline_stages[stage_name] = {
            "opportunities": opportunities,
            "total_value": summary["total_value"] or 0,
            "deal_count": summary["deal_count"],
        }

    context = {"pipeline_stages": pipeline_stages, "section": "pipeline"}
    return render(request, "clients/pipeline.html", context)
