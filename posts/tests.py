from django.test import Client, TestCase

# from unittest import TestCase
from posts.models import Group


class TestClientMixin:
    def setUp(self) -> None:
        self.client = Client()

    def tearDown(self) -> None:
        print("The end")


class TestStringMethods(TestCase):
    def test_length(self):
        self.assertEqual(len('yatybe'), 6)

    def test_show_msg(self):
        # действительно ли первый аргумент — True?
        self.assertTrue(False, msg="Важная проверка на истинность")


class TestIndexPage(TestClientMixin, TestCase):
    def test_index_available(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(Client.get('/').status_code, 200)


class TestGroups(TestClientMixin, TestCase):
    def test_page_not_found(self):
        response = self.client.get('/groups/not_exist')
        self.assertEqual(response.status_code, 404)

    def test_exists_group(self):
        Group.objects.create(title='test', slug='test-group', description='empty')
        response = self.client.get('/group/test-group/')
        self.assertEqual(response.status_code, 200)
