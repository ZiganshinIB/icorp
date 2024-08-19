from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Group(models.Model):
    # CN
    name = models.CharField("Название", max_length=255, unique=True)
    # Category
    category = models.CharField('Category', max_length=255)
    ds_name = models.CharField('DS', max_length=255)
    ou = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True, related_name='groups')

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField("Название", max_length=255, unique=True)
    parent_organization = models.ForeignKey('self',
                                            on_delete=models.CASCADE,
                                            null=True,
                                            blank=True,
                                            related_name='sub_organizations',
                                            verbose_name='Родительская организация')

    def __str__(self):
        return self.name
