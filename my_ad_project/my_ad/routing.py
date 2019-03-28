from django.urls import include, path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from ads.token_auth import TokenAuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from ads.consumers import MessageAddConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        TokenAuthMiddlewareStack(
            URLRouter(
                [
                    path('ads/<slug:ad_slug>', MessageAddConsumer),
                ]
            )
        )
    )
})
