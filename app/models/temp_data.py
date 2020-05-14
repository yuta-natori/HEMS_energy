from django.db import models

# Create your models here.

class TempData(models.Model):
    area = models.CharField(max_length=10)
    date = models.CharField(max_length=10)
    temperature = models.FloatField()
    
    class Meta:
        db_table = 'm_temp_data'
        unique_together = ('area', 'date')