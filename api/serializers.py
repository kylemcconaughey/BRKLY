from rest_framework import serializers
from users.models import User
from .models import Dog, Message, Conversation, Reaction, Meetup, Post, Comment


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = [
            "owner",
            "name",
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
        ]


class EmbeddedDogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = ["name", "url", "picture"]


class ConversationSerializer(serializers.ModelSerializer):
    messages = serializers.SlugRelatedField(
        slug_field="body", many=True, read_only=True
    )
    members = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "url",
            "id",
            "members",
            "messages",
            "created_at",
            "convo_name",
            "admin",
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
    class Meta:
        model = Meetup
        fields = [
            "url",
            "id",
            "start_time",
            "end_time",
            "location",
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    dogs = EmbeddedDogSerializer(many=True)
    conversations = EmbeddedConversationSerializer(many=True)
    adminconversations = EmbeddedConversationSerializer(many=True)
    meetups = EmbeddedMeetupSerializer(many=True)
    meetupsadmin = EmbeddedMeetupSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "last_name_is_public",
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
            "profile_picture",
            "dogs",
            "conversations",
            "adminconversations",
            "meetups",
            "meetupsadmin",
        ]


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = [
            "reaction",
            "user",
        ]


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    sender_username = serializers.StringRelatedField(read_only=True)
    sender = serializers.HyperlinkedRelatedField(
        view_name="user-detail", read_only=True
    )
    reactions = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            "sender",
            "sender_username",
            "conversation",
            "time_sent",
            "body",
            "reactions",
            "image",
            "read_by",
        ]


class MeetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meetup
        fields = [
            "admin",
            "attending",
            "start_time",
            "end_time",
            "location",
        ]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    liked_by = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ["user", "id", "url", "body", "posted_at", "post", "liked_by"]


class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    liked_by = serializers.StringRelatedField(many=True, read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "user",
            "dog",
            "user_id",
            "body",
            "image",
            "posted_at",
            "id",
            "url",
            "font_style",
            "text_align",
            "font_size",
            "liked_by",
            "comments",
        ]


# For use when displaying sub-lists of users, in which you don't want to see all their information
class EmbeddedUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id", "url"]