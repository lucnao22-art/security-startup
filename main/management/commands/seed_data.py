import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User, Group
from users.models import NhanVien, PhongBan, ChucDanh
# SỬA LỖI: Cập nhật toàn bộ import từ app 'clients'
from clients.models import KhachHangTiemNang, CoHoiKinhDoanh, HopDong, MucTieu
from operations.models import CaLamViec, PhanCongCaTruc, ViTriChot
from inventory.models import LoaiVatTu, VatTu, NhaCungCap
from datetime import date, timedelta, time
from decimal import Decimal

# Khởi tạo Faker
fake = Faker('vi_VN')

class Command(BaseCommand):
    help = 'Tạo dữ liệu giả hoàn chỉnh theo logic kinh doanh mới'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Bắt đầu quá trình tạo dữ liệu giả...'))

        # ==============================================================================
        # XÓA DỮ LIỆU CŨ ĐỂ ĐẢM BẢO TÍNH TOÀN VẸN
        # ==============================================================================
        self.stdout.write('Xóa dữ liệu cũ...')
        # Xóa theo thứ tự phụ thuộc để tránh lỗi khóa ngoại (foreign key)
        PhanCongCaTruc.objects.all().delete()
        ViTriChot.objects.all().delete()
        MucTieu.objects.all().delete()
        HopDong.objects.all().delete()
        CoHoiKinhDoanh.objects.all().delete()
        KhachHangTiemNang.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        NhanVien.objects.all().delete()
        PhongBan.objects.all().delete()
        ChucDanh.objects.all().delete()
        CaLamViec.objects.all().delete()
        VatTu.objects.all().delete()
        LoaiVatTu.objects.all().delete()
        NhaCungCap.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Đã xóa xong dữ liệu cũ.'))


        # ==============================================================================
        # 1. TẠO DỮ LIỆU NHÂN SỰ (PHÒNG BAN, CHỨC DANH, NHÂN VIÊN)
        # ==============================================================================
        self.stdout.write('Tạo dữ liệu Phòng ban, Chức danh và Nhân viên...')
        phong_ban_list = ['Ban Giám Đốc', 'Phòng Kinh doanh', 'Phòng Nhân sự', 'Phòng Vận hành']
        phong_bans = [PhongBan.objects.create(ten_phong_ban=ten) for ten in phong_ban_list]
        
        chuc_danh_list = ['Giám đốc', 'Trưởng phòng Kinh doanh', 'Nhân viên Kinh doanh', 'Chỉ huy trưởng', 'Nhân viên bảo vệ']
        chuc_danhs = [ChucDanh.objects.create(ten_chuc_danh=ten) for ten in chuc_danh_list]
        
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            NhanVien.objects.create(
                user=admin_user, ho_ten='Admin Quản trị', phong_ban=phong_bans[0], chuc_danh=chuc_danhs[0],
                ngay_sinh=fake.date_of_birth(minimum_age=30, maximum_age=50), gioi_tinh=NhanVien.GioiTinh.NAM,
                so_cccd=fake.unique.ssn(), sdt_chinh=fake.phone_number(), email='admin@example.com',
                ngay_vao_lam=date.today() - timedelta(days=365), trang_thai_lam_viec=NhanVien.TrangThaiLamViec.CHINH_THUC
            )
            
        for _ in range(50):
            ho_ten = fake.name()
            username = f"{ho_ten.split(' ')[-1].lower().replace('.', '')}{fake.unique.random_int(min=100, max=999)}"
            try:
                user = User.objects.create_user(username, f"{username}@example.com", 'password123')
                NhanVien.objects.create(
                    user=user, ho_ten=ho_ten, phong_ban=random.choice(phong_bans), chuc_danh=random.choice(chuc_danhs),
                    ngay_sinh=fake.date_of_birth(minimum_age=18, maximum_age=55), gioi_tinh=random.choice(list(NhanVien.GioiTinh)),
                    so_cccd=fake.unique.ssn(), sdt_chinh=fake.phone_number(), email=f"{username}@example.com"
                )
            except Exception: continue
        self.stdout.write(self.style.SUCCESS(f'Đã tạo {NhanVien.objects.count()} nhân viên.'))

        # ==============================================================================
        # 2. TẠO DỮ LIỆU PIPELINE KINH DOANH (KH TIỀM NĂNG -> CƠ HỘI -> HỢP ĐỒNG -> MỤC TIÊU)
        # ==============================================================================
        self.stdout.write('Tạo dữ liệu Pipeline Kinh doanh...')
        nhan_vien_kd_list = list(NhanVien.objects.all())

        for _ in range(30): # Tạo 30 khách hàng tiềm năng
            kh_tiem_nang = KhachHangTiemNang.objects.create(
                ten_cong_ty=fake.company(),
                nguoi_lien_he=fake.name(),
                email=fake.company_email(),
                sdt=fake.phone_number(),
                dia_chi=fake.address()
            )

            # Mỗi KHTN có 1-2 cơ hội kinh doanh
            for _ in range(random.randint(1, 2)):
                co_hoi = CoHoiKinhDoanh.objects.create(
                    ten_co_hoi=f"Cung cấp dịch vụ cho {kh_tiem_nang.ten_cong_ty}",
                    khach_hang_tiem_nang=kh_tiem_nang,
                    gia_tri_uoc_tinh=Decimal(random.randrange(50000000, 500000000, 1000000)),
                    ngay_ket_thuc_du_kien=date.today() + timedelta(days=random.randint(30, 90)),
                    trang_thai=random.choice(list(CoHoiKinhDoanh.TrangThai)),
                    nguoi_phu_trach=random.choice(nhan_vien_kd_list)
                )

                # Nếu cơ hội thành công -> tạo Hợp đồng
                if co_hoi.trang_thai == CoHoiKinhDoanh.TrangThai.THANH_CONG:
                    hop_dong = HopDong.objects.create(
                        co_hoi=co_hoi,
                        so_hop_dong=f"HD-{fake.unique.random_int(min=1000, max=9999)}",
                        ngay_ky=date.today() - timedelta(days=random.randint(5, 30)),
                        ngay_hieu_luc=date.today(),
                        ngay_het_han=date.today() + timedelta(days=365),
                        gia_tri=co_hoi.gia_tri_uoc_tinh,
                    )

                    # Mỗi hợp đồng có 1-3 mục tiêu
                    for i in range(random.randint(1, 3)):
                        mt = MucTieu.objects.create(
                            hop_dong=hop_dong,
                            ten_muc_tieu=f"Mục tiêu {i+1} - {kh_tiem_nang.ten_cong_ty}",
                            dia_chi=fake.address(),
                            nguoi_lien_he=fake.name(),
                            sdt_lien_he=fake.phone_number(),
                            quan_ly_muc_tieu=random.choice(nhan_vien_kd_list)
                        )
                        # Mỗi mục tiêu tạo 2-5 vị trí chốt
                        for j in range(random.randint(2, 5)):
                            ViTriChot.objects.create(muc_tieu=mt, ten_vi_tri=f"Chốt {j+1}")
        
        self.stdout.write(self.style.SUCCESS(f'Đã tạo {CoHoiKinhDoanh.objects.count()} cơ hội, {HopDong.objects.count()} hợp đồng và {MucTieu.objects.count()} mục tiêu.'))

        # ==============================================================================
        # CÁC PHẦN CÒN LẠI (CA LÀM VIỆC, KHO, PHÂN CÔNG)
        # ==============================================================================
        self.stdout.write('Tạo dữ liệu Ca làm việc...')
        ca_lam_viec_data = [
            {'ten_ca': 'Ca Ngày', 'gio_bat_dau': time(7, 0), 'gio_ket_thuc': time(19, 0)},
            {'ten_ca': 'Ca Đêm', 'gio_bat_dau': time(19, 0), 'gio_ket_thuc': time(7, 0)},
        ]
        for data in ca_lam_viec_data:
            CaLamViec.objects.get_or_create(**data)

        self.stdout.write('Tạo dữ liệu Kho và Vật tư...')
        # Sửa lại cho đúng tên trường trong model
        loai_vat_tu_list = ['Đồng phục', 'Công cụ hỗ trợ', 'Văn phòng phẩm']
        loai_vts = [LoaiVatTu.objects.create(ten_loai=ten) for ten in loai_vat_tu_list]
        for _ in range(10):
            NhaCungCap.objects.create(ten_nha_cung_cap=fake.company(), dia_chi=fake.address(), so_dien_thoai=fake.phone_number())
        nha_cung_cap_list = list(NhaCungCap.objects.all())
        for i in range(100):
            VatTu.objects.create(
                ten_vat_tu=f"{random.choice(loai_vat_tu_list)} loại {i+1}", ma_vat_tu=f"VT{1000+i}",
                don_vi_tinh=random.choice(['Cái', 'Bộ', 'Chiếc']), loai=random.choice(loai_vts),
                nha_cung_cap=random.choice(nha_cung_cap_list), so_luong_ton=random.randint(10, 200)
            )
        
        self.stdout.write('Tạo dữ liệu Phân công ca trực...')
        all_nhan_vien_bv = list(NhanVien.objects.exclude(user__is_superuser=True))
        all_vi_tri = list(ViTriChot.objects.all())
        all_ca_lam_viec = list(CaLamViec.objects.all())
        
        if all_nhan_vien_bv and all_vi_tri and all_ca_lam_viec:
            start_date = date.today() - timedelta(days=15)
            for i in range(45): # Tạo lịch cho 45 ngày (quá khứ và tương lai)
                current_date = start_date + timedelta(days=i)
                for vt in all_vi_tri:
                    for ca in all_ca_lam_viec:
                        # Gán 1-2 nhân viên cho mỗi vị trí mỗi ca
                        if len(all_nhan_vien_bv) >= 2:
                            nhan_vien_ca_nay = random.sample(all_nhan_vien_bv, k=random.randint(1, 2))
                            for nv in nhan_vien_ca_nay:
                                PhanCongCaTruc.objects.get_or_create(
                                    nhan_vien=nv, ca_lam_viec=ca, vi_tri_chot=vt, ngay_truc=current_date
                                )
        
        self.stdout.write(self.style.SUCCESS('Hoàn thành!'))