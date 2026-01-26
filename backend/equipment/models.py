from django.db import models
from django.utils import timezone


class EquipmentDataset(models.Model):
    """Store uploaded CSV datasets with summary information"""
    name = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(default=timezone.now)
    total_count = models.IntegerField()
    avg_flowrate = models.FloatField(null=True, blank=True)
    avg_pressure = models.FloatField(null=True, blank=True)
    avg_temperature = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-upload_date']
        verbose_name = "Equipment Dataset"
        verbose_name_plural = "Equipment Datasets"
    
    def __str__(self):
        return f"{self.name} ({self.upload_date.strftime('%Y-%m-%d %H:%M')})"


class Equipment(models.Model):
    """Individual equipment records"""
    dataset = models.ForeignKey(EquipmentDataset, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"
        indexes = [
            models.Index(fields=['dataset']),
            models.Index(fields=['type']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.type})"
