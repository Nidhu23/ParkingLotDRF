import json
from .models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.


"""class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
            "username": "name1",
            "email": "nid@gmail.com",
            "password": "passworddemo",
            "role": "driver"
        }
        response = self.client.post("/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)"""
