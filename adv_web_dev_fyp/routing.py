from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import sns_app.routing

application = ProtocolTypeRouter({
    'websocket' : AuthMiddlewareStack(URLRouter(sns_app.routing.websocket_urlpatterns))
})
