from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('company/', include('company.urls', namespace='company')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)