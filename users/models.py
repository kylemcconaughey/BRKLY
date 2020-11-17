from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    first_name = models.CharField(null=True, blank=True, max_length=63)

    last_name = models.CharField(null=True, blank=True, max_length=63)
    last_name_is_public = models.BooleanField(null=False, blank=False, default=False)

    num_pets = models.IntegerField(null=True, blank=True, default=0)

    street_address = models.CharField(null=True, blank=True, max_length=255)
    address_is_public = models.BooleanField(null=False, blank=False, default=False)

    city = models.CharField(null=True, blank=True, max_length=63)

    state = models.CharField(null=True, blank=True, max_length=63)

    created_at = models.DateTimeField(auto_now_add=True)

    phone_num = models.CharField(null=True, blank=True, max_lenth=12)
    phone_is_public = models.BooleanField(null=False, blank=False, default=False)

    birthdate = models.DateField(null=True, blank=True)
    birthdate_is_public = models.BooleanField(null=False, blank=False, default=False)
    # should have a minimum age/maximum date such that min. age = 18

    picture = models.ImageField(upload_to="post_images/", null=True, blank=True)
    # needs media routes set up

    followers = models.ManyToManyField(
        "self", related_name="following", symmetrical=False, blank=True
    )

    friends = models.ManyToManyField(
        "self", related_name="friends", symmetrical=True, blank=True
    )