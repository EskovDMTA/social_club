import time

from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Posts, Follow


class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='Terminator3', email='terminator@mail.ru',
                                              password='Terminator')
        print('Start')

    def test_profile(self):
        response = self.client.get('/Terminator3/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get('/new/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/new/')

    def test_new_post(self):
        self.client.login(username='Terminator3', password='Terminator', follow=True)
        response = self.client.post('/new/', {'text': 'Try to make a post'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_after_publisher(self):
        self.client.login(username='Terminator3', password='Terminator', follow=True)
        post = Posts.objects.create(text='Текст из пятого теста', author=self.user1)
        for url in (reverse('profile', kwargs={'username': 'Terminator3', }), reverse('index'),
                    reverse('post', kwargs={'username': 'Terminator3', 'post_id': post.id})):
            response = self.client.get(url)
            self.assertContains(response, text='Текст из пятого теста')

    def test_post_edit(self):
        self.client.login(username='Terminator3', password='Terminator', follow=True)
        post = Posts.objects.create(text='Текст который будет редактироваться', author=self.user1)
        self.client.post(reverse('post_edit', kwargs={'username': 'Terminator3', 'post_id':
            post.id}), {'text': 'Попытались отредактировать пост'})
        for url in (reverse('profile', kwargs={'username': 'Terminator3', }), reverse('index'),
                    reverse('post', kwargs={'username': 'Terminator3', 'post_id': post.id})):
            response = self.client.get(url)
            self.assertContains(response, text='Попытались отредактировать пост')

    def tearDown(self):
        User.objects.filter(username='Terminator3').delete()
        print('End')


class Test_page(TestCase):
    def setUp(self):
        self.client = Client()
        print('StartSprint_6')

    def test_check_404(self):
        response = self.client.get('/pagepage/')
        self.assertEqual(response.status_code, 404)
        print('check')

    def tearDown(self):
        print('EndSprint6')


class Test_image(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='Terminator3', email='terminator@mail.ru',
                                              password='Terminator')
        self.client.login(username='Terminator3', password='Terminator', follow=True)
        print('Test Image')

    def test_imgfound(self):
        self.user1 = User.objects.create_user(username='Terminator3', email='terminator@mail.ru',
                                              password='Terminator')
        self.client.login(username='Terminator3', password='Terminator', follow=True)
        with open('posts/media/about_me.jpg', 'rb') as img:
            # post = Posts.objects.create(text='Текст который будет редактироваться',
            #                           author=self.user1, image=img)
            self.client.post(reverse('new_post'), {'text': 'Check test_imgfound', 'image': img },
                             follow=True)
            post_id = Posts.objects.get(pk=1)

            for url in (reverse('profile', kwargs={'username': 'Terminator3', }), reverse('index'),
                        reverse('post', kwargs={'username': 'Terminator3', 'post_id':
                            post_id.pk})):
                response = self.client.get(url)
                self.assertContains(response, text='<img')

    def tearDown(self):
        print('Test Image End')


class Test_casher(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='Terminator3', email='terminator@mail.ru',
                                              password='Terminator')
        print('start')

    def test_cash(self):
        self.client.login(username='Terminator3', password='Terminator', follow=True)
        response = self.client.get(reverse('index'))
        Posts.objects.create(text='Текст которым тестирую кэш', author=self.user1)
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, text='Текст которым тестирую кэш')
        cache.clear()
        response = self.client.get(reverse('index'))
        self.assertContains(response, text='Текст которым тестирую кэш')

    def tearDown(self):
        print('Test cash End')


class Test_follow(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user1 = User.objects.create_user(username='Terminator3', email='terminator@mail.ru',
                                              password='Terminator')
        self.user2 = User.objects.create_user(username='Bond', email='Bond@mail.ru',
                                              password='Bond')
        self.user3 = User.objects.create_user(username='IronMan', email='IronMan@mail.ru',
                                              password='IronMan')
        self.login = self.client.login(username='Terminator3', password='Terminator', follow=True)
        self.login2 = self.client.login(username='IronMan', password='IronMan',
                                        follow=True)
        self.post = Posts.objects.create(text='Текст для проверки подписки', author=self.user2)


    def test_follow_unfollow(self):
        self.login
        self.client.get(reverse('profile_follow', kwargs={'username': 'Bond', }))
        self.assertEqual(1, Follow.objects.filter(author=self.user2).count())
        self.client.get(reverse('profile_unfollow', kwargs={'username': 'Bond', }))
        self.assertEqual(0, Follow.objects.filter(author=self.user2).count())

    def test_new_post(self):
        self.login
        self.client.get(reverse('profile_follow', kwargs={'username': 'Bond', }))
        self.post
        response = self.client.get(reverse('follow_index'))
        self.assertContains(response, text='Текст для проверки подписки')
        self.login2
        response = self.client.get(reverse('follow_index'))
        self.assertNotContains(response, text='Текст которым тестирую кэш')

    def test_auth_comment(self):
        self.login
        self.client.post(reverse('add_comment', kwargs={'username': 'Bond', 'post_id':
                                    self.post.pk}), {'text': 'Добавляю комментарий'})
        response = self.client.get(reverse('add_comment', kwargs={'username': 'Bond', 'post_id':
                                    self.post.pk}))
        self.assertContains(response, text='Добавляю комментарий')
        self.client.logout()
        response = self.client.get(reverse('add_comment', kwargs={'username': 'Bond', 'post_id':
            self.post.pk}), follow=True)
        self.assertRedirects(response, '/auth/login/?next=/Bond/1/')

    def tearDown(self):
        print('Test follow end')
