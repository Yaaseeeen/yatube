# import factory
# from django.contrib.auth.models import User
#
# from posts.models import Group
#
#
# class UserFactory(factory.DjangoModelFactory):
#     class Meta:
#         model = User
#
#     username = factory.Sequence(lambda n: f'ivan-{n}')
#     first_name = factory.Sequence(lambda n: f'ivan-{n}')
#     email = factory.Sequence(lambda n: f'ivan-{n}@yandex.ru')
#
#
# class GroupFactory(factory.DjangoModelFactory):
#     class Meta:
#         model = Group
#
#     title = 'Test title'
#     slug = factory.Sequence(lambda x: f'group_{x}')
#     description = 'empty'
