from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from django.conf.urls.static import static

from . import settings

urlpatterns = [
    url(r'^login/', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^backend/', include('backend.urls')),
    url(r'^', include('www.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
