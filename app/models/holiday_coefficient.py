from django.db import models

# Create your models here.

class HolidayCoefficient(models.Model):
    is_holiday = models.BigIntegerField(primary_key=True)
    holiday_coef = models.FloatField()
    
    class Meta:
        db_table = 't_holiday_coefficient'