from django.contrib import admin
from .models import Person, UserGroup



class UserGroupInline(admin.TabularInline):
    model = UserGroup
    extra = 1


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    inlines = [UserGroupInline]
