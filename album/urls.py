"""album URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from photoalbum.views import MainView, SignUpView, LogInView, logout_user, ajax_counter, UserDetails, PhotoDetails, EditUser

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^login/$', LogInView.as_view(), name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^ajax_counter/$', ajax_counter, name='ajax_counter'),
    url(r'^user_photo/$', UserDetails.as_view(), name='user_photo'),
    url(r'^photo_details/(?P<photo_id>(\d)+)/$', PhotoDetails.as_view(), name='photo_details'),
    url(r'^edit_user/$', EditUser.as_view(), name='edit_user'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
