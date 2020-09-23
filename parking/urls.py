from django.urls import path
from parking import views

urlpatterns = [
    path('park-unpark/', views.Park.as_view()),
    path('searchbynum/', views.vehicle_num_search),
    path('searchbytype/', views.vehicle_type_search),
    path('searchbycolor/', views.vehicle_color_search)
]
