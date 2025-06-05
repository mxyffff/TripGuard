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

# SSL 오류 방지용 커스텀 어댑터
class TLSv1_2HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT@SECLEVEL=1")  # 낮은 보안 수준 허용
        context.options |= ssl.OP_NO_TLSv1_3  # TLS 1.3 비활성화
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

# BaseCommand 상속
class Command(BaseCommand):
    help = '외교부 API(getCountrySafetyList)를 통해 유의 지역 공지 데이터를 가져온다.'

    def handle(self, *args, **kwargs):
        service_key = 't6G5D0EXlmcbAUoDA9t04kUw9N83jcIrQ3qcANfLy0aTuOnhhy%2BF7uGeFQD8s1lKym8BYzsGy0G6ToGC6zNk2A%3D%3D'
        url = (
            f'https://apis.data.go.kr/1262000/CountrySafetyService6/getCountrySafetyList6?serviceKey={service_key}&numOfRows=100&pageNo=1'
        )

        self.stdout.write(self.style.NOTICE("유의 지역 정보 API 요청 중..."))

        # 세션 설정 및 TLS 우회 어댑터 등록
        session = requests.Session()
        session.mount("https://", TLSv1_2HttpAdapter())

        try:
            response = session.get(url)  # API 요청 실행
            self.stdout.write(f"응답 상태 코드: {response.status_code}")  # 응답 상태 코드 출력

            # 200이 아닐 경우 에러 처리
            if response.status_code != 200:
                self.stderr.write("❌ API 요청 실패 (status != 200)")
                return

            data = response.json() # JSON 응답 파싱
            items = data["response"]["body"]["items"]["item"] # 안전 공지 데이터 추출

        except Exception as e:
            # 요청 실패 또는 JSON 파싱 중 에러 처리
            self.stderr.write(f"❌ 요청 또는 JSON 파싱 실패: {e}")
            return

        # 단일 객체로 응답된 경우 리스트로 반환
        if isinstance(items, dict):
            items = [items]

        # DB 저장 건수 초기화
        count = 0

        # 각 재외공관 item에 대해 DB 저장 반복
        for item in items:
            # 필수값 확인
            if not item.get("country_nm") or not item.get("country_eng_nm"):
                continue

            # 카테고리 유효성 검사
            raw_category = item.get("ctgy_nm")
            if raw_category not in ["주의", "안내"]:
                raw_category = "미지정"

            # DB에 저장 (있으면 업데이트, 없으면 생성)
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