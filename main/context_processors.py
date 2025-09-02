# file: main/context_processors.py
from .models import CompanyProfile # Sửa ThongTinCongTy thành CompanyProfile

def company_info(request):
    """
    Thêm thông tin công ty vào context của tất cả các template.
    """
    try:
        company = CompanyProfile.objects.first()
    except CompanyProfile.DoesNotExist:
        company = None
    return {"company": company}