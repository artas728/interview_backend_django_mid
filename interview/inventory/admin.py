from django.contrib import admin
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage, InventoryTag

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'language')
    search_fields = ('name', 'type__name', 'language__name')
    list_filter = ('type', 'language')

@admin.register(InventoryType)
class InventoryTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(InventoryLanguage)
class InventoryLanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(InventoryTag)
class InventoryTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
