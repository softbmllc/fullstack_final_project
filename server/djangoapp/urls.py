from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', TemplateView.as_view(template_name='About.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='Contact.html'), name='contact'),
]
