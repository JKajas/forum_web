from django.conf import settings
from django.contrib.auth.models import Permission
from django.test import RequestFactory, TestCase

from forum_comments import models, views

'''
Simple unit test checking creating process of user, allowed hosts, 
and view with login required decorator

'''
class TestUserManager(TestCase):
    def test_creation(self):
        new_user = models.UserModel.objects.create_user(
            email = 'example@example.pl',
            username = 'example',
            password= 'examplepassword'
            )
        self.assertEqual(new_user.email, 'example@example.pl')
        self.assertEqual(new_user.username, 'example')
        self.assertEqual(True, new_user.check_password('examplepassword'))
    def test_creaton_superuser(self):
        new_user = models.UserModel.objects.create_superuser(
            email = 'example@example.pl',
            username = 'example',
            password= 'examplepassword'
           )
        self.assertEqual(new_user.has_perm('forum_comments.add_usermodel'), True )
        self.assertEqual(new_user.has_perm('forum_comments.add_organizationmodel'), False)


class TestRequestRedirection(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = models.UserModel.objects.create_user(
            email = 'example@example.pl',
            username = 'example',
            password= 'examplepassword'
        )
    def test_loginrequire(self):
        request = self.factory.get('/profile/%s/' % self.user)
        request.user = self.user
        response = views.profile(request)
        self.assertEqual(response.status_code, 200)

class TestHost(TestCase):
    def test_host(self):
        response = self.client.get('', HTTP_HOST=settings.ALLOWED_HOSTS[0])
        self.assertEqual(response.status_code, 200)
