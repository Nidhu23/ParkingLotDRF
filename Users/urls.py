from django.urls import path
from Users import views

urlpatterns = [
    path('register/', views.register),
    path('login/',
         views.Login().as_view()),
    path('logout', views.logout)
]