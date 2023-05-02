from django.contrib.auth.backends import ModelBackend
from apps.user.models import User

class MyAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = User
        users = UserModel.objects.filter(email=email)
        for user in users:
            if user.check_password(password):
                return user
        return None