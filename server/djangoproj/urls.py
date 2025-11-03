from django.contrib import admin
from django.urls import path, include
from django.views.static import serve as static_serve
from django.conf import settings
import os

def serve_spa(request):
    # Sirve el index.html del build sin pasar por el loader de plantillas
    return static_serve(
        request,
        path='index.html',
        document_root=os.path.join(settings.BASE_DIR, 'frontend', 'build')
    )

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de la SPA (React) — login y register
    path('login/', serve_spa),
    path('register/', serve_spa),

    # Rutas Django de la app (Home/About/Contact y endpoints JSON)
    path('', include('djangoapp.urls')),
]