from django.db import models
from users.models import User
from maps.models import Location
from django_extensions.db.models import TimeStampedModel
import channels
import channels.layers
from django.dispatch import receiver
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from datetime import timedelta


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

    def __str__(self):
        return f"{self.name} | Owner: {self.owner.username}"


class Conversation(models.Model):
    members = models.ManyToManyField(to=User, related_name="conversations", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    convo_name = models.CharField(null=False, blank=False, max_length=63)

    admin = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="adminconversations"
    )

    def preview(self):
        pass

    def __str__(self):
        return f"Convo: {self.convo_name} | Admin: {self.admin.username}"


class Reaction(models.Model):

    reaction = models.CharField(blank=True, null=True, max_length=20)

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="reactions", null=True
    )

    def __str__(self):
        return f"reaction_id: {self.id} | {self.reaction} by {self.user.username}"


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

    read_by = models.ManyToManyField(to=User, related_name="messages_read", blank=True)

    def __str__(self):
        def convoLen():
            if len(self.conversation.convo_name) < 30:
                return self.conversation.convo_name
            return self.conversation.convo_name[:30] + "..."

        if len(self.body) < 30:
            return f"{self.sender.username}: '{self.body}' in '{convoLen()}'"
        return f"{self.sender.username}: '{self.body[:30]}...' in '{convoLen()}'"


class Meetup(models.Model):
    admin = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="meetupsadmin"
    )

    attending = models.ManyToManyField(to=User, related_name="meetups")

    start_time = models.DateTimeField(null=False, blank=False)

    end_time = models.DateTimeField(null=True, blank=True)

    location = models.ForeignKey(
        to=Location,
        on_delete=models.CASCADE,
        related_name="location_meetups",
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            f"Meetup {self.id} | Admin: {self.admin} | Location: {self.location.name}"
        )


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
        def bLen():
            if len(self.body) > 30:
                return f"{self.body[:30]}" + "..."
            return self.body

        return f"By {self.user.username}" + f", about {self.dog.name}" + f": {bLen()}"


class Comment(models.Model):
    body = models.CharField(max_length=255, blank=False, null=False)

    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")

    posted_at = models.DateTimeField(auto_now_add=True)

    liked_by = models.ManyToManyField(
        to=User, related_name="liked_comments", blank=True
    )

    def __str__(self):
        if len(self.body) < 30:
            return f"{self.user.username}: '{self.body}' on Post #{self.post.id}"
        return (
            f"{self.user.username}: '{self.body[:30]}'" + f"... on Post #{self.post.id}"
        )


class Request(models.Model):
    proposing = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="requests_sent"
    )

    receiving = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="requests_received"
    )

    accepted = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return (
            f"{self.proposing}" + " requested to be friends w/ " + f"{self.receiving}"
        )


class DiscussionBoard(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)

    body = models.TextField(blank=False, null=False)

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="discussion_boards"
    )

    posted_at = models.DateTimeField(auto_now_add=True)

    upvotes = models.ManyToManyField(to=User, related_name="upvotes", blank=True)
    downvotes = models.ManyToManyField(to=User, related_name="downvotes", blank=True)

    def __str__(self):
        if len(self.title) < 20:
            return f"{self.title}"
        return f"{self.title[:20]}..."


class Note(models.Model):

    body = models.TextField(null=False, blank=False)

    board = models.ForeignKey(
        to=DiscussionBoard, on_delete=models.CASCADE, related_name="notes"
    )

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="notes")

    posted_at = models.DateTimeField(auto_now_add=True)

    upvotes = models.ManyToManyField(to=User, related_name="note_upvotes", blank=True)
    downvotes = models.ManyToManyField(
        to=User, related_name="note_downvotes", blank=True
    )

    num_upvotes = models.IntegerField(default=0)
    num_downvotes = models.IntegerField(default=0)

    def total_votes(self):
        return self.num_upvotes - self.num_downvotes

    def niceCreated(self):
        nice_created = self.posted_at - timedelta(hours=5)
        return nice_created.strftime("%A at %I:%M %p")

    def __str__(self):
        if len(self.body) < 30:
            return f"{self.user.username}: '{self.body}' on '{self.board}'"
        return f"{self.user.username}: '{self.body[:30]}" + f"...' on '{self.board}'"


class Notification(TimeStampedModel, models.Model):
    sender = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="sent_notifications"
    )
    recipient = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="received_notifications"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    opened = models.BooleanField(null=False, blank=False, default=False)
    trigger = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        def notified():
            if self.trigger == "Message":
                return " messaged "
            elif self.trigger == "Request":
                return " friend requested "
            return " pinged "

        def nice_created():
            when = self.created_at - timedelta(hours=5)
            return when.strftime("%A at %I:%M %p")

        return f"{self.sender.username}{notified()}{self.recipient.username} on {nice_created()} | n_id:{self.id}"


@receiver(post_save, sender=Notification)
def send_new_notification_message(sender, instance, **kwargs):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user-{instance.recipient.pk}",
        {
            "type": "notification.create",
            "sender": instance.sender.username,
            "recipient": instance.recipient.username,
            "trigger": instance.trigger,
        },
    )
