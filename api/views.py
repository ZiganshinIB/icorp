from rest_framework import viewsets, generics, views, permissions, mixins, decorators
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

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

ad = LDAPService()


@api_view(http_method_names=['POST'])
def get_ADUser(request):
    response = {'username': request.data['username'], 'groups': []}
    cd = request.data
    cd['username'] = cd['username'].lower()
    ad_user = ad.get_object_by_ds(cd['username'])
    for group in ad_user.get('memberOf', []):
        response['groups'].append(
            ad.get_object_by_ds(
                ds_name=group,
                attributes=[ 'sAMAccountName'],
                object_class='group')
            ['sAMAccountName']
        )

    if not ad_user:
        raise NotFound
    return Response(response)


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
