from django.urls import include, path
from rest_framework import routers

from . import views as api_views

api_router = routers.DefaultRouter()

api_router.register("dogs", api_views.DogViewSet, basename="dog")
api_router.register("users", api_views.UserViewSet, basename="user")

urlpatterns = [
    path("", include(api_router.urls)),
]
