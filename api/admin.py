from django.contrib import admin
from .models import Dog, Conversation, Message, Reaction, Meetup

# Register your models here.

admin.site.register(Dog)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Reaction)
admin.site.register(Meetup)