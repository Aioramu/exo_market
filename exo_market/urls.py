from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('personality.urls')),
    path('', include('announcement.urls')),
    path('admin/', admin.site.urls),
]
