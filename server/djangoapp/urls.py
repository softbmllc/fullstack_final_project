from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Páginas estáticas / landing
    path('', TemplateView.as_view(template_name='Home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='About.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='Contact.html'), name='contact'),

    # Página de login (HTML)
    path('login/', views.login_page, name='login_page'),

    # Endpoints de autenticación (JSON)
    path('djangoapp/login', views.login_user),
    path('djangoapp/logout', views.logout_user),
    path('djangoapp/register', views.register_user),

    # Proyecto 4
    path('get_cars', views.get_cars, name='get_cars'),

    # Páginas dinámicas para dealer (DETALLE + FORM + SUBMIT)
    path('dealer/<int:dealer_id>', views.dealer_details_page, name='dealer_details'),
    path('dealer/<int:dealer_id>/review', views.add_review_form, name='add_review_form'),
    path('dealer/<int:dealer_id>/review/submit', views.post_review_view, name='post_review_view'),
]
