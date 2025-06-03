from django.core.management.base import BaseCommand
from backend.models import TravelAlert
import requests
import xml.etree.ElementTree as ET
from decouple import config
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch travel alerts from MOFA (외교부) API'

    def handle(self, *args, **kwargs):
        service_key = config('MOFA_API_KEY')
        url = f'http://apis.data.go.kr/1262000/CountryAlarmService/getCountryAlarmList?serviceKey={service_key}&numOfRows=100&pageNo=1'

        self.stdout.write('📡 외교부 API에서 여행경보 데이터를 가져오는 중...')

        response = requests.get(url)

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            items = root.find('.//items')
            count = 0

            for item in items.findall('item'):
                country = item.findtext('countryName', default='Unknown')
                level = item.findtext('alarmLvl', default='0')
                written_dt_str = item.findtext('writtenDt', default='2000-01-01 00:00:00')

                try:
                    written_dt = datetime.strptime(written_dt_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    written_dt = datetime.now()

                TravelAlert.objects.update_or_create(
                    country_name=country,
                    defaults={
                        'alert_level': level,
                        'updated_at': written_dt
                    }
                )
                count += 1

            self.stdout.write(self.style.SUCCESS(f'✅ {count}개 국가 경보 정보가 업데이트되었습니다.'))
        else:
            self.stderr.write(self.style.ERROR(f'❌ 요청 실패 - 상태 코드 {response.status_code}'))
