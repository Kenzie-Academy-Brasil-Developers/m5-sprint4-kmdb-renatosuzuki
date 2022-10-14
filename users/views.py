from rest_framework.views import APIView, Response, Request, status
from .models import User
from .serializers import UserSerializer


class UserView(APIView):
    def post(self, request: Request) -> Response:
        user_serializer = UserSerializer(data=request.data)

        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status.HTTP_400_BAD_REQUEST)

        user_serializer.save()

        return Response(user_serializer.data, status.HTTP_201_CREATED)