from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class User(AbstractUser):
    GENDER = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE')
    )
    username = models.CharField(max_length=20, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=50, blank=True, null=True, unique=True)

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    nationality = models.CharField(max_length=50, blank=True, null=True)
    national_id_number = models.CharField(max_length=50, blank=True, null=True)

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True, null=True, choices=GENDER)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    socials = models.ManyToManyField('UserSocials', blank=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return f'{self.username}'


class UserSocials(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    link = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.link}'
