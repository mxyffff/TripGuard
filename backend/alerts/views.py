from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Alert

def alert_geojson(request):
    features = []

    for alert in Alert.objects.all():
        features.append({
            "type": "Feature",
            "properties": {
                "country_name": alert.country_name,
                "alarm_level": alert.alarm_level,
                "country_code": alert.country_code,
            },
        })

    return JsonResponse({
        "type": "FeatureCollection",
        "features": features
    })

def alert_detail(request, country_code):
    alert = get_object_or_404(Alert, country_code=country_code.upper())

    return JsonResponse({
        "country_name": alert.country_name,
        "country_code": alert.country_code,
        "alarm_level": alert.alarm_level,
        "continent_name": alert.continent_name,
        "written_dt": alert.written_dt,
        "region_type": alert.region_type,
        "remark": alert.remark,
        "map_url": alert.map_url,
        "flag_url": alert.flag_url
    })

def homePage(request):
    return render(request, 'homePage.html')
