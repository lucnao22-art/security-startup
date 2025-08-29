# file: clients/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CoHoiKinhDoanh

@login_required
def pipeline_view(request):
    # Lấy tất cả các trạng thái từ model
    status_choices = CoHoiKinhDoanh.TrangThai.choices

    # Nhóm các cơ hội theo từng trạng thái
    pipeline_data = []
    for status_value, status_name in status_choices:
        co_hoi_trong_cot = CoHoiKinhDoanh.objects.filter(trang_thai=status_value)
        pipeline_data.append({
            'status_name': status_name,
            'opportunities': co_hoi_trong_cot
        })

    context = {
        'pipeline_data': pipeline_data,
    }
    return render(request, 'clients/pipeline.html', context)