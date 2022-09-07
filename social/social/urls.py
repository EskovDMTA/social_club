"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import path, include
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # admin section
    path('admin/', admin.site.urls),

    # registration and authorization
    path('auth/', include('Users.urls')),
    path('auth/', include('django.contrib.auth.urls')),

    # flatpages
    path('about/', include('django.contrib.flatpages.urls')),
    path('about-author/', views.flatpage, {'url': 'about-author/'}, name='about_author'),
    path('about-spec/', views.flatpage, {'url': 'about-spec/'}, name='about_spec'),

    # posts route
    path('', include('posts.urls')),

    # API Routes

    path('api/', include('SocialAPI.urls')),


]

handler404 = 'posts.views.page_not_found'

handler500 = 'posts.views.server_error'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)