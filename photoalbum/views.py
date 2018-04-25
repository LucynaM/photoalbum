from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate

from .models import Photo, MyUser
from .forms import PhotoForm, SignUpForm

# Create your views here.

class MainView(View):
    def get(self, request):
        form = PhotoForm()
        photos = Photo.objects.all().order_by('creation_date')
        ctx = {
            'form': form,
            'photos': photos,
        }
        return render(request, 'photoalbum/main.html', ctx)

    def post(self, request):
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        photos = Photo.objects.all().order_by('creation_date')
        ctx = {
            'form': form,
            'photos': photos,
        }
        return render(request, 'photoalbum/main.html', ctx)


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        ctx = {
            'form': form
        }
        return render(request, 'photoalbum/signup.html', ctx)

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop('password2')
            user = MyUser.objects.create_user(username=form.cleaned_data['email'], **form.cleaned_data)
            login(request, user)
            return redirect('main')
        ctx = {
            'form': form,
        }
        return render(request, 'photoalbum/signup.html', ctx)
