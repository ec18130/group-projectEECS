from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from wpproject import settings

urlpatterns = [
    path('', include('djnews.urls')),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
