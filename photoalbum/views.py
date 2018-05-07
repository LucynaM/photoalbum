from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse, HttpResponseBadRequest

from .models import Photo, MyUser, Likes
from .forms import PhotoForm, SignUpForm, LogInForm

# Create your views here.

class MainView(View):
    def get_all_photos(self, request):
        user = MyUser.objects.get(pk=request.user.id)
        photos = Photo.objects.all().order_by('creation_date')
        for photo in photos:
            if photo.likes.filter(user=user).count() > 0:
                photo.user_already_liked = True
        return photos

    def get(self, request):
        form = PhotoForm()
        #photos = Photo.objects.all().order_by('creation_date')
        photos = self.get_all_photos(request)
        ctx = {
            'form': form,
            'photos': photos,
        }
        return render(request, 'photoalbum/main.html', ctx)

    def post(self, request):
        print(request.user.id)
        user = MyUser.objects.get(pk=request.user.id)
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            Photo.objects.create(user=user, **form.cleaned_data)
        photos = self.get_all_photos(request)
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

class LogInView(View):
    def get(self, request):
        form = LogInForm()
        ctx = {
            'form': form,
        }
        return render(request, 'photoalbum/login.html', ctx)

    def post(self, request):
        form = LogInForm(request.POST)
        msg = ""
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('main')
            else:
                msg = "Błędny użytkownik lub hasło"
        ctx = {
            'msg': msg,
            'form': form,
        }
        return render(request, 'photoalbum/login.html', ctx)


def logout_user(request):
    logout(request)
    return redirect('login')



class UserDetails(View):
    def get(self, request):
        user = MyUser.objects.get(pk=request.user.id)
        user_photos = user.photos.all().order_by('creation_date')


def ajax_counter(request):
    if request.method == "GET":
        try:
            counter = int(request.GET['counter'])
            photo_id = int(request.GET['photo_id'])
            photo = Photo.objects.get(pk=photo_id)
            user_id = int(request.GET['user'])
            user = MyUser.objects.get(pk=user_id)
            if counter == 1:
                Likes.objects.create(photo=photo, user=user)
            else:
                like = Likes.objects.get(photo=photo, user=user)
                like.delete()
            photo_likes = photo.likes.count()
            print(photo_likes)
            data = {
                'id': photo.id,
                'photo_likes': photo_likes,
            }
            return JsonResponse(data)
        except Exception as e:
            print(e)

    else:
        return HttpResponseBadRequest()