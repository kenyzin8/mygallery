
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('get-image-preview/', get_image_preview, name='get-image-preview'),
    path('ipon/privacy-policy/', privacy_policy, name='privacy-policy'),
    path('image-viewer-for-s3/privacy-policy/', s3_privacy_policy, name='s3-privacy-policy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)