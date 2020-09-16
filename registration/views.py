from django.shortcuts import render
from .serializers import RegisterSerializer
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework import request
from rest_framework.response import Response
from .models import User
from ParkingLot import settings
import jwt
from django.contrib.auth import login, logout


# Create your views here.
class Register(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = RegisterSerializer

    def post(self, request):
        return self.create(request)


class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if (username is None) or (password is None):
            return Response("username and password required")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response("user not registered,please register")
        if (user is None):
            return Response("username required")
        if not user.check_password(password):
            return Response("wrong password entered")
        access_token_payload = {
            'username': user.username,
            'password': user.password
        }

        access_token = jwt.encode(access_token_payload, settings.SECRET_KEY)
        login(request, user)
        data = {"user": user.username, "token": access_token}
        return Response(data)