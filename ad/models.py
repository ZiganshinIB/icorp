from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Group(models.Model):
    # CN
    name = models.CharField("Название", max_length=255, unique=True)
    # Category
    category = models.CharField('Category', max_length=255)
    ds_name = models.CharField('DS', max_length=255)

    def __str__(self):
        return self.name



