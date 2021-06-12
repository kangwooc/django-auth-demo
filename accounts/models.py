from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
import uuid

GENDER_SELECTION = [
    ('M', 'Male'),
    ('F', 'Female'),
]

def default_place_pics():
    return "static/img/default_profile_pic.png"


class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(_('email address'), unique=True)
    nickname = models.CharField(
        _('nickname'),
        max_length=20
    )
    gender = models.CharField(_('gender'), max_length=10, choices=GENDER_SELECTION)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'gender']

    objects = CustomUserManager()
    
    is_subscribed = models.BooleanField(default=False)
    profile_image = models.ImageField(_('profile_image'), null=True, blank=True, default=default_place_pics)
    user_md_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.nickname
