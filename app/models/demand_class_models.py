from django.db import models

# Create your models here.

class DemandClassData(models.Model):
    household_id = models.CharField(max_length=100,primary_key=True)
    date = models.CharField(max_length=10)
    hour = models.BigIntegerField()
    minute = models.BigIntegerField()
    total = models.FloatField()
    val1 = models.FloatField()
    val2 = models.FloatField()
    val3 = models.FloatField()
    val4 = models.FloatField()
    val5 = models.FloatField()
    val6 = models.FloatField()
    val7 = models.FloatField()
    val8 = models.FloatField()
    val9 = models.FloatField()
    remove = models.BigIntegerField()
    
    class Meta:
        db_table = 't_energy_data_after_screening'

