from rest_framework import serializers
from users.models import User
from .models import Review


class CriticInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]


class ReviewSerializer(serializers.ModelSerializer):
    critic_user = CriticInfoSerializer(read_only=True)


    class Meta:
        model = Review
        fields = ["id", "stars", "review", "spoilers", "recomendation", "movie_id", "critic_user"]