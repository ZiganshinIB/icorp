from zlib import adler32

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from ldap_service import LDAPService
from .serializers import ADUserSerializer

ad = LDAPService()


class ADUserViewSet(APIView):
    serializer_class = ADUserSerializer

    # get list of AD users
    def get(self, request, format=None):
        users = ad.get_users()
        return Response


# Create your views here.
