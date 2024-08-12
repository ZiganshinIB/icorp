from django.contrib import admin

from .models import Company, Position, Department, Site


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'site')


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')


