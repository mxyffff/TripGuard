from django.db import models

class Alert(models.Model):
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    alarm_level = models.IntegerField()
    continent_name = models.CharField(max_length=100)
    written_dt = models.DateField()
    region_type = models.CharField(max_length=100)
    remark = models.TextField()
    map_url = models.URLField()
    flag_url = models.URLField()

    def __str__(self):
        return f"{self.country_name} ({self.country_code})"