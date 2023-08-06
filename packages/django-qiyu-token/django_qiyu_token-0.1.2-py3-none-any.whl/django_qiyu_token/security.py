from typing import Optional

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from ninja.security import HttpBearer

from .models import BearerTokenModel

__all__ = ["BearerTokenAuth"]


class BearerTokenAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[User]:
        try:
            m = BearerTokenModel.check_token(token)
            return m.user
        except ObjectDoesNotExist:
            return None
