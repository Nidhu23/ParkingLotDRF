from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all())])
    password = serializers.CharField(min_length=8)

    class Meta:
        model = Users
        fields = '__all__'