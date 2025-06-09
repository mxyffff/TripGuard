from http.client import responses
from itertools import count

import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from django.core.management.base import BaseCommand
from countries.models import Embassy


# 재외공관 정보 api 모델 - [재외공관 목록]

# SSL 오류 방지용 커스텀 어댑터
class TLSv1_2HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT@SECLEVEL=1")  # 낮은 보안 수준 허용
        context.options |= ssl.OP_NO_TLSv1_3  # TLS 1.3 비활성화
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)


class Command(BaseCommand):
    help = '외교부 API(getEmbassyList)로부터 대사관 정보를 가져온다.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("재외공관 정보 API 요청 중..."))

        service_key = "t6G5D0EXlmcbAUoDA9t04kUw9N83jcIrQ3qcANfLy0aTuOnhhy%2BF7uGeFQD8s1lKym8BYzsGy0G6ToGC6zNk2A%3D%3D"
        url = (
            f"https://apis.data.go.kr/1262000/EmbassyService2/getEmbassyList2"
            f"?serviceKey={service_key}&pageNo=1&numOfRows=100&type=JSON"
        )

        # 세션 설정 및 TLS 우회 어댑터 등록
        session = requests.Session()
        session.mount("https://", TLSv1_2HttpAdapter())

        try:
            # API 요청 실행
            response = session.get(url)
            self.stdout.write(f"응답 상태 코드: {response.status_code}")  # 응답 상태 코드 출력

            # 200이 아닐 경우 에러 처리
            if response.status_code != 200:
                self.stderr.write("❌ API 요청 실패 (status != 200)")
                return

            data = response.json()  # JSON 응답 파싱
            items = data["response"]["body"]["items"]["item"]  # 재외공관 데이터 항목 추출

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
            embassy_cd = item.get("embassy_cd")  # 재외공관 코드
            if not embassy_cd:
                continue  # 필수값이 없으면 건너뜀

            # DB에 저장
            try:
                # 기존 항목을 가져옴
                embassy = Embassy.objects.get(embassy_cd=embassy_cd)
                # country_name, country_en_name, slug는 보존하고 나머지만 업데이트
                embassy.embassy_name = item.get("embassy_kor_nm")
                embassy.address = item.get("emblgbd_addr")
                embassy.tel_no = item.get("tel_no")
                embassy.urgency_tel = item.get("urgency_tel_no")
                embassy.lat = item.get("embassy_lat")
                embassy.lng = item.get("embassy_lng")
                embassy.save()
            except Embassy.DoesNotExist:
                # 없는 경우는 모든 필드를 새로 생성
                Embassy.objects.create(
                    embassy_cd=embassy_cd,
                    country_name=item.get("country_nm"),
                    country_en_name=item.get("country_eng_nm"),
                    embassy_name=item.get("embassy_kor_nm"),
                    address=item.get("emblgbd_addr"),
                    tel_no=item.get("tel_no"),
                    urgency_tel=item.get("urgency_tel_no"),
                    lat=item.get("embassy_lat"),
                    lng=item.get("embassy_lng"),
                )

            count += 1  # 저장된 항목 수 증가

        # 최종 처리 결과 출력
        self.stdout.write(self.style.SUCCESS(f"✅ {count}건의 대사관 데이터를 성공적으로 저장했습니다."))
