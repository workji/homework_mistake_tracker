from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('diary/', include('diary.urls')),
    path('chat/', include('chatai.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
