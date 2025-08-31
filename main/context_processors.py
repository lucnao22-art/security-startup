from .models import ThongTinCongTy


def company_info(request):
    """
    Context processor này sẽ tải thông tin công ty
    và cung cấp nó cho tất cả các template trong biến 'thong_tin_cong_ty'.

    Sử dụng .first() để tránh gây lỗi nếu chưa có bản ghi nào được tạo.
    """
    info = ThongTinCongTy.objects.first()
    return {"thong_tin_cong_ty": info}
