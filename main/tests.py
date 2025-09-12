# file: main/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import NhanVien, PhongBan
import datetime

class MainAppAuthTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='superuser', 
            password='superpassword123',
            email='super@user.com'
        )
        self.phong_van_hanh = PhongBan.objects.create(ten_phong_ban="Phòng Vận hành")
        
        self.nhanvien_user = User.objects.create_user(
            username='nhanvien', 
            password='nhanvienpassword123',
            email='nhan@vien.com'
        )
        self.nhanvien = NhanVien.objects.create(
            user=self.nhanvien_user,
            phong_ban=self.phong_van_hanh,
            ngay_sinh=datetime.date(1990, 1, 1)
        )

    def test_homepage_view_for_unauthenticated_user(self):
        response = self.client.get(reverse('main:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/homepage.html')

    def test_homepage_view_for_authenticated_user_redirects(self):
        self.client.login(username='nhanvien', password='nhanvienpassword123')
        response = self.client.get(reverse('main:homepage'))
        # SỬA LỖI: Kiểm tra chuyển hướng mà không cần truy cập trang đích
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('main:dashboard_hub'))

    def test_login_success(self):
        response = self.client.post(reverse('main:homepage'), {
            'username': 'nhanvien',
            'password': 'nhanvienpassword123'
        })
        self.assertTrue(self.client.session['_auth_user_id'])
        # SỬA LỖI: Kiểm tra chuyển hướng mà không cần truy cập trang đích
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('main:dashboard_hub'))

    def test_login_fail_with_wrong_password(self):
        response = self.client.post(reverse('main:homepage'), {
            'username': 'nhanvien',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/homepage.html')
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertContains(response, "Tên đăng nhập hoặc mật khẩu không đúng.")

    def test_logout_view(self):
        self.client.login(username='nhanvien', password='nhanvienpassword123')
        response = self.client.get(reverse('main:logout'))
        self.assertRedirects(response, reverse('main:homepage'))
        self.assertNotIn('_auth_user_id', self.client.session)
    
    def test_dashboard_hub_unauthenticated_redirects(self):
        response = self.client.get(reverse('main:dashboard_hub'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('main:homepage')}?next=/hub/")

    def test_dashboard_hub_for_superuser(self):
        self.client.login(username='superuser', password='superpassword123')
        response = self.client.get(reverse('main:dashboard_hub'))
        self.assertRedirects(response, reverse('dashboard:dashboard_view'))

    def test_dashboard_hub_for_nhanvien_vanhanh(self):
        self.client.login(username='nhanvien', password='nhanvienpassword123')
        response = self.client.get(reverse('main:dashboard_hub'))
        self.assertRedirects(response, reverse('operations:mobile_dashboard'))