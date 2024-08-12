from rest_framework import permissions


class CanModel(permissions.BasePermission):
    def __init__(self, model_name, action):
        self.model_name = model_name
        self.action = action

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm(f'{self.model_name}.{self.action}_{self.model_name}')


class CanCreateCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.add_company')


class CanUpdateCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.change_company')


class CanDeleteCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.delete_company')


class CanReadCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.view_company')


class CanCreateSite(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.add_site')


class CanUpdateSite(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.change_site')


class CanDeleteSite(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.delete_site')


class CanReadSite(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.view_site')


class CanCreatePosition(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.add_position')


class CanUpdatePosition(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.change_position')


class CanDeletePosition(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.delete_position')


class CanReadPosition(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.view_position')


class CanCreateDepartment(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.add_department')


class CanUpdateDepartment(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.change_department')


class CanDeleteDepartment(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.delete_department')


class CanReadDepartment(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.view_department')


