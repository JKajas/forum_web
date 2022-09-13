from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from forum_comments.models import OrgUserModel


class Command(BaseCommand):
    def handle(self, **other):
        email = input("Email:")
        username = input("Username:")
        password = input("Password:")
        user = OrgUserModel.objects.create_superuser(email, username, password)
        self.stdout.write(
            self.style.SUCCESS('Successfully created user"%s"' % user)
        )
        # dopisac potwierdzenei wykonania operacji
