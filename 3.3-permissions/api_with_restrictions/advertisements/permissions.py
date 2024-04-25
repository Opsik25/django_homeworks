from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator or request.user.is_staff


class IsDraftRetrieve(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.status != 'DRAFT':
            return True
        return request.user == obj.creator or request.user.is_staff
