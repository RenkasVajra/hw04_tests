from django.contrib.auth import get_user_model
from django.http import response
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Group, User


class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='IvanIvanov')
        cls.authorized_client = Client()        
        cls.authorized_client.force_login(cls.user)
        cls.unauthorized_client = Client()
        cls.group = Group.objects.create(title='TestGroup',
                                         slug='Group for test',
                                         description='Testing site elements')
        cls.post = Post.objects.create(text='Text text text',
                                       author=cls.user,
                                       group=cls.group,
                                       )

    def test_unauthorized_user(self):
        response = self.unauthorized_client.get('new_post')
        self.assertEqual(response.status_code, 404)

    def edit_forms(self, response, user, new_text, new_group):
        self.assertEqual(response.author, user)
        self.assertEqual(response.text, new_text)
        self.assertEqual(response.group, new_group)

    def test_new_post(self):
        count = Post.objects.count()
        response = self.authorized_client.post(reverse('new_post'),
                                              {'text':'Новый пост'},
                                              follow=True
    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(),count + 1)

    def test_show_edit(self):
        new = self.authorized_client.post(
            reverse('post_edit', args=(self.user.username, self.post.pk)),
            data={'text': 'new text', 'group': self.group.id},
            follow=True,
    )
        edit_post = self.authorized_client.post('/IvanIvanov/1/edit',
                                               {'text':self.post.text,'id':self.post.pk},
                  
                                               follow=True
    )
    
        urls = (reverse('index'),reverse('profile',kwargs={'username':self.user}),
                reverse('post',kwargs={'username':self.user,'post_id':self.post.pk}))
        for url in urls:
            print(url)
            response_authorized = self.authorized_client.get(url)
            response_unauthorized = self.unauthorized_client.get(url)
            self.assertContains(response_authorized,
                text = 'new text',
                msg_prefix=('the edited post is not displayed'
                            ' on the page for an authorized user'
    ))
            self.assertContains(response_unauthorized,
                text = 'new text',
                msg_prefix=('the edited post is not displayed'
                ' on the page for an unauthorized user'
    ))
