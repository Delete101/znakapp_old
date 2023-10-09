from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.urls import include


urlpatterns = [
    path('', views.index, name='homepage'),
    path('how-it-work/', views.how_it_work, name='how-it-work'),
    path('price-list/', views.price_list, name='price-list'),
    path('contacts/', views.contacts, name='contacts'),
    path('login/cabinet/<str:user_id>', views.cabinet, name='cabinet'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register_request, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('accounts/login/', LoginView.as_view()),
    path('login/cabinet/<str:user_id>/download/', views.download_images, name='download_images'),
    path('politica-confidincialnosti/', views.pol_sogl, name='pol_sogl'),
    path('politica-obrabotki/', views.pol_obr, name='pol_obr'),
    path('sposobi-oplati/', views.sposob_opl, name='sposob_opl'),
    path('checkout/<str:item>/', views.checkout_view, name='checkout'),
    path('oferta/', views.oferta, name='oferta')
]