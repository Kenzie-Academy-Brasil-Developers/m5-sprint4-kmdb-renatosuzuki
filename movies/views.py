from django.shortcuts import render
from rest_framework.views import APIView, Response, Request, status
from .permissions import IsGetOrSuperUser
from rest_framework.authentication import TokenAuthentication
from movies.models import Movie
from movies.serializers import MovieSerializer
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

class MovieView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsGetOrSuperUser]


    def get (self, request: Request) -> Response:
        movies = Movie.objects.all()

        if not movies:
            return Response({"details": "Not found"}, status.HTTP_404_NOT_FOUND)

        result_page = self.paginate_queryset(movies, request, view=self)

        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


    def post (self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsGetOrSuperUser]


    def get (self, request: Request, movie_id) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie)

        return Response(serializer.data, status.HTTP_200_OK)

    
    def delete (self, request: Request, movie_id) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


    def patch(self, request: Request, movie_id) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie, request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except KeyError as error:
            return Response(*error.args)

        return Response(serializer.data, status.HTTP_200_OK)