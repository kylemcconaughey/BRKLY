from django.db import models
from django.db.models.fields import CharField
from users.models import User

# Create your models here.


class Dog(models.Model):

    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="dogs")
    name = models.CharField(null=False, blank=False, max_length=63)
    breed = models.CharField(null=False, blank=False, max_length=63)
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
    members = models.ManyToManyField(to=User, related_name="conversations")

    created_at = models.DateTimeField(auto_now_add=True)

    convo_name = models.CharField(
        null=False, blank=False, default="New Conversation", max_length=63
    )

    admin = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="adminconversations"
    )

    def preview(self):
        pass


class Reaction(models.Model):

    reaction = models.CharField(blank=True, null=True, max_length=20)

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="reactions", null=True
    )


class Message(models.Model):
    sender = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="messages_sent"
    )

    conversation = models.ForeignKey(
        to="Conversation", on_delete=models.CASCADE, related_name="messages"
    )

    time_sent = models.DateTimeField(auto_now_add=True)

    body = models.TextField(null=True, blank=True)

    reactions = models.ManyToManyField(
        to="Reaction", related_name="message", blank=True
    )

    image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    # needs media routes set up

    read_by = models.ManyToManyField(to=User, related_name="messages_read", blank=True)


class Meetup(models.Model):
    admin = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="meetupsadmin"
    )

    # invited = models.ManyToManyField(to=User, related_name="meetup_invites")

    attending = models.ManyToManyField(to=User, related_name="meetups")

    start_time = models.DateTimeField(null=False, blank=False)

    end_time = models.DateTimeField(null=True, blank=True)

    location = models.CharField(null=False, blank=False, max_length=255)
    # needs auto-fill options pulled from geo-API

    # recurring = models.whoTheHellKnows


class Post(models.Model):
    body = models.CharField(max_length=255, null=False, blank=False)

    dog = models.ForeignKey(to=Dog, on_delete=models.CASCADE, related_name="posts")

    posted_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="posts")

    class FontStyleChoices(models.TextChoices):
        NORMAL = "N", ("Normal")
        ITALICS = "I", ("Italics")
        BOLD = "B", ("Bold")
        UNDERLINE = "U", ("Underline")

    font_style = models.CharField(
        max_length=1, choices=FontStyleChoices.choices, default=FontStyleChoices.NORMAL
    )

    class TextAlignChoices(models.TextChoices):
        LEFT = "L", ("Left")
        RIGHT = "R", ("Right")
        CENTER = "C", ("Center")
        JUSTIFIED = (
            "J",
            ("Justified"),
        )

    text_align = models.CharField(
        max_length=1,
        choices=TextAlignChoices.choices,
        default=TextAlignChoices.LEFT,
    )

    class FontSizeChoices(models.IntegerChoices):
        SMALL = (
            "0",
            ("Small"),
        )
        MEDIUM = (
            "1",
            ("Medium"),
        )
        LARGE = (
            "2",
            ("Large"),
        )
        XLARGE = (
            "3",
            ("Xtra Large"),
        )

    font_size = models.IntegerField(
        choices=FontSizeChoices.choices,
        default=FontSizeChoices.MEDIUM,
    )

    image = models.ImageField(upload_to="post_images/", null=True, blank=True)

    liked_by = models.ManyToManyField(to=User, related_name="liked_posts", blank=True)

    reactions = models.ManyToManyField(to="Reaction", related_name="post", blank=True)

    def __str__(self):
        return f"{self.id}"


class Comment(models.Model):
    body = models.CharField(max_length=255, blank=False, null=False)

    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")

    posted_at = models.DateTimeField(auto_now_add=True)

    liked_by = models.ManyToManyField(
        to=User, related_name="liked_comments", blank=True
    )

    def __str__(self):
        return f"{self.body}"


class Request(models.Model):
    proposing = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="requests_sent"
    )

    receiving = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="requests_received"
    )

    accepted = models.BooleanField(blank=False, null=False, default=False)


class DiscussionBoard(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)

    body = models.TextField(blank=False, null=False)

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="discussion_boards"
    )

    posted_at = models.DateTimeField(auto_now_add=True)

    upvotes = models.ManyToManyField(to=User, related_name="upvoted_boards", blank=True)

    downvotes = models.ManyToManyField(
        to=User, related_name="downvoted_boards", blank=True
    )

    def __str__(self):
        return f"{self.title}"
