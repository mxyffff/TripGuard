import requests
from django.core.management.base import BaseCommand
from alerts.models import TravelAlert
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch travel alerts from MOFA API'

    def handle(self, *args, **kwargs):
        url = 'https://apis.data.go.kr/1262000/TravelWarningService/getTravelWarningList'
        params = {
            'serviceKey': 'jT%2BQ4DOdKXTFolmGz1Dc5zu0wiHpEBMiXar01c9qfg8AnazFkPC0k8cklvYJETq28XP0Za6hsipzL3lhtAFOxA%3D%3D',
            'returnType': 'JSON',
            'numOfRows': 100,
            'pageNo': 1,
        }

        response = requests.get(url, params=params)
        data = response.json()

        items = data['response']['body']['items']['item']

        TravelAlert.objects.all().delete()  # 기존 데이터 삭제

        for item in items:
            TravelAlert.objects.create(
                alarm_level = item['alarm_lvl'],
                continent_code = item['continent_cd'],
                continent_name_kr = item['continent_nm'],
                continent_name_en = item['continent_eng_nm'],
                country_name_kr = item['country_nm'],
                country_name_en = item['country_eng_nm'],
                country_iso_alpha2 = item['country_iso_alp2'],
                flag_url = item['flag_download_url'],
                map_url = item['map_download_url'],
                dang_map_url = item['dang_map_download_url'],
                region_type = item['region_ty'],
                remark = item['remark'],
                written_date = datetime.strptime(item['written_dt'], "%Y-%m-%d").date()
            )

        self.stdout.write(self.style.SUCCESS('Travel alerts updated successfully.'))
