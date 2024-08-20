from rest_framework import viewsets, generics, views, permissions, mixins, decorators, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from setuptools.command.build_ext import if_dl

from ad.serializers import ADUserCreateSerializer
# Company
from company.models import Company
from company.serializers import CompanySerializer
from .permissions import CanCreateCompany, CanUpdateCompany, CanDeleteCompany
# Site
from company.models import Site
from company.serializers import SiteSerializer
from .permissions import CanCreateSite, CanUpdateSite, CanDeleteSite
# Position
from company.models import Position
from company.serializers import PositionSerializer
from .permissions import CanCreatePosition, CanUpdatePosition, CanDeletePosition
# Department
from company.models import Department
from company.serializers import DepartmentSerializer
from .permissions import CanCreateDepartment, CanUpdateDepartment, CanDeleteDepartment
# Task
from task.models import Task
from task.serializers import TaskSerializer
from .permissions import IsOwner, CanViewTask, CanCreateTask, CanUpdateTask, CanDeleteTask
from ad.ldap_service import LDAPService

from .permissions import CanViewADUser, CanCreateADUser, RequireUsernameParam

ad = LDAPService()


def get_user_status(status_code):
    if status_code & 0x0002:
        return 'Account disabled'
    if status_code & 0x0008:
        return 'Account expired'
    if status_code & 0x0010:
        return 'Password expired'
    if status_code & 0x0020:
        return 'Password not required'
    if status_code & 0x0040:
        return 'Account locked'
    return 'Active'


class ADUserViewSet(viewsets.ViewSet):

    def get_permissions(self):
        if self.action == 'create':
            permission = [CanCreateADUser]
        elif self.action == 'update':
            permission = [CanUpdateCompany]
        elif self.action == 'destroy':
            permission = [CanDeleteCompany]
        elif self.action == 'retrieve':
            permission = [CanViewADUser]
        else:
            permission = [permissions.IsAuthenticated]
        return [permission_class() for permission_class in permission]

    def retrieve(self, request):
        username = request.query_params.get('username')
        if username is None:
            return Response(
                {"error": "The 'username' parameter is required."},
                status=status.HTTP_400_BAD_REQUEST  # Возвращаем статус 400 Bad Request
            )
        ad.connect()
        response = {'username': username, 'groups': []}
        ad_user = ad.search_user(
            username,
            attributes=['memberOf', 'DistinguishedName', 'mail', 'title', 'department', 'userAccountControl', 'displayName',
                        "givenName", 'sn'])
        response['fullname'] = str(ad_user['displayName'] if ad_user['displayName'] else '')
        response['first_name'] = str(ad_user['givenName'] if ad_user['givenName'] else '')
        response['last_name'] = str(ad_user['sn'] if ad_user['sn'] else '')
        response['DistinguishedName'] = str(ad_user['DistinguishedName'])
        response['email'] = str(ad_user['mail'] if ad_user['mail'] else '')
        response['position'] = str(ad_user['title'] if ad_user['title'] else '')
        response['department'] = str(ad_user['department'] if ad_user['department'] else '')
        response['satus'] = get_user_status(ad_user.userAccountControl.value)
        for group in ad_user['memberOf']:
            g = ad.get_object_by_ds(
                ds_name=group,
                attributes=['sAMAccountName'],
                object_class='group')
            response['groups'].append({'name': str(g['sAMAccountName']), 'distinguishedName': str(group)})
        if not ad_user:
            raise Response(status=status.HTTP_404_NOT_FOUND)
        return Response(response)

    def create(self, request):
        serializer = ADUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            permission = [CanCreateCompany]
        elif self.action == 'update':
            permission = [CanUpdateCompany]
        elif self.action == 'destroy':
            permission = [CanDeleteCompany]
        else:
            permission = [permissions.IsAuthenticated]
        return [permission_class() for permission_class in permission]


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission = [CanCreateSite]
        elif self.action == 'update':
            permission = [CanUpdateSite]
        elif self.action == 'destroy':
            permission = [CanDeleteSite]
        else:
            permission = [permissions.IsAuthenticated]
        return [permission_class() for permission_class in permission]

    def get_queryset(self):
        company_id = self.request.query_params.get('company_id', None)
        if company_id is not None:
            return self.queryset.filter(company_id=company_id)
        return self.queryset


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            permission = [CanCreateDepartment]
        elif self.action == 'update':
            permission = [CanUpdateDepartment]
        elif self.action == 'destroy':
            permission = [CanDeleteDepartment]
        else:
            permission = [permissions.IsAuthenticated]
        return [permission_class() for permission_class in permission]

    def get_queryset(self):
        site_id = self.request.query_params.get('site_id', None)
        if site_id is not None:
            return self.queryset.filter(site_id=site_id)
        company_id = self.request.query_params.get('company_id', None)
        if company_id is not None:
            return self.queryset.filter(company_id=company_id)
        return self.queryset


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission = [CanCreatePosition]
        elif self.action == 'update':
            permission = [CanUpdatePosition]
        elif self.action == 'destroy':
            permission = [CanDeletePosition]
        else:
            permission = [permissions.IsAuthenticated]
        return [permission_class() for permission_class in permission]

    def get_queryset(self):
        department_id = self.request.query_params.get('department_id', None)
        if department_id is not None:
            return self.queryset.filter(department_id=department_id)
        site_id = self.request.query_params.get('site_id', None)
        if site_id is not None:
            return self.queryset.filter(department__site_id=site_id)
        company_id = self.request.query_params.get('company_id', None)
        if company_id is not None:
            return self.queryset.filter(department__site__company_id=company_id)
        return self.queryset


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission = [permissions.IsAuthenticated]
        elif self.action == 'update':
            permission = [CanUpdateTask, IsOwner]
        elif self.action == 'destroy':
            permission = [CanDeleteTask]
        elif self.action == 'retrieve':
            permission = [CanViewTask, IsOwner]
        else:
            permission = [CanViewTask, IsOwner]
        return [permission_class() for permission_class in permission]
