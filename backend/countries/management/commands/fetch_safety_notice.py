from unicodedata import category

import requests
import xmltodict
import json
from django.core.management.base import BaseCommand
from countries.models import SafetyNotice

import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

# 안전 공지 api 모델 - [유의 지역 정보]

# 커스텀 TLS 어댑터 (SSL 오류)
class TLSv1_2HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT@SECLEVEL=1")
        context.options |= ssl.OP_NO_TLSv1_3
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

# BaseCommand 상속
class Command(BaseCommand):
    help = '외교부 API(getCountrySafetyNoticeList)를 통해 유의 지역 공지 데이터를 가져온다.'

    def handle(self, *args, **kwargs):
        service_key = 't6G5D0EXlmcbAUoDA9t04kUw9N83jcIrQ3qcANfLy0aTuOnhhy%2BF7uGeFQD8s1lKym8BYzsGy0G6ToGC6zNk2A%3D%3D'
        url = (
            f'https://apis.data.go.kr/1262000/CountrySafetyService6/getCountrySafetyList6?serviceKey={service_key}&numOfRows=100&pageNo=1'
        )

        self.stdout.write(self.style.NOTICE("유의 지역 정보 API 요청 중..."))

        # 세션 설정 및 SSL 버그 우회
        session = requests.Session()
        session.mount("https://", TLSv1_2HttpAdapter())
        response = session.get(url)

        # api 상태 확인용 디버깅 코드
        print("응답 상태 코드:", response.status_code)
        print("응답 내용 (앞 300자):", response.text[:300])
        if response.status_code != 200:
            self.stderr.write("❌외교부 API 응답 오류. JSON 파싱 중단.")
            return

        try:
            data = response.json()
            items = data["response"]["body"]["items"]["item"]
        except Exception as e:
            self.stderr.write(f"❌JSON 파싱 실패: {e}")
            return

        items = data["response"]["body"]["items"]["item"]

        # item이 dict 한 개일 경우 list로 감싸기
        if isinstance(items, dict):
            items = [items]

        count = 0

        for item in items:
            # 필수값 확인
            if not item.get("country_nm") or not item.get("country_eng_nm"):
                continue

            # 카테고리 유효성 검사
            raw_category = item.get("ctgy_nm")
            if raw_category not in ["주의", "안내"]:
                raw_category = "미지정"

            SafetyNotice.objects.update_or_create(
                notice_id=item.get("sfty_notice_id"),
                defaults={
                    "country_name": item.get("country_nm"),
                    "country_en_name": item.get("country_eng_nm"),
                    "title": item.get("title"),
                    "content": item.get("txt_origin_cn"),  # HTML 포함
                    "category": raw_category, # "안내", "주의"
                    "written_dt": item.get("wrt_dt"),
                    "file_url": item.get("file_download_url") or None,
                }
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {count}건의 지역 안전공지 데이터를 성공적으로 저장했습니다."))