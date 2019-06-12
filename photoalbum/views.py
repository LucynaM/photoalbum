from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest

from .models import Photo, MyUser, Likes, Comment
from .forms import PhotoForm, SignUpForm, LogInForm, CommentForm

# Create your views here.


class MainView(LoginRequiredMixin, View):
    """Main page dispalying all photos available in service"""
    def get_all_photos(self, request):
        user = MyUser.objects.get(pk=request.user.id)
        photos = Photo.objects.all().order_by('creation_date')
        for photo in photos:
            if photo.likes.filter(user=user).count() > 0:
                photo.user_already_liked = True
        return photos

    def get(self, request):
        form = PhotoForm()
        photos = self.get_all_photos(request)
        ctx = {
            'form': form,
            'photos': photos,
        }
        return render(request, 'photoalbum/main.html', ctx)

    def post(self, request):
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
    """Registration page"""
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


class EditUser(LoginRequiredMixin, View):
    """User details to change"""

    def get(self, request):
        user = MyUser.objects.get(pk=request.user.id)
        form = SignUpForm(instance=user)
        ctx = {
            'form': form,
        }
        return render(request, 'photoalbum/edit_user.html', ctx)

    def post(self, request):
        user = MyUser.objects.get(pk=request.user.id)
        form = SignUpForm(request.POST, instance=user)
        if form.is_valid():
            user.username = form.cleaned_data['email']
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            logout(request)
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
        return redirect('main')


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



class UserDetails(LoginRequiredMixin, View):
    """User page displaying all his photos"""
    def get(self, request):
        user = MyUser.objects.get(pk=request.user.id)
        user_photos = user.photos.all().order_by('creation_date')
        ctx = {
            'user_photos': user_photos,
        }
        return render(request, 'photoalbum/user_photos.html', ctx)


class PhotoDetails(LoginRequiredMixin, View):
    """Single photo details with comments handling"""
    def get(self, request, photo_id):
        photo = Photo.objects.get(pk=photo_id)
        form = CommentForm()
        comments = photo.comments.all()
        ctx = {
            'photo': photo,
            'form': form,
            'comments': comments,
        }
        return render(request, 'photoalbum/photo_details.html', ctx)

    def post(self, request, photo_id):
        photo = Photo.objects.get(pk=photo_id)
        user = MyUser.objects.get(pk=request.user.id)
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(user=user, photo=photo, **form.cleaned_data)
        comments = photo.comments.all()
        ctx = {
            'photo': photo,
            'form': form,
            'comments': comments,
        }
        return render(request, 'photoalbum/photo_details.html', ctx)


# update likes count on user click
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
            data = {
                'id': photo.id,
                'photo_likes': photo_likes,
            }
            return JsonResponse(data)
        except Exception as e:
            print(e)

    else:
        return HttpResponseBadRequest()