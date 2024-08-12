from rest_framework import serializers
from .models import Site, Department, Position, Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('short_name', 'name', 'inn',
                  'city',
                  'address',
                  'website', 'email', 'phone_number', 'employees_count', 'industry', 'description')
        # city, address, website, email, phone_number - не обязательные поля



class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


