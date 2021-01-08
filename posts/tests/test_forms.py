from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from posts.forms import PostForm
from posts.models import Post, Group

class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        cls.user = User.objects.create(username='testuser')
        
        cls.group =Group.objects.create(
                title='Тестовый текст',
                slug='test_slug',
            )
        
        cls.post = Post.objects.create(
            text='Тестовый заголовок',
            author=PostCreateFormTests.user,
            group=PostCreateFormTests.group,
            pub_date='20.10.2020'
        )
        
        # Создаем форму, если нужна проверка атрибутов
        cls.form = PostForm()
        
    
    def setUp(self):
        # Создаем неавторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
    
    def test_create_task(self):
        """Валидная форма создает запись в Task."""
        # Подсчитаем количество записей в Task
        posts_count = Post.objects.count()
        form_data = {
            "text": "Тестовый заголовок",
            "group": PostCreateFormTests.group.id,
        }

        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, '/')
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count+1)
        # Проверяем, что создалась запись с нашим слагом
        #self.assertTrue(Post.objects.filter(slug='testovyij-zagolovok').exists())
