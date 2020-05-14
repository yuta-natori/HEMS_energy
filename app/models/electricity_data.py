from django.db import models

# Create your models here.

class ElectricityData(models.Model):
    area = models.CharField(max_length=10)
    household_id = models.CharField(max_length=10)
    date = models.CharField(max_length=10)
    hour = models.BigIntegerField()
    minute = models.BigIntegerField()
    total = models.FloatField()
    val1 = models.FloatField()
    val2 = models.FloatField()
    val3 = models.FloatField()
    val4 = models.FloatField()
    val5= models.FloatField()
    val6 = models.FloatField()
    val7 = models.FloatField()
    val8 = models.FloatField()
    val9 = models.FloatField()
    val10 = models.FloatField()
    
    class Meta:
        db_table = 'm_electricity_data'
        unique_together = ('area', 'household_id', 'date', 'hour', 'minute')