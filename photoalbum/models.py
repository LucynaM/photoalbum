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


class Photo(models.Model):
    title = models.CharField(max_length=255)
    path = models.ImageField(upload_to='images')
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser, related_name='photos')


class Likes(models.Model):
    user = models.ForeignKey(MyUser, related_name="likes")
    photo = models.ForeignKey(Photo, related_name="likes")


class Comment(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(MyUser, related_name='comments')
    photo = models.ForeignKey(Photo, related_name='comments')
    creation_date = models.DateTimeField(auto_now_add=True)