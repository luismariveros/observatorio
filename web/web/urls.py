"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from django.conf.urls.static import static


from backend import views
from . import settings

urlpatterns = [
    #url('^', include('django.contrib.auth.urls')),
    url(r'^login/', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^cambiar-password/', auth_views.PasswordChangeView.as_view(success_url='/backend'), name='change'),
    url(r'^admin/', admin.site.urls),
    url(r'^backend/', include('backend.urls')),
    url(r'^', include('www.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)