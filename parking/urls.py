from django.urls import path
from parking import views

urlpatterns = [
    path('park-unpark/', views.Park.as_view()),
]
