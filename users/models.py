from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    first_name = models.CharField(null=True, blank=True, max_length=63)

    last_name = models.CharField(null=True, blank=True, max_length=63)

    num_pets = models.IntegerField(null=True, blank=True, default=0)

    street_address = models.CharField(null=True, blank=True, max_length=255)

    city = models.CharField(null=True, blank=True, max_length=63)

    state = models.CharField(null=True, blank=True, max_length=63)

    created_at = models.DateTimeField(auto_now_add=True)

    phone_num = models.IntegerField(null=True, blank=True)

    birthdate = models.DateField(null=True, blank=True)
    # should have a minimum age/maximum date such that min. age = 18

    profile_picture = models.ImageField(upload_to="post_images/", null=True, blank=True)
    # needs media routes set up

    # username? email?