from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404 # Importante

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portafolio.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Manejador de error 404 (Asegúrate de cambiar 'portafolio' por el nombre real de tu carpeta de app)
handler404 = 'portafolio.views.error_404'