from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import api.routing
from .monkeyware import QueryAuthMiddleware

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": QueryAuthMiddleware(URLRouter(api.routing.websocket_urlpatterns)),
    }
)
