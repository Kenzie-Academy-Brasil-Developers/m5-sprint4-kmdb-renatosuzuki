from rest_framework.views import APIView, Response, Request, status
from .serializers import LoginSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class UserView(APIView):
    def post(self, request: Request) -> Response:
        user_serializer = UserSerializer(data=request.data)

        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status.HTTP_400_BAD_REQUEST)

        user_serializer.save()

        return Response(user_serializer.data, status.HTTP_201_CREATED)

    
class LoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"token": token.key}, status.HTTP_200_OK)

        else:
            return Response({"detail": "invalid username or password"}, status.HTTP_400_BAD_REQUEST)