from django.core.exceptions import PermissionDenied
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from users.models import User
from .models import (
    Comment,
    Conversation,
    DiscussionBoard,
    Dog,
    Meetup,
    Message,
    Post,
    Reaction,
    Request,
    Note,
)
from maps.models import Location
from .serializers import (
    CommentSerializer,
    ConversationSerializer,
    DiscussionBoardSerializer,
    DiscussionBoardPFSerializer,
    DogSerializer,
    MeetupSerializer,
    MessageSerializer,
    PostSerializer,
    PostPFSerializer,
    ReactionSerializer,
    UserSerializer,
    RequestSerializer,
    LocationSerializer,
    UserSearchSerializer,
    NoteSerializer,
)

"""
GET /users/search/?q=<search_term>      searches for 'search_term' across username, first_name, last_name, and the names of people's dogs
(but still returns the person, not the dog)
"""


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


class IsSelf(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, usr):
        if request.method in SAFE_METHODS:
            return True

        return request.user == usr


class DogViewSet(ModelViewSet):
    serializer_class = DogSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]
    parser_classes = [JSONParser, FileUploadParser]

    def get_queryset(self):
        return Dog.objects.all().select_related("owner").order_by("-created_at")

    def retrieve(self, request, pk):
        dog = (
            (
                Dog.objects.filter(pk=pk)
                .select_related("owner")
                .prefetch_related("posts")
            )
            .annotate(num_posts=Count("posts", distinct=True))
            .first()
        )
        serializer = DogSerializer(dog, context={"request": request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(owner=self.request.user)
        raise PermissionDenied()

    @action(detail=False, methods=["GET"])
    def name_search(self, request):
        search_term = request.GET.get("q")
        dogs = Dog.objects.filter(
            Q(name__icontains=search_term)
            | Q(owner__username__icontains=search_term)
            | Q(owner__first_name__icontains=search_term)
        ).annotate(num_posts=Count("posts", distinct=True))
        serializer = DogSerializer(dogs, context={"request": request}, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def tag_search(self, request):
        search_term = request.GET.get("q")
        dogs = Dog.objects.filter(
            Q(breed__icontains=search_term)
            | Q(size__icontains=search_term)
            | Q(energy__icontains=search_term)
            | Q(temper__icontains=search_term)
            | Q(group_size__icontains=search_term)
            | Q(vaccinated__icontains=search_term)
            | Q(kid_friendly__icontains=search_term)
        ).annotate(num_posts=Count("posts", distinct=True))
        serializer = DogSerializer(dogs, context={"request": request}, many=True)
        return Response(serializer.data)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelf]

    def get_queryset(self):
        return (
            User.objects.all()
            .prefetch_related(
                "dogs",
                "followers",
                "conversations",
                "meetups",
                "adminconversations",
                "meetupsadmin",
                "friends",
                "requests_sent",
                "requests_received",
            )
            .annotate(
                num_followers=Count("followers", distinct=True),
                num_conversations=Count("conversations", distinct=True),
                num_friends=Count("friends", distinct=True),
                friend_requests=Count(
                    "requests_received",
                    filter=Q(requests_received__accepted=False),
                    distinct=True,
                ),
                unread_messages=(
                    Count(
                        "conversations__messages",
                        distinct=True,
                    )
                )
                - (Count("messages_read", distinct=True)),
            )
        )

    @action(detail=False, methods=["GET"])
    def search(self, request):
        search_term = request.GET.get("q")
        users = User.objects.filter(
            Q(username__icontains=search_term)
            | Q(first_name__icontains=search_term)
            | Q(last_name__icontains=search_term)
            | Q(dogs__name__icontains=search_term)
        ).distinct("id")
        serializer = UserSearchSerializer(
            users, context={"request": request}, many=True
        )
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def follow(self, request, pk):
        person = User.objects.get(pk=pk)
        person.followers.add(self.request.user)
        serializer = UserSerializer(person, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def unfollow(self, request, pk):
        person = User.objects.get(pk=pk)
        person.followers.remove(self.request.user)
        person.save()
        return Response(status=204)

    @action(detail=True, methods=["POST"])
    def request(self, request, pk):
        proposer = self.request.user
        receiver = User.objects.get(pk=pk)
        Request.objects.create(proposing=proposer, receiving=receiver, accepted=False)
        return Response(status=200)

    @action(detail=True, methods=["POST"])
    def unfriend(self, request, pk):
        them = User.objects.filter(pk=pk)
        friend_request = Request.objects.get(
            (Q(proposing=self.request.user) & Q(receiving=them))
            | (Q(proposing=them) & Q(receiving=self.request.user))
        )
        self.request.user.friends.remove(them)
        friend_request.delete()
        return Response(status=204)

    def retrieve(self, request, pk):
        user = (
            User.objects.filter(pk=pk)
            .prefetch_related(
                "dogs",
                "conversations",
                "meetups",
                "adminconversations",
                "meetupsadmin",
                "posts",
                "comments",
                "followers",
                "friends",
                "requests_sent",
                "requests_received",
            )
            .annotate(
                num_followers=Count("followers", distinct=True),
                num_conversations=Count("conversations", distinct=True),
                num_friends=Count("friends", distinct=True),
                friend_requests=Count(
                    "requests_received",
                    filter=Q(requests_received__accepted=False),
                    distinct=True,
                ),
                unread_messages=(
                    Count(
                        "conversations__messages",
                        distinct=True,
                    )
                )
                - (Count("messages_read", distinct=True)),
            )
            .first()
        )
        serializer = UserSerializer(user, context={"request": request})
        return Response(serializer.data)


class ConversationViewSet(ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Conversation.objects.all()
            .prefetch_related("members", "messages")
            .select_related("admin")
            .annotate(
                num_messages=Count("messages", distinct=True),
                unread=(
                    Count(
                        "messages",
                        distinct=True,
                    )
                )
                - (
                    Count(
                        "messages",
                        filter=Q(messages__read_by=self.request.user),
                        distinct=True,
                    )
                ),
            )
        )

    def retrieve(self, request, pk):
        convo = (
            Conversation.objects.filter(pk=pk)
            .select_related("admin")
            .prefetch_related("members", "messages")
            .annotate(
                num_messages=Count("messages", distinct=True),
                unread=(
                    Count(
                        "messages",
                        distinct=True,
                    )
                )
                - (
                    Count(
                        "messages",
                        filter=Q(messages__read_by=self.request.user),
                        distinct=True,
                    )
                ),
            )
        ).first()
        serializer = ConversationSerializer(convo, context={"request": request})
        return Response(serializer.data)


class RequestViewSet(ModelViewSet):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Request.objects.all().select_related("proposing", "receiving")

    @action(detail=True, methods=["POST"])
    def accept(self, request, pk):
        friend_request = self.get_object()
        if self.request.user == friend_request.receiving:
            self.request.user.friends.add(friend_request.proposing)
            friend_request.accepted = True
            friend_request.save()
            return Response(201)
        raise PermissionDenied()

    @action(detail=True, methods=["POST"])
    def deny(self, request, pk):
        friend_request = self.get_object()
        if self.request.user == friend_request.receiving:
            friend_request.delete()
            return Response(204)
        raise PermissionDenied()


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Message.objects.all()
            .select_related("sender", "conversation")
            .prefetch_related("reactions", "read_by")
        )

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()
        serializer.save(sender=self.request.user, read_by=self.request.user)

    @action(detail=True, methods=["POST"])
    def read(self, request, pk):
        message = Message.objects.filter(pk=pk).first()
        message.read_by.add(self.request.user)
        message.save()
        return Response(201)


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

    @action(detail=True, methods=["POST"])
    def like(self, request, pk):
        comment = self.get_object()
        if self.request.user not in comment.liked_by.all():
            comment.liked_by.add(self.request.user)
            comment.save()
            return Response(status=201)
        comment.liked_by.remove(self.requst.user)
        comment.save()
        return Response(status=204)


class PostViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostPFSerializer
        return PostSerializer

    permission_classes = [
        IsAuthenticated,
    ]
    parser_classes = [JSONParser, FileUploadParser]

    @action(detail=True, methods=["POST"])
    def react(self, request, pk):
        reaction_emoji = request.GET.get("r")
        # POST /posts/<int:pk>/react/?r=🤣
        post = Post.objects.filter(pk=pk).first()
        reaction = Reaction.objects.create(
            reaction=reaction_emoji, user=self.request.user
        )
        post.reactions.add(reaction)
        post.save()
        return Response(201)

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
            Post.objects.filter(
                Q(user__friends=self.request.user)
                | Q(user__followers=self.request.user)
                | Q(user=self.request.user)
            )
            .select_related("user", "dog")
            .prefetch_related(
                "liked_by", "comments", "comments__user", "comments__liked_by"
            )
            .order_by("-posted_at")
        ).distinct("posted_at")
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

    @action(detail=True, methods=["POST"])
    def like(self, request, pk):
        post = self.get_object()
        if self.request.user not in post.liked_by.all():
            post.liked_by.add(self.request.user)
            post.save()
            return Response(status=201)
        post.liked_by.remove(self.request.user)
        post.save()
        return Response(status=204)

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


class DiscussionBoardViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return DiscussionBoardPFSerializer
        return DiscussionBoardSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(user=self.request.user)
        raise PermissionDenied()

    def get_queryset(self):
        return (
            DiscussionBoard.objects.all()
            .order_by("-posted_at")
            .select_related("user")
            .prefetch_related(
                "upvotes", "downvotes", "notes", "notes__upvotes", "notes__downvotes"
            )
        ).annotate(
            num_upvotes=Count("upvotes", distinct=True),
            num_downvotes=Count("downvotes", distinct=True),
            total_votes=(
                (Count("upvotes", distinct=True)) - (Count("downvotes", distinct=True))
            ),
            num_notes=Count("notes", distinct=True),
            num_note_upvotes=Count("notes__upvotes", distinct=True),
        )

    def retrieve(self, request, pk):
        board = (
            DiscussionBoard.objects.filter(pk=pk)
            .select_related("user")
            .prefetch_related(
                "upvotes",
                "downvotes",
                "notes",
                "notes__upvotes",
                "notes__downvotes",
            )
            .annotate(
                num_upvotes=Count("upvotes", distinct=True),
                num_downvotes=Count("downvotes", distinct=True),
                total_votes=(
                    (Count("upvotes", distinct=True))
                    - (Count("downvotes", distinct=True))
                ),
                num_notes=Count("notes", distinct=True),
                num_note_upvotes=Count("notes__upvotes", distinct=True),
            )
            .first()
        )
        serializer = DiscussionBoardSerializer(board, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def upvote(self, request, pk):
        board = DiscussionBoard.objects.filter(pk=pk).first()
        if self.request.user not in board.upvotes.all():
            board.upvotes.add(self.request.user)
            board.save()
            return Response(status=201)
        board.upvotes.remove(self.request.user)
        board.save()
        return Response(status=204)

    @action(detail=True, methods=["POST"])
    def downvote(self, request, pk):
        board = DiscussionBoard.objects.filter(pk=pk).first()
        if self.request.user not in board.downvotes.all():
            board.downvotes.add(self.request.user)
            board.save()
            return Response(status=201)
        board.downvotes.remove(self.request.user)
        board.save()
        return Response(status=204)


class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Location.objects.all().order_by("-created_at")


class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, PostMaker]

    def get_queryset(self):
        return Note.objects.all().order_by("-posted_at")

    @action(detail=True, methods=["POST"])
    def upvote(self, request, pk):
        note = Note.objects.filter(pk=pk).first()
        if self.request.user not in note.upvotes.all():
            note.upvotes.add(self.request.user)
            note.num_upvotes += 1
            note.save()
            return Response(status=201)
        note.upvotes.remove(self.request.user)
        note.num_upvotes -= 1
        note.save()
        return Response(status=204)

    @action(detail=True, methods=["POST"])
    def downvote(self, request, pk):
        note = Note.objects.filter(pk=pk).first()
        if self.request.user not in note.downvotes.all():
            note.downvotes.add(self.request.user)
            note.num_downvotes += 1
            note.save()
            return Response(status=201)
        note.downvotes.remove(self.request.user)
        note.num_downvotes -= 1
        note.save()
        return Response(status=204)