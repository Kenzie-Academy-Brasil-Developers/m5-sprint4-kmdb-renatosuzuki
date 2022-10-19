from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, Request, status
from rest_framework.authentication import TokenAuthentication
from .models import Review
from movies.models import Movie
from .serializers import ReviewSerializer
from .permissions import AdminOrCriticPermission, AdminOrOwnCriticPermission
from rest_framework.pagination import PageNumberPagination


class ReviewView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminOrCriticPermission]


    def post(self, request: Request, movie_id) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        check_review = Review.objects.filter(movie_id=movie.id, critic_user=request.user).exists()

        

        if check_review:
            return Response({"detail": "Review already exists."}, status.HTTP_403_FORBIDDEN)

        serializer = ReviewSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(movie=movie, critic_user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)


    def get(self, request: Request, movie_id) -> Response:
        reviews = Review.objects.filter(movie_id=movie_id)

        if not reviews:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

        result_page = self.paginate_queryset(reviews, request, view=self)

        serializer = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)
        

class ReviewDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminOrOwnCriticPermission]


    def get(self, request: Request, movie_id, review_id) -> Response:
        review = get_object_or_404(Review, movie_id=movie_id, id=review_id)

        serializer = ReviewSerializer(review)

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request: Request, movie_id, review_id) -> Response:
        review = get_object_or_404(Review, movie_id=movie_id, id=review_id)

        self.check_object_permissions(request, review.critic_user)

        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)