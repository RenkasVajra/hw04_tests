from django.contrib.auth import get_user_model
from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import get_object_or_404

from posts.models import Post, Group


User = get_user_model()

class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='IvanIvanov')
        cls.authorized_client = Client()        
        cls.authorized_client.force_login(cls.user)
        cls.unauthorized_client = Client()
    
    def test_profie(self,username):
        response = self.authorized_client.get(reverse('profile',kwargs={'username':self.user.username}))
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context["author"].username, self.user.username)
        self.assertEqual(response.context["author"].username, self.user.username)

    def test_new_post(self):
        new_post = self.authorized_client.post(
            reverse("new_post"), 
                  {"text": "Это текст публикации", 
                   "group": "Shikama"}, 
            follow=True
        )
        response = self.authorized_client.get("/")
        self.assertContains(
            response, 
            text="Это текст публикации",
            msg_prefix=("Новый пост не отображается на главной странице (index)"),
        )

    def test_published_post(self):
        client = Client()
        user = User.objects.create_user(username="StasBoretskiy",password="ArmorUnit")
        client.force_login(user)
        response = client.post('/new/',
                              {'text':'Read this pls'},
                              follow=True,
        )
        response = client.get('/index/')
        post = Post.objects.get(author=user)
        post_id = post.pk
        self.assertContains(response, post_id)

    def test_post_edit(self):
        text = 'Возможно отредактированный текст из-за очепятки'
        response = self.authorized_client.post("/new/",
                                                "text":text,
                                                follow=True
        )
        self.assertEqual(response.status_code, 200)
        post = Post.objects.get(text=text)
        edit_text="Отредактированный текст"
        editing_post = self.authorized_client.post(f"{post.author.username}/{post.id}/edit/",
                                                      {"text":edit_text},
                                                      follow=True,
        )
        post = Post.objects.get(text=edit_text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.text, edit_text, 'Функция post_edit работает неправильно')


