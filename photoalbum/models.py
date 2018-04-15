from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    @property
    def nick(self):
        return self.email[:self.email.index('@')].title()

    class Meta:
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"