from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from chat.utils import TokenAuthMiddlewareStack

# Define the Django Channels application routing.
application = ProtocolTypeRouter(
    {
        # Specifies that for WebSocket protocol, the following settings should be used.
        "websocket": TokenAuthMiddlewareStack(
            # URLRouter directs incoming WebSocket connections based on their URL pattern.
            URLRouter(chat.routing.websocket_urlpatterns)
            # TokenAuthMiddlewareStack is a custom middleware for handling Token Authentication
            # in WebSocket connections.
        ),
    }
)
