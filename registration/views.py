from django.shortcuts import render
from .serializers import RegisterSerializer
from rest_framework import generics, mixins


# Create your views here.
class Register(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = RegisterSerializer

    def post(self, request):
        return self.create(request)