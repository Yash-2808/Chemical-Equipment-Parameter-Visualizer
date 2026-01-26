from django.contrib import admin
from .models import EquipmentDataset, Equipment


class EquipmentInline(admin.TabularInline):
    model = Equipment
    extra = 0
    readonly_fields = ('name', 'type', 'flowrate', 'pressure', 'temperature')
    can_delete = False
    max_num = 0


@admin.register(EquipmentDataset)
class EquipmentDatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'file_name', 'upload_date', 'total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature']
    list_filter = ['upload_date']
    search_fields = ['name', 'file_name']
    readonly_fields = ['upload_date', 'total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature']
    inlines = [EquipmentInline]
    
    def has_add_permission(self, request):
        return False  # Datasets should only be created via CSV upload


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'flowrate', 'pressure', 'temperature', 'dataset']
    list_filter = ['type', 'dataset']
    search_fields = ['name', 'type']
    readonly_fields = ('dataset',)
    
    def has_add_permission(self, request):
        return False  # Equipment should only be created via CSV upload
