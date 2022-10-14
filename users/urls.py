from django.urls import path

from users.views import UserView

urlpatterns = [
    path("users/register/", UserView.as_view())
]