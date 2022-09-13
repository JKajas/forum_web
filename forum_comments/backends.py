import datetime
import os

from django.contrib.auth.backends import BaseBackend
from django.core.mail.backends.filebased import EmailBackend

from forum_comments.models import UserModel

"""
Simple backend to authenticate user. If user is member of organization
could be log in entering only alias from email(email is login)
"""


class UserBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        loginobj = UserModel.objects.filter(email__startswith=email)
        for users in loginobj:
            if users.organization_id is not None:
                pass_valid = users.check_password(password)
                if pass_valid:
                    user = UserModel.objects.get(username=users.username)
                    return user
            else:
                try:
                    user = UserModel.objects.get(email=email)
                    pass_vaild = user.check_password(password)
                    if pass_vaild:
                        return user
                    else:
                        return None
                except:
                    return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except:
            UserModel.DoesNotExist
            return None


"""
Corrected EmailBackand saving emails for dev environment in .eml format
"""


class NewEmailBackend(EmailBackend):
    def _get_filename(self):
        """Return a unique file name."""
        if self._fname is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            fname = "%s-%s.eml" % (timestamp, abs(id(self)))
            self._fname = os.path.join(self.file_path, fname)
        return self._fname
