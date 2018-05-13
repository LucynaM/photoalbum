from django import forms
from django.core.exceptions import ValidationError
from .models import Photo, MyUser, Comment


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ['user', 'blocked']
        labels = {
            'path': '',
            'title': '',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'podaj tytuł',
            })
        }
        help_texts = {
            'path': '',
        }


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'password2']

    def clean(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise ValidationError
        return self.cleaned_data

class LogInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'photo', 'blocked']
        labels = {'content': ''}