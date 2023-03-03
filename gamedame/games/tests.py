from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class UserTestCase(TestCase):
    
    def test_create_user(self):
        user = User.objects.create_user('joao', 'joao@email.com', '123')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'joao')
        self.assertEqual(user.email, 'joao@email.com')
        self.assertTrue(user.check_password('123'))