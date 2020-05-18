from django.db import models

# Create your models here.

class PowerDemandProfile(models.Model):
    month = models.BigIntegerField()
    hour = models.BigIntegerField()
    total = models.FloatField()
    rate = models.FloatField()
    
    class Meta:
        db_table = 't_power_demand_profile'
        unique_together = ('month', 'hour')