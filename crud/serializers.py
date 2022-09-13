from rest_framework import serializers
from .models import User ,Token ,Employee


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'firstname', 'lastname', 'email')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('id', 'username', 'password', 'token')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'firstname', 'lastname', 'email')