from django.urls import path
from registration import views

urlpatterns = [
    path('register/', views.Register.as_view()),
    path('login/',
         views.Login().as_view())
]