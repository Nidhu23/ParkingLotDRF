from django.urls import path
from registration import views

urlpatterns = [
    path('register/', views.Register.as_view()),
]