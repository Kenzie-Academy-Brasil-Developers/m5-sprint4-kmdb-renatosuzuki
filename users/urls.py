from django.urls import path

from users.views import LoginView, UserListAllView, UserListByIdView, UserView

urlpatterns = [
    path("register/", UserView.as_view()),
    path("login/", LoginView.as_view()),
    path("", UserListAllView.as_view()),
    path("<int:user_id>/", UserListByIdView.as_view())
]