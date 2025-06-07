from django.contrib import admin

# Register your models here.

from .models import TravelAlert

@admin.register(TravelAlert)
class TravelAlertAdmin(admin.ModelAdmin):
    list_display = ('country_name_kr', 'alarm_level', 'written_date')
    list_filter = ('alarm_level', 'continent_name_kr')
    search_fields = ('country_name_kr', 'country_iso_alpha2')

