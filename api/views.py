from rest_framework import viewsets, generics, views, permissions, mixins, decorators


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


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

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


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

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
