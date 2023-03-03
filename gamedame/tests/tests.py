from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from games.views import gameList


class TestCase(TestCase):
    # Testa se é possível cadastrar um usuário
    def test_create_user(self):
        user = User.objects.create_user('joao', 'joao@email.com', '123')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'joao')
        self.assertEqual(user.email, 'joao@email.com')
        self.assertTrue(user.check_password('123'))

    # Testa se é possível logar no sistema
    def test_user_login(self):
        user = User.objects.create_user('maria', 'maria@email.com', 'abc123')
        login = self.client.login(username=user.username, password='abc123')
        self.assertTrue(login)

    # Testa se é possível cadastrar um superusuário
    def test_create_superuser(self):
        superuser = User.objects.create_superuser('admin', 'admin@example.com', 'pass')
        self.assertIsNotNone(superuser)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        
    # Verifica se URl está resolvida
    def test_gamelist_is_resolved(self):
        url = reverse('game-list')
        self.assertEquals(resolve(url).func, gameList)