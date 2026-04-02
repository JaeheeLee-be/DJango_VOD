from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@test.com',
            'password': 'testpassword',
            'nickname': 'testnickname',
        }

    def test_user_manager_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.nickname, self.user_data['nickname'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_superuser)

    def test_user_manager_create_superuser(self):
        user = User.objects.create_superuser(**self.user_data)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)