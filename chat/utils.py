from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections

from channels.auth import AuthMiddlewareStack
from accounts.models import User
from django.conf import settings

from channels.db import database_sync_to_async

import firebase_admin
from firebase_admin import auth


@database_sync_to_async
def get_user(headers):
    try:
        firebase_token = headers.get(b"authorization").decode().split()[1]
        decoded_token = auth.verify_id_token(firebase_token)
        user_uid = decoded_token.get("uid")
        user = User.objects.get(firebase_uid=user_uid)
        return user
    except User.DoesNotExist:
        return AnonymousUser()
    except auth.ExpiredIdTokenError:
        return AnonymousUser()
    except auth.InvalidIdTokenError:
        return AnonymousUser()


class FirebaseTokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()
        self.scope = dict(scope)
        headers = dict(self.scope["headers"])
        if b"authorization" in headers:
            scope["user"] = await get_user(headers)

        return await self.inner(scope, receive, send)


FirebaseTokenAuthMiddlewareStack = lambda inner: FirebaseTokenAuthMiddleware(
    AuthMiddlewareStack(inner)
)
