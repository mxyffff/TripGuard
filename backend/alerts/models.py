from django.db import models

class TravelAlert(models.Model):
    alarm_level = models.IntegerField()
    continent_code = models.CharField(max_length=10)
    continent_name_kr = models.CharField(max_length=100)
    continent_name_en = models.CharField(max_length=100)
    country_name_kr = models.CharField(max_length=100)
    country_name_en = models.CharField(max_length=100)
    country_iso_alpha2 = models.CharField(max_length=2)
    flag_url = models.URLField()
    map_url = models.URLField()
    dang_map_url = models.URLField()
    region_type = models.CharField(max_length=50)
    remark = models.TextField()
    written_date = models.DateField()

    def __str__(self):
        return f"{self.country_name_kr} ({self.country_iso_alpha2})"
