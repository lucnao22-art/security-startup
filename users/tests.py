# file: users/tests.py
from django.test import TestCase
from .models import NhanVien, CauHinhMaNhanVien, PhongBan, ChucDanh
from django.contrib.auth.models import User
from datetime import date

class NhanVienModelTestCase(TestCase):
    """
    Bộ kiểm thử cho model NhanVien.
    """

    def setUp(self):
        """
        Thiết lập dữ liệu ban đầu cho mỗi bài test.
        Hàm này sẽ chạy trước mỗi hàm test (bắt đầu bằng test_*).
        """
        CauHinhMaNhanVien.objects.create(pk=1, tien_to="NV", do_dai_so=4, so_hien_tai=0)
        PhongBan.objects.create(ten_phong_ban="Phòng Kỹ thuật")
        ChucDanh.objects.create(ten_chuc_danh="Lập trình viên")

    def test_generate_employee_code_on_creation(self):
        """
        Kiểm tra xem mã nhân viên có được tự động sinh ra khi tạo mới không.
        """
        # Tạo nhân viên đầu tiên
        nv1 = NhanVien.objects.create(
            ho_ten="Nguyễn Văn A",
            ngay_sinh=date(1990, 1, 1),
            gioi_tinh="M",
            so_cccd="123456789012",
            sdt_chinh="0901234567",
            email="a.nguyen@example.com",
            phong_ban=PhongBan.objects.get(pk=1),
            chuc_danh=ChucDanh.objects.get(pk=1),
        )
        
        # Kiểm tra mã của nhân viên đầu tiên
        self.assertEqual(nv1.ma_nhan_vien, "NV0001")

        # Tạo nhân viên thứ hai
        nv2 = NhanVien.objects.create(
            ho_ten="Trần Thị B",
            ngay_sinh=date(1995, 5, 10),
            gioi_tinh="F",
            so_cccd="987654321098",
            sdt_chinh="0987654321",
            email="b.tran@example.com",
            phong_ban=PhongBan.objects.get(pk=1),
            chuc_danh=ChucDanh.objects.get(pk=1),
        )

        # Kiểm tra mã của nhân viên thứ hai phải tăng lên
        self.assertEqual(nv2.ma_nhan_vien, "NV0002")

        # Kiểm tra xem cấu hình mã đã được cập nhật đúng chưa
        config = CauHinhMaNhanVien.objects.get(pk=1)
        self.assertEqual(config.so_hien_tai, 2)