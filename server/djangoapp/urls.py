# server/djangoapp/urls.py
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('', TemplateView.as_view(template_name='Home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='About.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='Contact.html'), name='contact'),

    path('djangoapp/login', views.login_user),
    path('djangoapp/logout', views.logout_user),
    path('djangoapp/register', views.register_user),
]