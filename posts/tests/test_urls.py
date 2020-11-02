from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Post


User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.unauthorized_client = Client()

    def authorized_user(self):
        user = User.objects.create_user(username='StasBasov')
        authorized_client = Client()        
        authorized_client.force_login(user)

    def test_homepage(self):
        response = self.unauthorized_client.get('/')
        self.assertEqual(response.status_code, 200)
