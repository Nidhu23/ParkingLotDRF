from django.shortcuts import render
from .serializers import RegisterSerializer
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework import request
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.decorators import api_view
from parking.services import get_user
from ParkingLot import settings
from . import redis_setup
import jwt
import datetime
import redis
from .redis_setup import get_redis_instance
from .tasks import send_notification
from django.contrib.auth import login, logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import exceptions
''' 
Register API

Parameters:
argument(1):request paramter: having username,role,email,password

Returns:
registers user and returns status code and message
'''


@api_view(['POST'])
def register(request):
    try:
        user_email = request.data['email']
        user_name = request.data['username']
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_notification.delay(user_email, user_name)
            return Response("SUCCESSFULLY REGISTERED",
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except exceptions as exception:
        return Response(exception=True,
                        data={
                            "exception": exception,
                            "status": status.HTTP_400_BAD_REQUEST
                        })


''' 
Login API

Parameters:
argument(1):request paramter: having username,password

Returns:
create access token and returns status code and message
'''


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
            access_token_payload = {'username': 'login' + user.username}
            access_token = jwt.encode(access_token_payload,
                                      settings.SECRET_KEY)
            redis_instance.set('login' + username, access_token)
            return Response("LOGIN SUCCESSFULL",
                            headers={'token': access_token},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response("user not registered,please register")
        except exceptions as exception:
            return Response(data={"exception": exception})
        except Exception:
            return Response("Error")


''' 
Logout function

Parameters:
argument(1):request paramter: token in request header

Returns:
deletes the user from redis 
'''


@api_view(['GET'])
def logout(request):
    try:
        redis_instance = get_redis_instance()
        user = get_user(request.headers.get('token'))
        redis_instance.delete(user)
        return Response("logged out successfully", status=status.HTTP_200_OK)
    except DataError:
        return Response("You are not logged in",
                        status=status.HTTP_404_NOT_FOUND)
