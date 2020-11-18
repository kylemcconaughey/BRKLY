from rest_framework import serializers
from users.models import User
from .models import (
    DiscussionBoard,
    Dog,
    Message,
    Conversation,
    Reaction,
    Meetup,
    Post,
    Comment,
    Request,
    Note,
)
from maps.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "name",
            "url",
            "description",
            "coordinates",
            "location_type",
        ]


class EmbeddedLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["name", "url", "coordinates"]


class EmbeddedUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["username", "url", "id"]


class DogSerializer(serializers.ModelSerializer):
    owner = EmbeddedUserSerializer()
    num_posts = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dog
        fields = [
            "name",
            "url",
            "owner",
            "breed",
            "picture",
            "age",
            "created_at",
            "size",
            "energy",
            "temper",
            "group_size",
            "vaccinated",
            "kid_friendly",
            "num_posts",
        ]


class EmbeddedDogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = ["name", "url", "picture"]


class EmbeddedMessageSerializer(serializers.ModelSerializer):
    sender = EmbeddedUserSerializer()
    reactions = serializers.StringRelatedField(many=True, read_only=True)
    read_by = serializers.SlugRelatedField(
        slug_field="username", read_only=True, many=True
    )

    class Meta:
        model = Message
        fields = [
            "url",
            "sender",
            "time_sent",
            "body",
            "reactions",
            "image",
            "read_by",
        ]


class ConversationSerializer(serializers.ModelSerializer):
    messages = EmbeddedMessageSerializer(many=True)
    members = EmbeddedUserSerializer(many=True)
    admin = EmbeddedUserSerializer()
    num_messages = serializers.IntegerField(read_only=True)
    unread = serializers.IntegerField(read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "convo_name",
            "url",
            "id",
            "members",
            "messages",
            "created_at",
            "admin",
            "num_messages",
            "unread",
        ]


class EmbeddedConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = [
            "url",
            "id",
            "convo_name",
            "created_at",
        ]


class EmbeddedMeetupSerializer(serializers.ModelSerializer):
    location = EmbeddedLocationSerializer()

    class Meta:
        model = Meetup
        fields = [
            "url",
            "start_time",
            "end_time",
            "location",
        ]


class RequestSerializer(serializers.ModelSerializer):
    proposing = EmbeddedUserSerializer()
    receiving = EmbeddedUserSerializer()

    class Meta:
        model = Request
        fields = [
            "url",
            "id",
            "proposing",
            "receiving",
            "accepted",
        ]


class EmbeddedRequestSerializer(serializers.ModelSerializer):
    proposing = serializers.SlugRelatedField(slug_field="username", read_only=True)
    receiving = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Request
        fields = [
            "url",
            "proposing",
            "receiving",
            "accepted",
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    dogs = EmbeddedDogSerializer(many=True)
    conversations = EmbeddedConversationSerializer(many=True)
    adminconversations = EmbeddedConversationSerializer(many=True)
    meetups = EmbeddedMeetupSerializer(many=True)
    meetupsadmin = EmbeddedMeetupSerializer(many=True)
    followers = EmbeddedUserSerializer(many=True)
    friends = EmbeddedUserSerializer(many=True)
    requests_sent = EmbeddedRequestSerializer(many=True)
    requests_received = EmbeddedRequestSerializer(many=True)
    num_followers = serializers.IntegerField()
    num_conversations = serializers.IntegerField()
    num_friends = serializers.IntegerField()
    unread_messages = serializers.IntegerField()
    friend_requests = serializers.IntegerField()

    class Meta:
        model = User
        fields = [
            "url",
            "username",
            "first_name",
            "last_name",
            "last_name_is_public",
            "email",
            "num_pets",
            "street_address",
            "address_is_public",
            "city",
            "state",
            "created_at",
            "phone_num",
            "phone_is_public",
            "birthdate",
            "birthdate_is_public",
            "picture",
            "dogs",
            "conversations",
            "adminconversations",
            "meetups",
            "meetupsadmin",
            "followers",
            "friends",
            "requests_received",
            "requests_sent",
            "num_followers",
            "num_conversations",
            "num_friends",
            "unread_messages",
            "friend_requests",
        ]


class ReactionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Reaction
        fields = [
            "reaction",
            "user",
            "url",
        ]


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    sender = EmbeddedUserSerializer()
    reactions = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            "sender",
            "conversation",
            "url",
            "time_sent",
            "body",
            "reactions",
            "image",
            "read_by",
        ]


class MeetupSerializer(serializers.ModelSerializer):
    admin = EmbeddedUserSerializer()
    attending = EmbeddedUserSerializer(many=True)
    location = EmbeddedLocationSerializer()

    class Meta:
        model = Meetup
        fields = [
            "url",
            "admin",
            "attending",
            "start_time",
            "end_time",
            "location",
        ]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = EmbeddedUserSerializer()
    liked_by = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ["user", "post", "body", "id", "url", "posted_at", "liked_by"]


class PostPFSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "body",
            "dog",
            "image",
            "posted_at",
            "font_style",
            "text_align",
            "font_size",
        ]


class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = EmbeddedUserSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    liked_by = serializers.StringRelatedField(many=True, read_only=True)
    reactions = ReactionSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            "url",
            "id",
            "user",
            "dog",
            "body",
            "image",
            "posted_at",
            "font_style",
            "text_align",
            "font_size",
            "liked_by",
            "comments",
            "reactions",
        ]


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            "url",
            "body",
            "board",
            "user",
            "posted_at",
            "upvotes",
            "downvotes",
            "num_upvotes",
            "num_downvotes",
            "total_votes",
        ]


class DiscussionBoardPFSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscussionBoard
        fields = ["title", "body", "posted_at"]


class DiscussionBoardSerializer(serializers.HyperlinkedModelSerializer):
    def get_notes(self, request, instance):
        notes = instance.notes.order_by("board__notes__num_upvotes")
        return NoteSerializer(notes, many=True, context={"request": request}).data

    user = EmbeddedUserSerializer()
    num_upvotes = serializers.IntegerField()
    num_downvotes = serializers.IntegerField()
    total_votes = serializers.IntegerField()
    num_notes = serializers.IntegerField()
    notes = serializers.SerializerMethodField()

    class Meta:
        model = DiscussionBoard
        fields = [
            "url",
            "title",
            "body",
            "user",
            "posted_at",
            "num_upvotes",
            "num_downvotes",
            "total_votes",
            "notes",
            "num_notes",
        ]


class UserSearchSerializer(serializers.ModelSerializer):

    dogs = EmbeddedDogSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "url",
            "id",
            "picture",
            "dogs",
        ]