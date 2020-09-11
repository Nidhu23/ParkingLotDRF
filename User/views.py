from django.shortcuts import render
from rest_framework.views import APIView
from .models import Users
from .serializers import UserSerializer
from django.http import Http404
from rest_framework import request
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class UserList(APIView):
    def get(self, request, format=None):
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)