from django.contrib.auth import get_user_model
from django.http import response
from django.test import TestCase, Client

from posts.models import Post, Group


class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()

    def test_homepage(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get('/')  
        self.assertEqual(response.status_code, 200)

    def test_about_author(self):
        response = self.guest_client.get('about_author/')
        self.assertEqual(response.status_code, 404)

    def test_techonologies(self):
        response = self.guest_client.get('techonologies/')
        self.assertEqual(response.status_code, 404)



class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        cls.user = User.objects.create(username='AndreyG')
        cls.group =Group.objects.create(
                slug="test_slug",
            )
        

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        #self.user = get_user_model().objects.create(username='AndreyG')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_post_group_slug_url_exists_at_desired_location(self):
        """Страница /group/test_slug/ доступна любому пользователю."""
        response = self.guest_client.get('/group/test_slug')
        self.assertEqual(response.status_code, 200)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_post_new_url_exists_at_desired_location(self):
        """Страница /new/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'posts/index.html': '/',
            'posts/new_post.html': '/new/',
            'group.html': '/group/test_slug',
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)