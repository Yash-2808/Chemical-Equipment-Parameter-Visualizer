from rest_framework import serializers
from .models import EquipmentDataset, Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'type', 'flowrate', 'pressure', 'temperature']


class EquipmentDatasetSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    equipment_count = serializers.SerializerMethodField()
    type_distribution = serializers.SerializerMethodField()
    
    class Meta:
        model = EquipmentDataset
        fields = [
            'id', 'name', 'file_name', 'upload_date', 'total_count',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'equipment', 'equipment_count', 'type_distribution'
        ]
    
    def get_equipment_count(self, obj):
        return obj.equipment.count()
    
    def get_type_distribution(self, obj):
        """Get distribution of equipment types"""
        distribution = {}
        for equipment in obj.equipment.all():
            distribution[equipment.type] = distribution.get(equipment.type, 0) + 1
        return distribution


class DatasetListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for dataset list view"""
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EquipmentDataset
        fields = [
            'id', 'name', 'file_name', 'upload_date', 'total_count',
            'avg_flowrate', 'avg_pressure', 'avg_temperature', 'equipment_count'
        ]
    
    def get_equipment_count(self, obj):
        return obj.equipment.count()


class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    dataset_name = serializers.CharField(max_length=255, required=False)
    
    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size must be less than 10MB.")
        return value
