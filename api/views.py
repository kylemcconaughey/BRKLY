from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from users.models import User

from .models import Conversation, Dog, Meetup, Message, Reaction, Comment, Post
from .serializers import (
    ConversationSerializer,
    DogSerializer,
    MeetupSerializer,
    MessageSerializer,
    ReactionSerializer,
    UserSerializer,
    CommentSerializer,
    PostSerializer,
    EmbeddedUserSerializer,
)


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.owner


class PostMaker(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.user


class DogViewSet(ModelViewSet):
    serializer_class = DogSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]
    parser_classes = [JSONParser, FileUploadParser]

    def get_queryset(self):
        return Dog.objects.all().select_related("owner").order_by("-created_at")

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(owner=self.request.user)
        raise PermissionDenied()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()

    def retrieve(self, request, pk):
        user = User.objects.filter(pk=pk).prefetch_related(
            "dogs",
            "conversations",
            "admin_conversations",
            "messages_sent",
            "meetups",
            "meetups_admin",
        )
        serializer = UserSerializer(user, context={"request": request})
        return Response(serializer.data)


class ConversationViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Conversation.objects.all()
            .prefetch_related("members", "messages")
            .select_related("admin")
        )


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Message.objects.all()
            .select_related("sender", "conversation")
            .prefetch_related("reactions", "read_by")
        )


class MeetupViewSet(ModelViewSet):
    serializer_class = MeetupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Meetup.objects.all().select_related("admin").prefetch_related("attending")
        )


class ReactionViewSet(ModelViewSet):
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reaction.objects.all().select_related("user")


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return (
            Comment.objects.all()
            .select_related("user", "post")
            .prefetch_related("liked_by")
        )

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def like(self, request, pk):
        comment = self.get_object()
        comment.liked_by.add(self.request.user)
        comment.save()
        return Response(status=201)


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthenticated,
        PostMaker,
    ]
    parser_classes = [JSONParser, FileUploadParser]

    def retrieve(self, request, pk):
        post = (
            Post.objects.filter(pk=pk)
            .select_related("user", "dog")
            .prefetch_related(
                "liked_by", "comments", "comments__user", "comments__liked_by"
            )
        ).first()
        serializer = PostSerializer(post, context={"request": request})
        return Response(serializer.data)

    @action(detail=False)
    def mine(self, request):
        posts = (
            Post.objects.filter(user=self.request.user)
            .select_related("user", "dog")
            .prefetch_related(
                "liked_by", "comments", "comments__user", "comments__liked_by"
            )
            .order_by("-posted_at")
        )
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=False)
    def all(self, request):
        posts = (
            Post.objects.all()
            .select_related("user", "dog")
            .prefetch_related(
                "liked_by", "comments", "comments__user", "comments__liked_by"
            )
            .order_by("-posted_at")
        )
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def image(self, request, pk, format=None):
        if "file" not in request.data:
            raise ParseError("Empty content")

        file = request.data["file"]
        post = self.get_object()

        post.image.save(file.name, file, save=True)
        return Response(status=201)

    @action(detail=True, methods=["POST"])
    def delete_image(self, request, pk, format=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        post.image.delete(save=True)
        return Response(status=204)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def like(self, request, pk):
        post = self.get_object()
        post.liked_by.add(self.request.user)
        post.save()
        return Response(status=201)

    def get_parser_classes(self):
        print(self.action)
        if self.action == "image":
            return [FileUploadParser]

        return [JSONParser]

    def get_queryset(self):
        return (
            Post.objects.all()
            .select_related("user", "dog")
            .prefetch_related("liked_by", "comments", "comments__user")
            .order_by("-posted_at")
        )

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(user=self.request.user)
        raise PermissionDenied()