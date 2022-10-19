from rest_framework import serializers
from .models import Movie
from genres.serializers import GenreSerializer
from genres.models import Genre

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    premiere = serializers.DateField()
    duration = serializers.CharField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()
    genres = GenreSerializer(many=True)


    def create(self, validate_data) -> Movie:
        genres = validate_data.pop("genres")

        movie = Movie.objects.create(**validate_data)

        for genre_new in genres:
            genre, _ = Genre.objects.get_or_create(**genre_new)

            movie.genres.add(genre)

        return movie


    def update(self, instance, validate_data):
        instance.genres.clear()

        for key, value in validate_data.items():
            if key == "genres":
                for genres in value:
                    genre, _ = Genre.objects.get_or_create(**genres)
                    instance.genres.add(genre)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance