from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.auth_token.models import AccessToken
from apps.user.models import User

def create_token(user: User):
    if not user.is_active:
        raise ValidationError(_("User is not active"))
    
    token = AccessToken(user=user)
    token.save()
    return token.token
