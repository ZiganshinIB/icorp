from django.contrib import admin
from .models import Material, Location, Guarantee, Category, Equipment, Consumable, Service

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("title", )

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("title",)

@admin.register(Guarantee)
class GuaranteeAdmin(admin.ModelAdmin):
    list_display = ("title", "date_start", "date_end")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("title", "material")

    def title(self, obj):
        return obj.__str__()

@admin.register(Consumable)
class ConsumableAdmin(admin.ModelAdmin):
    list_display = ("title", "material")

    def title(self, obj):
        return obj.material.title



