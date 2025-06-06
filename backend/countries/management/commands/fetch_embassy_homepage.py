import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from django.core.management.base import BaseCommand
from countries.models import Embassy, EmbassyHomepage

# 재외공관 홈페이지 api

# SSL 오류 방지용 커스텀 어댑터
class TLSv1_2HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT@SECLEVEL=1") # 낮은 보안 수준 허용
        context.options |= ssl.OP_NO_TLSv1_3 # TLS 1.3 비활성화
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

class Command(BaseCommand):
    help = '외교부 API(getEmbassyHomepageList2)를 통해 대사관 홈페이지 정보를 가져온다.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("재외공관 홈페이지 API 요청 중..."))

        # API 호출용 인증키 및 URL 설정
        service_key = "t6G5D0EXlmcbAUoDA9t04kUw9N83jcIrQ3qcANfLy0aTuOnhhy%2BF7uGeFQD8s1lKym8BYzsGy0G6ToGC6zNk2A%3D%3D"
        url = (
            f"https://apis.data.go.kr/1262000/EmbassyHomepageService2/getEmbassyHomepageList2"
            f"?serviceKey={service_key}&pageNo=1&numOfRows=100&type=JSON"
        )

        # 세션 설정 및 TLS 우회 어댑터 등록
        session = requests.Session()
        session.mount("https://", TLSv1_2HttpAdapter())

        try:
            response = session.get(url)
            self.stdout.write(f"응답 상태 코드: {response.status_code}")

            if response.status_code != 200:
                self.stderr.write("❌ API 요청 실패 (status != 200)")
                return

            data = response.json()
            items = data["response"]["body"]["items"]["item"]

        except Exception as e:
            self.stderr.write(f"❌ 요청 또는 JSON 파싱 실패: {e}")
            return

        if isinstance(items, dict):
            items = [items]

        count = 0

        # 각 항목 저장
        for item in items:
            embassy_cd = item.get("embassy_cd")
            homepage_url = item.get("homepage_url")

            if not embassy_cd or not homepage_url:
                continue

            # 연결된 Embassy가 존재하는 경우만 저장
            try:
                embassy = Embassy.objects.get(embassy_cd=embassy_cd)
                EmbassyHomepage.objects.update_or_create(
                    embassy=embassy,
                    defaults={
                        "url": homepage_url,
                    }
                )
                count += 1
            except Embassy.DoesNotExist:
                continue  # 일치하는 공관이 없으면 스킵

        self.stdout.write(self.style.SUCCESS(f"✅ {count}건의 대사관 홈페이지 정보를 저장했습니다."))

