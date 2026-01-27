from django.core.management.base import BaseCommand
from equipment.models import EquipmentDataset, Equipment
import pandas as pd
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Load sample equipment data from CSV file'

    def handle(self, *args, **options):
        # Path to sample CSV file
        csv_path = os.path.join(settings.BASE_DIR.parent, 'sample_equipment_data.csv')
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR('Sample CSV file not found'))
            return

        try:
            # Read CSV data
            df = pd.read_csv(csv_path)
            
            # Create dataset
            dataset = EquipmentDataset.objects.create(
                name="Sample Equipment Data",
                file_name="sample_equipment_data.csv",
                total_count=len(df)
            )

            # Create equipment records
            equipment_objects = []
            for _, row in df.iterrows():
                equipment_objects.append(Equipment(
                    dataset=dataset,
                    name=row['name'],
                    type=row['type'],
                    flowrate=row['flowrate'],
                    pressure=row['pressure'],
                    temperature=row['temperature']
                ))

            Equipment.objects.bulk_create(equipment_objects)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully loaded {len(equipment_objects)} equipment records for dataset "{dataset.name}"'
                )
            )
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading sample data: {str(e)}'))
