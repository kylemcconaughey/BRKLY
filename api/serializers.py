from rest_framework import serializers
from users.models import User
from .models import Dog, Message, Conversation, Reaction, Meetup


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


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = [
            "members",
            "created_at",
            "convo_name",
            "admin",
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    dogs = serializers.HyperlinkedRelatedField(
        many=True, view_name="dog-detail", read_only=True
    )
    conversations = serializers.HyperlinkedRelatedField(
        many=True, view_name="conversation-detail", read_only=True
    )
    admin_conversations = serializers.HyperlinkedRelatedField(
        many=True, view_name="admin_conversation-detail", read_only=True
    )
    meetups = serializers.HyperlinkedRelatedField(
        many=True, view_name="meetup-detail", read_only=True
    )
    meetups_admin = serializers.HyperlinkedRelatedField(
        many=True, view_name="meetup_admin-detail", read_only=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "num_pets",
            "street_address",
            "city",
            "state",
            "created_at",
            "phone_num",
            "birthdate",
            "profile_picture",
            "pets",
            "conversations",
            "admin_conversations",
            "meetups",
            "meetups_admin",
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