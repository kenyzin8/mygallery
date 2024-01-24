
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('get-image-preview/', get_image_preview, name='get-image-preview'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)