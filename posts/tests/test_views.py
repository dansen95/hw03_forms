from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms  

from posts.models import Post, Group


#User = get_user_model()

class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):        
        super().setUpClass()     
        User = get_user_model()
        cls.user = User.objects.create(username='testuser')

        cls.group = Group.objects.create(
                title="Тестовый заголовок",
                slug="test_slug",
        )

        cls.group_01 = Group.objects.create(
                title="Тестовая группа",
                slug="test_slug_1",
        )

        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=PostModelTest.user,
            group=PostModelTest.group,
            pub_date="20.10.2020" 
        )

    def setUp(self):
        """ Create authorized client """
        self.authorized_client = Client()
        self.authorized_client.force_login(PostModelTest.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # шаблон страны: название приложения с views файлом 
        # для обращения к классам или методам отображения
        templates_pages_names = {
            'posts/index.html': reverse('index'),
            'posts/new_post.html': reverse('new_post'),
            'group.html': reverse('group', kwargs={'slug': 'test_slug'}),
        }
        # Проверяем, что при обращении к name вызывается 
        # соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
    
    def test_home_page_show_correct_context(self):
        """Шаблон home сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('index'))
        post_text_0 = response.context.get('page')[0].text 
        self.assertEqual(post_text_0, PostModelTest.post.text)
        post_pub_date_0 = response.context.get('page')[0].pub_date
        self.assertEqual(post_pub_date_0, PostModelTest.post.pub_date)
        post_author_0 = response.context.get('page')[0].author
        self.assertEqual(post_author_0, PostModelTest.post.author)
        post_group_0 = response.context.get('page')[0].group
        self.assertEqual(post_group_0, PostModelTest.post.group)

    def test_group_page_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('group', kwargs={'slug': 'test_slug'}))
        self.assertEqual(response.context.get('group').title, PostModelTest.group.title)
        self.assertEqual(response.context.get('group').slug, PostModelTest.group.slug)
    
    def test_new_post_page_show_correct_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_post'))
        # Список ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {
            "group": forms.fields.ChoiceField,
            "text": forms.fields.CharField,
        }
        
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)  

    def test_new_post_that_is_not_in_group_01(self):
        response = self.authorized_client.get(reverse('group', kwargs={'slug': 'test_slug_1'}))
        self.assertIsNone(response.context.get('post'))
