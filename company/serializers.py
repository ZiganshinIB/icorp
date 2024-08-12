from django.contrib.auth import get_user_model
from rest_framework import serializers
from phonenumber_field import validators
from .models import Site, Department, Position, Company

User = get_user_model()


class EmployCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'birthday', 'company', 'position', 'department', 'site')
        extra_kwargs = {'password': {'write_only': True}}


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('short_name', 'name', 'inn',
                  'city',
                  'address',
                  'website', 'email', 'phone_number', 'employees_count', 'industry', 'description')
        # city, address, website, email, phone_number - не обязательные поля

    def create(self, validated_data):
        return Company.objects.create(**validated_data)

    def validate_phone_number(self, value):
        try:
            validators.validate_international_phonenumber(value)
        except Exception:
            raise serializers.ValidationError('Телефон должен быть в формате +7XXXXXXXXXX')
        return value



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


