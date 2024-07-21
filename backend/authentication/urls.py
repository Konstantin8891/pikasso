from authentication.views import CustomTokenObtainPairView, LogoutView, RegisterUser
from django.urls import path

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterUser.as_view(), name="register_user"),
]
