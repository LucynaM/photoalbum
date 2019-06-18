from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Photo, MyUser, Likes, Comment
from .forms import PhotoForm, SignUpForm, LogInForm, CommentForm

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

from random import shuffle

# Create your views here.


class MainView(LoginRequiredMixin, View):
    """Main page dispalying all photos available in service"""
    @staticmethod
    def process_photos_with_likes(request):
        user = MyUser.objects.get(pk=request.user.id)
        photos = Photo.objects.all().order_by('-creation_date')
        for photo in photos:
            if photo.likes.filter(user=user).count() > 0:
                photo.user_already_liked = True
        return photos

    def get(self, request):
        form = PhotoForm()
        photos = self.process_photos_with_likes(request)

        ctx = {
            'form': form,
            'photos': photos,
        }
        return render(request, 'photoalbum/main.html', ctx)

    def post(self, request):
        user = MyUser.objects.get(pk=request.user.id)
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():

            photo = form.save(commit=False)
            photo.user = user

            # open uploaded file to process it
            scr = Image.open(request.FILES['path'])
            file_name = request.FILES['path'].name

            #check original orientation settings
            orientation = 274
            try:
                exif = scr._getexif()
                if exif:
                    exif = dict(exif.items())
                    if exif[orientation] == 3:
                        scr = scr.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        scr = scr.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        scr = scr.rotate(90, expand=True)
            except:
                # There is AttributeError: _getexif sometimes.
                pass

            #save orientation info and prepare resized img
            w, h = scr.size
            photo.orientation = 'landscape'
            new_w, new_h = 900, int(h / (w / 900))

            if w < h:
                photo.orientation = 'portrait'
                new_w, new_h = 600, int(h / (w / 600))

            img_resized = scr.resize((new_w, new_h),Image.ANTIALIAS)

            # save compressed/rotated/converted img in its original size as path
            with BytesIO() as img_io:
                scr.save(img_io, format='JPEG', optimize=True, quality=80)
                pillow_image = ContentFile(img_io.getvalue())
                photo.path = InMemoryUploadedFile(pillow_image, None, file_name, 'image/jpeg',
                                                             pillow_image.tell, None)

            # save compressed/rotated/converted and resized(!) img as path_to_resized
            with BytesIO() as img_resized_io:
                img_resized.save(img_resized_io, format='JPEG', optimize=True, quality=80)
                pillow_image = ContentFile(img_resized_io.getvalue())
                photo.path_to_resized = InMemoryUploadedFile(pillow_image, None, file_name, 'image/jpeg',
                                                             pillow_image.tell, None)

            photo.save()
            scr.close()

        form = PhotoForm()
        photos = self.process_photos_with_likes(request)
        ctx = {
            'form': form,
            'photos': photos,
        }
        return render(request, 'photoalbum/main.html', ctx)



class PhotoDetails(LoginRequiredMixin, View):
    """Single photo details with comments handling"""

    @staticmethod
    def process_photo_with_likes(request, photo_id):
        user = MyUser.objects.get(pk=request.user.id)
        photo = Photo.objects.get(pk=photo_id)
        if photo.likes.filter(user=user).count() > 0:
            photo.user_already_liked = True
        return photo

    def get(self, request, photo_id):
        photo = self.process_photo_with_likes(request, photo_id)
        form = CommentForm()
        comments = photo.comments.all()
        ctx = {
            'photo': photo,
            'form': form,
            'comments': comments,
        }
        return render(request, 'photoalbum/photo_details.html', ctx)

    def post(self, request, photo_id):

        photo = self.process_photo_with_likes(request, photo_id)
        user = MyUser.objects.get(pk=request.user.id)
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(user=user, photo=photo, **form.cleaned_data)
            form = CommentForm()
        comments = photo.comments.all()
        ctx = {
            'photo': photo,
            'form': form,
            'comments': comments,
        }
        return render(request, 'photoalbum/photo_details.html', ctx)



def ajax_counter(request):
    """update likes count on user click"""
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

class SignUpView(View):
    """Registration page"""

    @staticmethod
    def get_random_result():
        photos_all = Photo.objects.filter(orientation='landscape')
        random_list = list(range(photos_all.count()))
        shuffle(random_list)
        return (photos_all[i] for i in random_list[:2])

    def get(self, request):
        form = SignUpForm()
        photos = self.get_random_result()
        ctx = {
            'form': form,
            'photos': photos,
        }
        return render(request, 'photoalbum/signup.html', ctx)

    def post(self, request):
        form = SignUpForm(request.POST)
        photos = self.get_random_result()
        if form.is_valid():
            form.cleaned_data.pop('password2')
            user = MyUser.objects.create_user(username=form.cleaned_data['email'], **form.cleaned_data)
            login(request, user)
            return redirect('main')
        ctx = {
            'form': form,
            'photos': photos,
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
    @staticmethod
    def get_random_result():
        photos_all = Photo.objects.filter(orientation='landscape')
        random_list = list(range(photos_all.count()))
        shuffle(random_list)
        return (photos_all[i] for i in random_list[:2])


    def get(self, request):
        form = LogInForm()
        photos = self.get_random_result()
        ctx = {
            'form': form,
            'photos': photos,
        }
        return render(request, 'photoalbum/login.html', ctx)

    def post(self, request):
        form = LogInForm(request.POST)
        photos = self.get_random_result()

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
            'photos': photos,
        }
        return render(request, 'photoalbum/login.html', ctx)


def logout_user(request):
    logout(request)
    return redirect('login')



class UserDetails(LoginRequiredMixin, View):
    """User page displaying all his photos"""
    def get(self, request):
        user = MyUser.objects.get(pk=request.user.id)
        user_photos = user.photos.all().order_by('-creation_date')
        ctx = {
            'user_photos': user_photos,
        }
        return render(request, 'photoalbum/user_photos.html', ctx)
