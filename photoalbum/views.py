from django.shortcuts import render
from django.views import View

from .models import Photo
from .forms import PhotoForm

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
