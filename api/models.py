from django.db import models
from users.models import User

# Create your models here.


class Dog(models.Model):

    owner = models.ForeignKey(to="User", on_delete=models.CASCADE, related_name="dogs")
    name = models.CharField(null=False, blank=False)
    breed = models.CharField(null=False, blank=False)
    picture = models.ImageField(upload_to="post_images/", null=True, blank=True)
    age = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class SizeChoices(models.TextChoices):
        SML = "S", ("SMALL")
        MED = "M", ("MEDIUM")
        LRG = "L", ("LARGE")

    size = models.CharField(
        max_length=3, choices=SizeChoices.choices, default=SizeChoices.MED
    )

    class EnergyChoices(models.TextChoices):
        HI = "HI", ("High Energy")
        MD = "MD", ("Medium Energy")
        LO = "LO", ("Low Energy")

    energy = models.CharField(
        max_length=2, choices=EnergyChoices.choices, default=EnergyChoices.MD
    )

    class TemperChoices(models.TextChoices):
        AGR = "AGR", ("Aggressive")
        NML = "NML", ("Normal")
        CHL = "CHL", ("Relaxed")

    temper = models.CharField(
        max_length=3, choices=TemperChoices.choices, default=TemperChoices.NML
    )

    class GroupChoices(models.TextChoices):
        ONE = "ONE", ("ONE ON ONE")
        BIG = "BIG", ("GOOD IN LARGE GROUPS")
        SML = "SML", ("GOOD IN SMALL GROUPS")
        ANY = "ANY", ("GOOD IN ANY SETTING")

    group_size = models.CharField(
        max_length=3, choices=GroupChoices.choices, default=GroupChoices.ONE
    )

    class VaccineChoices(models.TextChoices):
        VAC = "YES", ("VACCINATED")
        NOT = "NOT", ("I AM TERRIBLE DOG OWNER")

    vaccinated = models.CharField(
        max_length=3, choices=VaccineChoices.choices, default=VaccineChoices.VAC
    )

    class ChildrenChoices(models.TextChoices):
        Y = "Y", ("GOOD WITH CHILDREN")
        N = "N", ("NOT GOOD WITH CHILDREN")

    kid_friendly = models.CharField(
        max_length=1, choices=ChildrenChoices.choices, default=ChildrenChoices.Y
    )


class Conversation(models.Model):
    members = models.ManyToManyField(to="User", related_name="conversations")

    created_at = models.DateTimeField(auto_now_add=True)

    convo_name = models.CharField(null=False, blank=False, default="New Conversation")

    admin = models.ForeignKey(
        to="User", on_delete=models.PROTECT, related_name="admin_conversations"
    )

    def preview(self):
        pass


class Reaction(models.Model):
    class ReactionChoices(models.TextChoices):
        LIKE = "LI", ("Like")
        LOVE = "LO", ("Love")
        LAUGH = "LA", ("Laugh")
        ANGRY = "AN", ("Angry")

    reaction = models.CharField(
        max_length=2, choices=ReactionChoices.choices, default=ReactionChoices.LIKE
    )


class Message(models.Model):
    sender = models.ForeignKey(
        to="User", on_delete=models.CASCADE, related_name="messages_sent"
    )

    conversation = models.ForeignKey(
        to="Conversation", on_delete=models.CASCADE, related_name="messages"
    )

    time_sent = models.DateTimeField(auto_now_add=True)

    body = models.TextField(null=True, blank=True)

    reactions = models.ManyToManyField(to="Reaction", related_name="message")

    image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    # needs media routes set up

    read_by = models.ManyToManyField(to="User", related_name="messages_read")


class Meetup(models.Model):
    admin = models.ForeignKey(
        to="User", on_delete=models.CASCADE, related_name="meetups_admin"
    )

    # invited = models.ManyToManyField(to="User", related_name="meetup_invites")

    attending = models.ManyToManyField(to="User", related_name="meetups")

    start_time = models.DateTimeField(null=False, blank=False)

    end_time = models.DateTimeField(null=True, blank=True)

    location = models.CharField(null=False, blank=False)
    # needs auto-fill options pulled from geo-API

    # recurring = models.whoTheHellKnows
