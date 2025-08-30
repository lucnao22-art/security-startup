# file: clients/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from .models import CoHoiKinhDoanh

@login_required
def pipeline_view(request):
    # Dòng code dưới đây gây lỗi vì không tìm thấy mô hình CoHoiKinhDoanh.
    # Bạn có thể bỏ bình luận dòng trên và đoạn code dưới khi đã định nghĩa mô hình.
    
    # status_choices = CoHoiKinhDoanh.TrangThai.choices
    # pipeline_data = []
    # for status_value, status_name in status_choices:
    #     co_hoi_trong_cot = CoHoiKinhDoanh.objects.filter(trang_thai=status_value)
    #     pipeline_data.append({
    #         'status_name': status_name,
    #         'opportunities': co_hoi_trong_cot
    #     })

    context = {
        # 'pipeline_data': pipeline_data,
        'message': 'Chức năng này hiện chưa khả dụng. Vui lòng định nghĩa mô hình CoHoiKinhDoanh.'
    }
    return render(request, 'clients/pipeline.html', context)