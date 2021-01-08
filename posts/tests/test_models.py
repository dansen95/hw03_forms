from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from posts.models import Post, Group


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        cls.user = User.objects.create(username='testuser')
        
        cls.group =Group.objects.create(
                title="тестовый заголовок",
                slug="test_slug",
            )
        
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=PostModelTest.user,
            group=PostModelTest.group,
            pub_date="20.10.2020" 
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(PostModelTest.user)
        # Сохраняем созданную запись в качестве переменной класса
        #cls.task = Post.objects.get(slug='test-task')

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        task = PostModelTest.post
        field_verboses = {
            
            'text': 'Текст',
            
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        task = PostModelTest.post
        field_help_texts = {
            #'title': 'Дайте короткое название задаче',
            'text': 'Заполнить',
            #'slug': ('Укажите адрес для страницы задачи. Используйте '
            #         'только латиницу, цифры, дефисы и знаки '
            #         'подчёркивания'),
            #'image': 'Загрузите картинку',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).help_text, expected)

    def test_object_name_is_title_fild(self):
        """__str__  task - это строчка с содержимым task.title."""
        task = PostModelTest.post
        expected_object_name = task.text
        self.assertEquals(expected_object_name, str(task))


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        cls.user = User.objects.create(username='testuser')
        
        cls.group =Group.objects.create(
                title="Тестовый заголовок",
                slug="test_slug",
            )

        
    def setUp(self):
        # Создаем неавторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(GroupModelTest.user)
        # Сохраняем созданную запись в качестве переменной класса
        #cls.task = Post.objects.get(slug='test-task')

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        task = GroupModelTest.group
        field_verboses = {
            
            'title': 'Группа',
            
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        task = GroupModelTest.group
        field_help_texts = {
            #'title': 'Дайте короткое название задаче',
            'title': 'Выбрать группу',
            #'slug': ('Укажите адрес для страницы задачи. Используйте '
            #         'только латиницу, цифры, дефисы и знаки '
            #         'подчёркивания'),
            #'image': 'Загрузите картинку',
        }

        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).help_text, expected)

    def test_object_name_is_title_fild(self):
        """__str__  task - это строчка с содержимым task.title."""
        task = GroupModelTest.group
        expected_object_name = task.title
        self.assertEquals(expected_object_name, str(task))