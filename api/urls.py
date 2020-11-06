from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from . import views as api_views

api_router = routers.DefaultRouter()

api_router.register("dogs", api_views.DogViewSet, basename="dog")
api_router.register("users", api_views.UserViewSet, basename="user")
api_router.register(
    "conversations", api_views.ConversationViewSet, basename="conversation"
)
api_router.register("messages", api_views.MessageViewSet, basename="message")
api_router.register("meetups", api_views.MeetupViewSet, basename="meetup")

urlpatterns = [
    path("", include(api_router.urls)),
]