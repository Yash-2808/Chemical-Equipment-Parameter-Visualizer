import pandas as pd
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import EquipmentDataset, Equipment
from .serializers import (
    EquipmentDatasetSerializer, DatasetListSerializer, 
    CSVUploadSerializer, EquipmentSerializer
)
from .utils import generate_dataset_report, generate_charts_pdf
from .authentication import SimpleAPIKeyAuthentication


@authentication_classes([SimpleAPIKeyAuthentication])
@permission_classes([permissions.IsAuthenticated])
class EquipmentDatasetViewSet(viewsets.ModelViewSet):
    queryset = EquipmentDataset.objects.all()
    serializer_class = EquipmentDatasetSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DatasetListSerializer
        return EquipmentDatasetSerializer
    
    def get_queryset(self):
        # For list view, return only last 5 datasets
        if self.action == 'list':
            return EquipmentDataset.objects.all()[:5]
        # For detail view, return all datasets so specific objects can be found
        return EquipmentDataset.objects.all()
    
    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        """Upload and process CSV file"""
        serializer = CSVUploadSerializer(data=request.data)
        if serializer.is_valid():
            csv_file = serializer.validated_data['file']
            dataset_name = serializer.validated_data.get('dataset_name', csv_file.name)
            
            try:
                # Read CSV file
                df = pd.read_csv(csv_file)
                
                # Validate required columns
                required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    return Response(
                        {'error': f'Missing required columns: {", ".join(missing_columns)}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Calculate summary statistics
                total_count = len(df)
                avg_flowrate = df['Flowrate'].mean()
                avg_pressure = df['Pressure'].mean()
                avg_temperature = df['Temperature'].mean()
                
                with transaction.atomic():
                    # Create dataset record
                    dataset = EquipmentDataset.objects.create(
                        name=dataset_name,
                        file_name=csv_file.name,
                        total_count=total_count,
                        avg_flowrate=avg_flowrate,
                        avg_pressure=avg_pressure,
                        avg_temperature=avg_temperature
                    )
                    
                    # Create equipment records
                    equipment_objects = []
                    for _, row in df.iterrows():
                        equipment_objects.append(Equipment(
                            dataset=dataset,
                            name=row['Equipment Name'],
                            type=row['Type'],
                            flowrate=float(row['Flowrate']),
                            pressure=float(row['Pressure']),
                            temperature=float(row['Temperature'])
                        ))
                    
                    Equipment.objects.bulk_create(equipment_objects)
                
                # Return created dataset with full details
                serializer = EquipmentDatasetSerializer(dataset)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response(
                    {'error': f'Error processing CSV file: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def equipment(self, request, pk=None):
        """Get all equipment for a specific dataset"""
        dataset = self.get_object()
        equipment = dataset.equipment.all()
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get detailed summary statistics for a dataset"""
        dataset = self.get_object()
        equipment = dataset.equipment.all()
        
        # Type distribution
        type_stats = {}
        for item in equipment:
            type_stats[item.type] = type_stats.get(item.type, 0) + 1
        
        # Calculate statistics
        flowrates = [item.flowrate for item in equipment]
        pressures = [item.pressure for item in equipment]
        temperatures = [item.temperature for item in equipment]
        
        summary = {
            'dataset_info': {
                'name': dataset.name,
                'upload_date': dataset.upload_date,
                'total_count': dataset.total_count
            },
            'statistics': {
                'flowrate': {
                    'avg': sum(flowrates) / len(flowrates) if flowrates else 0,
                    'min': min(flowrates) if flowrates else 0,
                    'max': max(flowrates) if flowrates else 0,
                },
                'pressure': {
                    'avg': sum(pressures) / len(pressures) if pressures else 0,
                    'min': min(pressures) if pressures else 0,
                    'max': max(pressures) if pressures else 0,
                },
                'temperature': {
                    'avg': sum(temperatures) / len(temperatures) if temperatures else 0,
                    'min': min(temperatures) if temperatures else 0,
                    'max': max(temperatures) if temperatures else 0,
                }
            },
            'type_distribution': type_stats
        }
        
        return Response(summary)
    
    @action(detail=True, methods=['get'])
    def generate_pdf_report(self, request, pk=None):
        """Generate PDF report for a dataset"""
        dataset = self.get_object()
        equipment = dataset.equipment.all()
        summary_data = None
        
        try:
            # Get summary data
            summary_response = self.summary(request, pk)
            if summary_response.status_code == 200:
                summary_data = summary_response.data
            
            # Generate PDF report
            pdf_content = generate_dataset_report(dataset, equipment, summary_data)
            
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.name.replace(" ", "_")}.pdf"'
            return response
            
        except Exception as e:
            return Response(
                {'error': f'Error generating PDF report: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def generate_charts_pdf(self, request, pk=None):
        """Generate charts PDF for a dataset"""
        dataset = self.get_object()
        
        try:
            # Get summary data for charts
            summary_response = self.summary(request, pk)
            if summary_response.status_code != 200:
                return Response(
                    {'error': 'Could not retrieve summary data for charts'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            summary_data = summary_response.data
            
            # Generate charts PDF
            pdf_content = generate_charts_pdf(dataset, summary_data)
            
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="equipment_charts_{dataset.name.replace(" ", "_")}.pdf"'
            return response
            
        except Exception as e:
            return Response(
                {'error': f'Error generating charts PDF: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@authentication_classes([SimpleAPIKeyAuthentication])
@permission_classes([permissions.IsAuthenticated])
class EquipmentViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for individual equipment items"""
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    
    def get_queryset(self):
        queryset = Equipment.objects.all()
        dataset_id = self.request.query_params.get('dataset_id')
        equipment_type = self.request.query_params.get('type')
        
        if dataset_id:
            queryset = queryset.filter(dataset_id=dataset_id)
        if equipment_type:
            queryset = queryset.filter(type__icontains=equipment_type)
            
        return queryset


@authentication_classes([SimpleAPIKeyAuthentication])
@permission_classes([permissions.IsAuthenticated])
class AnalyticsView(APIView):
    """Global analytics across all datasets"""
    
    def get(self, request):
        datasets = EquipmentDataset.objects.all()
        all_equipment = Equipment.objects.all()
        
        # Overall statistics
        total_datasets = datasets.count()
        total_equipment = all_equipment.count()
        
        # Type distribution across all datasets
        type_distribution = {}
        for equipment in all_equipment:
            type_distribution[equipment.type] = type_distribution.get(equipment.type, 0) + 1
        
        # Recent datasets (last 5)
        recent_datasets = datasets[:5]
        recent_data = []
        for dataset in recent_datasets:
            recent_data.append({
                'id': dataset.id,
                'name': dataset.name,
                'upload_date': dataset.upload_date,
                'equipment_count': dataset.equipment.count()
            })
        
        analytics = {
            'overview': {
                'total_datasets': total_datasets,
                'total_equipment': total_equipment,
                'type_distribution': type_distribution
            },
            'recent_datasets': recent_data
        }
        
        return Response(analytics)
