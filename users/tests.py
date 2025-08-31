from django.test import TestCase
from .models import NhanVien


class NhanVienModelTest(TestCase):
    def setUp(self):
        """
        Thiết lập dữ liệu mẫu để chạy test.
        Hàm này sẽ được chạy trước mỗi bài test.
        """
        # Tạo một nhân viên mẫu.
        self.nhan_vien_instance = NhanVien.objects.create(
            ho_ten="Nguyễn Văn A",
            ngay_sinh="1990-01-15",
            gioi_tinh=NhanVien.GioiTinh.NAM,
            so_cccd="012345678901",
            ngay_cap_cccd="2020-10-10",
            noi_cap_cccd="Công an TP.Hà Nội",
            sdt_chinh="0987654321",
            dia_chi_thuong_tru="Hà Nội",
            dia_chi_tam_tru="Hà Nội",
            ten_lien_he_khan_cap="Nguyễn Thị B",
            quan_he_khan_cap="Vợ",
            sdt_khan_cap="0123456788",
            chuc_vu=NhanVien.ChucVu.NHAN_VIEN,
        )

    def test_nhan_vien_str_method(self):
        """
        Kiểm tra phương thức __str__ của NhanVien
        có trả về đúng định dạng "ma_nhan_vien - ho_ten" không.
        """
        # Lấy lại đối tượng nhân viên từ database để có `ma_nhan_vien`
        nv = NhanVien.objects.get(id=self.nhan_vien_instance.id)

        # Kết quả mong đợi theo định dạng trong model của bạn
        expected_string = f"{nv.ma_nhan_vien} - {nv.ho_ten}"

        # So sánh kết quả của hàm __str__() với kết quả mong đợi
        self.assertEqual(str(nv), expected_string)

        print(f"Đã test thành công: __str__ trả về '{expected_string}'")
