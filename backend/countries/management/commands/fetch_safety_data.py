import requests
import xmltodict
import json
from django.core.management.base import BaseCommand
from countries.models import CountrySafety

import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

# 안전 정보 API - [안전 공지]

# SSL 오류 방지용 커스텀 어댑터
class TLSv1_2HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT@SECLEVEL=1")  # 낮은 보안 수준 허용
        context.options |= ssl.OP_NO_TLSv1_3  # TLS 1.3 비활성화
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

class Command(BaseCommand):
    help = '외교부 API(getCountrySafetyList)로부터 지역 안전 공지를 가져온다.'

    # API 요청
    def handle(self, *args, **kwargs):
        service_key = 't6G5D0EXlmcbAUoDA9t04kUw9N83jcIrQ3qcANfLy0aTuOnhhy%2BF7uGeFQD8s1lKym8BYzsGy0G6ToGC6zNk2A%3D%3D'
        url = f'https://apis.data.go.kr/1262000/CountrySafetyService/getCountrySafetyList?serviceKey={service_key}&numOfRows=100&pageNo=1'

        self.stdout.write(self.style.NOTICE("안전 공지 API 요청 중..."))

        # 세션 설정 및 TLS 우회 어댑터 등록
        session = requests.Session()
        session.mount("https://", TLSv1_2HttpAdapter())

        try:
            # API 요청 실행
            response = session.get(url)
            self.stdout.write(f"응답 상태 코드: {response.status_code}") # 응답 상태 코드 출력

            # 200이 아닐 경우 에러 처리
            if response.status_code != 200:
                self.stderr.write("❌ API 요청 실패 (status != 200)")
                return

            # JSON 구조로 변환
            data_dict = xmltodict.parse(response.content)
            json_data = json.loads(json.dumps(data_dict))
            items = json_data["response"]["body"]["items"]["item"] # 안전 정보 데이터 추출

        except Exception as e:
            self.stderr.write(f"❌ 요청 또는 XML → JSON 변환 실패: {e}")
            return

        # 단일 객체로 응답된 경우 리스트로 반환
        if isinstance(items, dict):
            items = [items]

        # DB 저장 건수 초기화
        count = 0

        # 각 재외공관 item에 대해 DB 저장 반복
        for item in items:
            country_name = item.get("countryName")
            country_en_name = item.get("countryEnName")

            # 필수 필드가 없는 경우는 건너뛰기
            if not country_name or not country_en_name:
                continue

            safety_id = item.get("id")

            # DB에 저장 (있으면 업데이트, 없으면 생성)
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