from django.contrib.auth.models import User
from django.test import Client, TestCase

# from posts.factories import GroupFactory
from posts.models import Group, Post


class TestIndexPage(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_index_available(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class TestGroups(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def tearDown(self) -> None:
        Group.objects.filter(slug='first_group').delete()

    def test_page_not_found(self):
        response = self.client.get('/group/not_exist/')
        self.assertEqual(response.status_code, 404)

    # def test_exists_group(self):
    #     GroupFactory(slug='first_group')
    #     response = self.client.get('/group/first_group')
    #     self.assertEqual(response.status_code, 200)


class TestPosts(TestCase):
    def setUp(self) -> None:
        self.auth_client = Client()
        user = User.objects.create(username='test_user', email='q@q.com')
        user.set_password('123')
        user.save()
        self.auth_client.login(username='test_user', password='123')

    def tearDown(self) -> None:
        Group.objects.filter(
            title='test',
            slug='first_group',
            description='empty'
        ).delete()

        User.objects.filter(username='test_user').delete()

    def test_valid_form(self):
        group = Group.objects.create(
            title='test',
            slug='first_group',
            description='empty'
        )
        group_id = f'{group.id}'
        self.auth_client.post(
            '/new/',
            data={
                'text': 'test text',
                'group': group_id
            }
        )

        self.assertTrue(
            Post.objects.filter(text='test text', group=group_id).exists()
        )

    def test_form_not_valid(self):
        response = self.auth_client.post(
            '/new/',
            data={
                'group': '100500'
            }
        )

        self.assertFormError(
            response,
            form='form',
            field='text',
            errors=['Обязательное поле.']
        )
