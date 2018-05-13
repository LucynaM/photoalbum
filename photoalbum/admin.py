from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Photo, Comment, Likes
# Register your models here.


def block_elements(model_admin, request, query_set):
    query_set.update(blocked=True)

block_elements.short_description = 'Zablokuj'

def unblock_elements(model_admin, request, query_set):
    query_set.update(blocked=False)

unblock_elements.short_description = 'Odblokuj'


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ('nick',)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'blocked',)
    actions = (block_elements, unblock_elements,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'photo', 'user', 'blocked',)
    actions = (block_elements, unblock_elements,)

