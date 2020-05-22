from django.db import models

# Create your models here.

class ElectricityData(models.Model):
    area = models.CharField(max_length=10)
    household_id = models.CharField(max_length=20)
    date = models.CharField(max_length=10)
    hour = models.BigIntegerField()
    minute = models.BigIntegerField()
    total = models.FloatField()
    val1 = models.CharField(max_length=10)
    val2 = models.CharField(max_length=10)
    val3 = models.CharField(max_length=10)
    val4 = models.CharField(max_length=10)
    val5= models.CharField(max_length=10)
    val6 = models.CharField(max_length=10)
    val7 = models.CharField(max_length=10)
    val8 = models.CharField(max_length=10)
    val9 = models.CharField(max_length=10)
    val10 = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'm_electricity_data'
        unique_together = ('area', 'household_id', 'date', 'hour', 'minute')