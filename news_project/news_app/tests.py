from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import News, Comment

class NewsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.news = News.objects.create(
            title='Тестовая новость',
            content='Содержание новости',
            author=self.user
        )

    def test_news_creation(self):
        self.assertEqual(self.news.title, 'Тестовая новость')
        self.assertEqual(self.news.author.username, 'testuser')
        self.assertTrue(isinstance(self.news, News))
        self.assertEqual(str(self.news), 'Тестовая новость')


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.news = News.objects.create(
            title='Тестовая новость',
            content='Содержание новости',
            author=self.user
        )
        self.comment = Comment.objects.create(
            user=self.user,
            news=self.news,
            text='Комментарий к новости'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.text, 'Комментарий к новости')
        self.assertEqual(self.comment.user.username, 'testuser')
        self.assertEqual(str(self.comment), 'testuser - Тестовая новость')


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.news = News.objects.create(
            title='Тестовая новость',
            content='Содержание новости',
            author=self.user
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_news_list_view(self):
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_list.html')

    def test_news_detail_view(self):
        response = self.client.get(reverse('news_detail', args=[self.news.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_detail.html')

