from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class LoginTest(APITestCase):
    
    def setUp(self):
        """
        Set up user for testing login
        """
        self.username = 'minhtuan123'
        self.password = '123456a8'
        # Tạo một user để test login
        self.user = User.objects.create_user(username=self.username, password=self.password)
        
        # URL của API login (cần thay đổi tùy theo cấu hình của bạn)
        self.url = '/api/account/login'

    def test_login_successful(self):
        """
        Test login with valid credentials
        """
        # Gửi yêu cầu POST để login với username và password
        response = self.client.post(self.url, data={
            'username': self.username,
            'password': self.password
        })
        
        # Kiểm tra xem status code trả về có phải là 200 OK không
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Kiểm tra rằng response trả về chứa access token
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        
        # Kiểm tra token có phải là chuỗi không
        self.assertIsInstance(response.data['access_token'], str)
        self.assertIsInstance(response.data['refresh_token'], str)

    def test_login_invalid_credentials(self):
        """
        Test login with invalid credentials
        """
        # Gửi yêu cầu POST với thông tin đăng nhập sai
        response = self.client.post(self.url, data={
            'username': self.username,
            'password': 'wrongpassword'
        })
        
        # Kiểm tra xem status code có phải là 401 Unauthorized không
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Kiểm tra rằng response không chứa token
        self.assertIn('error', response.data)  # Đảm bảo API trả về key 'error'
        self.assertEqual(response.data['error'], 'Invalid username or password.')
