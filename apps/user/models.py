from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy

# Other apps models or Abstract models
from apps.common.models import BaseModel
from apps.common.models import CustomID

# Third party app/packages fields
from phonenumber_field.modelfields import PhoneNumberField

# uploaded file path
from apps.user.utils import user_directory_path

# Custom Validator
from apps.user.utils import validate_image_dimention as custom_size
from apps.user.utils import validate_image_type as custom_type

# Create your models here.
class MyUserManager(BaseUserManager):

    """A custom manager to deal with emails and custom identifiers"""

    def _create_user(self, email, password, **extra_fields):
        """A custom manager to deal with emails and custom identifiers"""
        if not email:
            raise ValueError('Users must have an email address')
    
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("superuser must have is_staff=True")
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser=True')
        
        return self._create_user(email, password, **extra_fields)


class User(CustomID, BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    contact_number = PhoneNumberField(verbose_name=gettext_lazy("Contact Number"), unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True)


    is_moderator = models.BooleanField(
        gettext_lazy('modarator'), default=False,
        help_text=gettext_lazy('designates whether the user can review and post'),
    )
    
    is_staff = models.BooleanField(
        gettext_lazy('staff_status'), default=False,
        help_text=gettext_lazy('designates whether the user can login to this site'),
    )

    is_active = models.BooleanField(
        gettext_lazy('active'), default=True,
        help_text=gettext_lazy('designates whether the user can loin to this site'),
    )

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    class Meta:
        verbose_name = gettext_lazy('user')
        verbose_name_plural = gettext_lazy('users')
        permissions = (
            ("can_login_web", "To Login Webpanel"),
            ("can_login_app", "To Login App"),
        )

    @property
    def date_joined(self):
        return self.created_at

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email