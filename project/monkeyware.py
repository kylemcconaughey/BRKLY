from users.models import User
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user(user_token):
    try:
        return Token.objects.get(key=user_token).user
    except Token.DoesNotExist:
        return AnonymousUser()


class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user tokens from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            scope["user"] = await get_user(scope["query_string"].decode("utf8"))
        except Exception as exc:
            print(exc)

        return await self.app(scope, receive, send)