# file: inspection/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import TuyenTuanTra, LuotTuanTra, KetQuaKiemTra, DiemKiemTra
from users.models import NhanVien


@login_required
def tuan_tra_mobile_view(request):
    """
    Hiển thị danh sách các tuyến tuần tra cho nhân viên và cho phép họ bắt đầu một lượt mới.
    """
    try:
        nhan_vien = request.user.nhanvien
        muc_tieu_hien_tai = nhan_vien.muc_tieu_lam_viec
    except NhanVien.DoesNotExist:
        messages.error(request, "Tài khoản của bạn không liên kết với hồ sơ nhân viên.")
        return render(request, "inspection/mobile/tuan_tra.html")

    if not muc_tieu_hien_tai:
        messages.warning(request, "Bạn chưa được phân công cho mục tiêu nào.")
        return render(request, "inspection/mobile/tuan_tra.html")

    # Xử lý khi nhân viên bấm nút "Bắt đầu"
    if request.method == "POST":
        tuyen_id = request.POST.get("tuyen_id")
        tuyen_tuan_tra = get_object_or_404(TuyenTuanTra, id=tuyen_id)

        # Tạo một lượt tuần tra mới
        luot_tuan_tra = LuotTuanTra.objects.create(
            tuyen_tuan_tra=tuyen_tuan_tra, nhan_vien=nhan_vien
        )
        return redirect(
            "inspection:mobile_chi_tiet_luot_tuan_tra",
            luot_tuan_tra_id=luot_tuan_tra.id,
        )

    # Kiểm tra xem có lượt tuần tra nào đang dang dở không
    luot_dang_thuc_hien = LuotTuanTra.objects.filter(
        nhan_vien=nhan_vien, trang_thai=LuotTuanTra.TrangThai.DANG_TIEN_HANH
    ).first()

    # Nếu có, chuyển thẳng đến trang chi tiết lượt đó
    if luot_dang_thuc_hien:
        return redirect(
            "inspection:mobile_chi_tiet_luot_tuan_tra",
            luot_tuan_tra_id=luot_dang_thuc_hien.id,
        )

    # Nếu không, hiển thị danh sách các tuyến tuần tra tại mục tiêu
    tuyen_tuan_tra_list = TuyenTuanTra.objects.filter(
        muc_tieu=muc_tieu_hien_tai, is_active=True
    )

    context = {
        "tuyen_tuan_tra_list": tuyen_tuan_tra_list,
        "muc_tieu": muc_tieu_hien_tai,
    }
    return render(request, "inspection/mobile/tuan_tra.html", context)


@login_required
def chi_tiet_luot_tuan_tra_view(request, luot_tuan_tra_id):
    """
    Hiển thị chi tiết một lượt tuần tra đang diễn ra, bao gồm danh sách các điểm cần check.
    """
    luot_tuan_tra = get_object_or_404(LuotTuanTra, id=luot_tuan_tra_id)

    # Lấy tất cả các điểm kiểm tra của tuyến này
    diem_kiem_tra_list = DiemKiemTra.objects.filter(
        tuyen_tuan_tra=luot_tuan_tra.tuyen_tuan_tra
    )

    # Lấy danh sách các điểm đã được quét trong lượt này
    diem_da_quet_ids = KetQuaKiemTra.objects.filter(
        luot_tuan_tra=luot_tuan_tra
    ).values_list("diem_kiem_tra_id", flat=True)

    context = {
        "luot_tuan_tra": luot_tuan_tra,
        "diem_kiem_tra_list": diem_kiem_tra_list,
        "diem_da_quet_ids": list(diem_da_quet_ids),
    }
    return render(request, "inspection/mobile/chi_tiet_luot_tuan_tra.html", context)
