from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.views import handler404

urlpatterns = [
    path('admin/marwaneMezzane/Coding/debug/makeiteasy/controle/', admin.site.urls),
    path('', include('app.urls')),
]

# Add static and media URLs for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'app.views.handler404'


