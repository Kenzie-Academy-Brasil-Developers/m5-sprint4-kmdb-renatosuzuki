from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(), message=("email already exists"))])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all(), message=("username already exists"))])
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    birthdate = serializers.DateField()
    bio = serializers.CharField(required=False)
    is_critic = serializers.BooleanField(required=False)
    updated_at = serializers.DateTimeField(read_only=True)


    def create(self, validated_data:dict) -> User:
        user = User.objects.create_user(**validated_data)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)