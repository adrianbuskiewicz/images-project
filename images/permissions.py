from rest_framework import permissions


class BiggerSizePermission(permissions.BasePermission):
    message = 'Tier does not allow to see bigger size thumbnail.'

    def has_permission(self, request, view):
        return request.user.tier.can_bigger_size


class OriginalImagePermission(permissions.BasePermission):
    message = 'Tier does not allow to see original size image.'

    def has_permission(self, request, view):
        return request.user.tier.can_original_image


class LinksCreatingPermission(permissions.BasePermission):
    message = 'Tier does not allow to create expiring links.'

    def has_permission(self, request, view):
        return request.user.tier.can_expiring_link

