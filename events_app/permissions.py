from rest_framework import permissions

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and not request.user.cust_type

class IsOrganizer(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        print(request.user.cust_type)
        return request.user and request.user.cust_type

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return True
        else:
            False