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

    def __str__(self):
        return self.nick


class Photo(models.Model):
    title = models.CharField(max_length=255)
    path = models.ImageField(upload_to='images')
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser, related_name='photos', verbose_name='Użytkownik', on_delete=models.CASCADE)
    blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Zdjęcie"
        verbose_name_plural = "Zdjęcia"

    def __str__(self):
        return self.title


class Likes(models.Model):
    user = models.ForeignKey(MyUser, related_name="likes", on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, related_name="likes", on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(MyUser, related_name='comments', verbose_name='Użytkownik', on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, related_name='comments', verbose_name='Zdjęcie', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Komentarz"
        verbose_name_plural = "Komentarze"

    def __str__(self):
        return '{}...'.format(self.content[:15]) if len(self.content) > 15 else self.content