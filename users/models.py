from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    '''Custom user class with email as a unique identifier instead of username'''
    username = None
    email = models.EmailField('email address', unique=True)
    
    # unique identifier
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return " ".join((self.first_name, self.last_name))

def get_sentinel_user():
    """Get or create a user to replace deleted users as foreign key"""
    return CustomUser.objects.get_or_create(email='deleted@user.com')[0]
