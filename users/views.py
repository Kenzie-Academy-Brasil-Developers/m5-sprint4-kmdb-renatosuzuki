from rest_framework.views import APIView, Response, Request, status
from django.shortcuts import get_object_or_404
from users.permissions import AdmPermission, UserPermission
from .serializers import LoginSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from .models import User

class UserView(APIView):
    def post(self, request: Request) -> Response:
        user_serializer = UserSerializer(data=request.data)

        user_serializer.is_valid(raise_exception=True)

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


class UserListAllView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]


    def get(self, request: Request) -> Response:
        users = User.objects.all()

        if not users:
            return Response({"details": "Not found"}, status.HTTP_404_NOT_FOUND)

        users_serializer = UserSerializer(users, many=True)

        return Response(users_serializer.data, status.HTTP_200_OK)


class UserListByIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdmPermission | UserPermission]


    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)


