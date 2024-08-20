from django.contrib.auth.password_validation import password_changed
from rest_framework import serializers
from .ldap_service import LDAPService
ad = LDAPService()

class ADUserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    path_ou = serializers.CharField()
    position = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(required=False)

    def create(self, validated_data):
        ad.connect()
        print(validated_data)
        ad.create_user(
            **validated_data)
        return validated_data
