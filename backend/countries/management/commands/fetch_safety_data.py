import requests
import xmltodict
import json
from django.core.management.base import BaseCommand
from countries.models import CountrySafety

import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

# 안전 정보 API - [안전 공지]

# 커스텀 TLS 어댑터 (SSL 오류)
class TLSv1_2HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT@SECLEVEL=1")
        context.options |= ssl.OP_NO_TLSv1_3
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

class Command(BaseCommand):
    help = '외교부 API(getCountrySafetyList)로부터 지역 안전 공지를 가져온다.'

    # API 요청
    def handle(self, *args, **kwargs):
        service_key = 't6G5D0EXlmcbAUoDA9t04kUw9N83jcIrQ3qcANfLy0aTuOnhhy%2BF7uGeFQD8s1lKym8BYzsGy0G6ToGC6zNk2A%3D%3D'
        url = f'https://apis.data.go.kr/1262000/CountrySafetyService/getCountrySafetyList?serviceKey={service_key}&numOfRows=100&pageNo=1'

        self.stdout.write(self.style.NOTICE("안전 공지 API 요청 중..."))

        # 세션 설정 및 SSL 버그 우회
        session = requests.Session()
        session.mount("https://", TLSv1_2HttpAdapter())

        response = session.get(url)

        # JSON 구조로 변환
        data_dict = xmltodict.parse(response.content)
        json_data = json.loads(json.dumps(data_dict))

        # 응답 구조 확인용
        print(json.dumps(json_data, indent=2, ensure_ascii=False))

        items = json_data["response"]["body"]["items"]["item"]
        # item이 dict이면 list로 변환
        if isinstance(items, dict):
            items = [items]

        count = 0

        for item in items:
            country_name = item.get("countryName")
            country_en_name = item.get("countryEnName")

            # 필수 필드가 없는 경우는 건너뛰기
            if not country_name or not country_en_name:
                continue

            safety_id = item.get("id")

            CountrySafety.objects.update_or_create(
                safety_id=safety_id,
                defaults={
                    "country_name": item.get("countryName"),
                    "country_en_name": item.get("countryEnName"),
                    "title": item.get("title"),
                    "content": item.get("content"),
                    "file_url": item.get("fileUrl") or None,
                    "written_dt": item.get("wrtDt"),
                }
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {count}건의 안전정보 데이터를 성공적으로 저장했습니다."))