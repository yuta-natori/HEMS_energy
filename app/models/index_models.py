from django.db import models

# Create your models here.

class HolidayData(models.Model):
    date = models.CharField(max_length=10,primary_key=True)
    is_holiday = models.BigIntegerField()
    
    class Meta:
        db_table = 'm_holiday_data'

