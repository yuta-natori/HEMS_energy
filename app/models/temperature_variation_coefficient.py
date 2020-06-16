from django.db import models

# Create your models here.

class TemperatureVariationCoefficient(models.Model):
    status = models.BigIntegerField(primary_key=True)
    coefficient = models.FloatField(null=True)
    intercept = models.FloatField(null=True)
    
    class Meta:
        db_table = 't_temperature_variation_coefficient'