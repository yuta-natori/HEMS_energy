from django.db import models

# Create your models here.

class TemperatureVariationCoefficient(models.Model):
    status = models.BigIntegerField(primary_key=True)
    coefficient = models.FloatField()
    intercept = models.FloatField()
    
    class Meta:
        db_table = 't_temperature_variation_coefficient'