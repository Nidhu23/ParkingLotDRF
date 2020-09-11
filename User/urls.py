from django.urls import path
from User import views

urlpatterns = [path('users/', views.UserList.as_view())]
