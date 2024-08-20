from rest_framework import permissions

class IsGetRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'

class CanViewADUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.has_group('ad_admin') or request.user.username == request.GET.get('username'))

class RequireUsernameParam(permissions.BasePermission):
    message = 'Не был передан параметр username'
    def has_permission(self, request, view):
        if request.method == 'GET':
            if 'username' not in request.query_params:
                return False
        return True


class CanCreateADUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_group('ad_admin')


class CanModel(permissions.BasePermission):
    def __init__(self, model_name, action):
        self.model_name = model_name
        self.action = action

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm(f'{self.model_name}.{self.action}_{self.model_name}')


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CanCreateEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.create_employee')


class CanViewPosition(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.view_position')


class CanCreatePosition(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.add_position')


class CanUpdatePosition(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.change_position')


class CanDeletePosition(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('company.delete_position')


class CanViewTask(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('task.view_task')


class CanCreateTask(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('task.add_task')


class CanUpdateTask(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('task.change_task')


class CanDeleteTask(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.has_perm('task.delete_task')


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


