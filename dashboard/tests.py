# file: dashboard/tests.py
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta, datetime, time

from django.contrib.auth.models import User
from users.models import NhanVien, LichSuCongTac
from clients.models import MucTieu, KhachHangTiemNang, HopDong, CoHoiKinhDoanh
from operations.models import BaoCaoSuCo, PhanCongCaTruc, CaLamViec, ViTriChot


class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = Client()
        
        hom_nay = timezone.now().date()
        hom_qua = hom_nay - timedelta(days=1)
        
        thoi_diem_hom_nay = timezone.make_aware(datetime.combine(hom_nay, time(10, 0)))
        thoi_diem_hom_qua = timezone.make_aware(datetime.combine(hom_qua, time(15, 0)))

        # --- Dữ liệu mẫu ---
        khach_hang = KhachHangTiemNang.objects.create(
            ten_cong_ty="Công ty ABC", nguoi_lien_he="Anh A", email="contact@abc.com",
            sdt="0123456789", dia_chi="123 Đường ABC"
        )
        co_hoi = CoHoiKinhDoanh.objects.create(
            ten_co_hoi="Cơ hội với ABC", khach_hang_tiem_nang=khach_hang,
            gia_tri_uoc_tinh=100000000, ngay_ket_thuc_du_kien=hom_nay + timedelta(days=30)
        )
        hop_dong = HopDong.objects.create(
            co_hoi=co_hoi, so_hop_dong="HD001", ngay_ky=hom_nay, ngay_hieu_luc=hom_nay,
            ngay_het_han=hom_nay + timedelta(days=365), gia_tri=100000000
        )
        muc_tieu = MucTieu.objects.create(ten_muc_tieu="Mục tiêu A", hop_dong=hop_dong)
        vi_tri = ViTriChot.objects.create(muc_tieu=muc_tieu, ten_vi_tri="Chốt cổng chính")
        ca_lam_viec = CaLamViec.objects.create(ten_ca="Ca ngày", gio_bat_dau="06:00", gio_ket_thuc="18:00")
        nv1 = NhanVien.objects.create(ho_ten="Nhân viên 1", ngay_sinh=date(1990,1,1), gioi_tinh="M", so_cccd="111")
        LichSuCongTac.objects.create(nhan_vien=nv1, ngay_bat_dau=hom_nay-timedelta(days=10), la_vi_tri_hien_tai=True)
        ca_truc_hom_nay = PhanCongCaTruc.objects.create(nhan_vien=nv1, vi_tri_chot=vi_tri, ca_lam_viec=ca_lam_viec, ngay_truc=hom_nay)

        # --- SỬA LỖI LOGIC TRIỆT ĐỂ ---
        # Do trường `thoi_gian_bao_cao` có `auto_now_add=True`, chúng ta không thể
        # gán giá trị trực tiếp khi tạo. Ta phải tạo trước, rồi update sau.
        
        # Tạo 2 sự cố, thời gian sẽ tự động là "hôm nay"
        sc1 = BaoCaoSuCo.objects.create(ca_truc=ca_truc_hom_nay, tieu_de="Sự cố hôm nay 1", noi_dung="Chi tiết")
        sc2 = BaoCaoSuCo.objects.create(ca_truc=ca_truc_hom_nay, tieu_de="Sự cố hôm nay 2", noi_dung="Chi tiết")
        
        # Tạo sự cố thứ 3, sau đó "ép" thời gian của nó về "hôm qua"
        sc3 = BaoCaoSuCo.objects.create(ca_truc=ca_truc_hom_nay, tieu_de="Sự cố hôm qua", noi_dung="Chi tiết")
        BaoCaoSuCo.objects.filter(pk=sc3.pk).update(thoi_gian_bao_cao=thoi_diem_hom_qua)


    def test_dashboard_view_loads_correctly_and_has_chart_data(self):
        """
        Kiểm tra: Trang dashboard tải thành công VÀ có chứa dữ liệu cho biểu đồ.
        """
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('dashboard:dashboard_view'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/main.html')
        
        self.assertIn('incident_chart_labels', response.context)
        self.assertIn('incident_chart_data', response.context)
        
        labels = json.loads(response.context['incident_chart_labels'])
        data = json.loads(response.context['incident_chart_data'])
        
        self.assertEqual(len(labels), 7)
        self.assertEqual(len(data), 7)
        
        # Bây giờ, khẳng định này chắc chắn sẽ đúng
        self.assertEqual(data[-1], 2) # Dữ liệu ngày cuối cùng (hôm nay)
        self.assertEqual(data[-2], 1) # Dữ liệu ngày kế cuối (hôm qua)