from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # páginas estáticas
    path('', TemplateView.as_view(template_name='Home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='About.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='Contact.html'), name='contact'),

    # endpoints de autenticación
    path('djangoapp/login', views.login_user),
    path('djangoapp/logout', views.logout_user),
    path('djangoapp/register', views.register_user),

    # endpoint de Proyecto 4
    path('get_cars', views.get_cars, name='get_cars'),
]