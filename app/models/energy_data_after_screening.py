from django.db import models

# Create your models here.
class EnergyDataAfterScreening(models.Model):
    household_id = models.CharField(max_length=20)
    date = models.CharField(max_length=10)
    hour = models.BigIntegerField()
    minute = models.BigIntegerField()
    total = models.FloatField(null=True)
    val1 = models.CharField(max_length=10, null=True)
    val2 = models.CharField(max_length=10, null=True)
    val3 = models.CharField(max_length=10, null=True)
    val4 = models.CharField(max_length=10, null=True)
    val5= models.CharField(max_length=10, null=True)
    val6 = models.CharField(max_length=10, null=True)
    val7 = models.CharField(max_length=10, null=True)
    val8 = models.CharField(max_length=10, null=True)
    val9 = models.CharField(max_length=10, null=True)
    val10 = models.CharField(max_length=10, null=True)
    
    class Meta:
        db_table = 't_energy_data_after_screening'
        unique_together = ('household_id', 'date', 'hour', 'minute')