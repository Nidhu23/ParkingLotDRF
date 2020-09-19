from django.shortcuts import render
from .serializers import RegisterSerializer
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework import request
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.decorators import api_view
from ParkingLot import settings
from . import redis_setup
import jwt
import datetime
import redis
from django.contrib.auth import login, logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
class Register(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = RegisterSerializer

    def post(self, request):
        return self.create(request)


class Login(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ), )
    def post(self, request):
        try:
            redis_instance = redis_setup.get_redis_instance()
            username = request.data.get('username')
            password = request.data.get('password')
            if (username is None) or (password is None):
                return Response("username and password required")
            user = User.objects.get(username=username)
            if (user is None):
                return Response("username required")
            if not user.check_password(password):
                return Response("wrong password entered")
            access_token_payload = {
                'username':
                user.username,
                'exp':
                datetime.datetime.utcnow() +
                datetime.timedelta(days=0, minutes=15)
            }
            access_token = jwt.encode(access_token_payload,
                                      settings.SECRET_KEY)
            redis_instance.set(username, access_token)
            return Response("LOGIN SUCCESSFULL",
                            headers={'token': access_token},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response("user not registered,please register")
