from typing import Any

from django.http import HttpRequest
from ninja_extra import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, controller: "APIController"):
        return True

    def has_object_permission(
        self, request: HttpRequest, controller: "APIController", obj: Any
    ):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if obj.fc_id != request.user.id:
                return False
            return True
