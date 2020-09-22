from django.urls import path
from . import views

urlpatterns = [
    path('searchbynum/', views.vehicle_num_search),
    path('searchbytype/', views.vehicle_type_search),
    path('searchbycolor/', views.vehicle_color_search)
]