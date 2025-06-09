import requests
from django.core.management.base import BaseCommand
from alerts.models import Alert
from datetime import datetime

class Command(BaseCommand):
    help = "외교부 여행경보 API에서 데이터를 받아와 DB에 저장합니다."

    def handle(self, *args, **options):
        print("외교부 여행경보 API 요청 중...")

        service_key = "jT%2BQ4DOdKXTFolmGz1Dc5zu0wiHpEBMiXar01c9qfg8AnazFkPC0k8cklvYJETq28XP0Za6hsipzL3lhtAFOxA%3D%3D"
        url = (
            "http://apis.data.go.kr/1262000/TravelAlarmService2/getTravelAlarmList2"
            f"?serviceKey={service_key}&pageNo=1&numOfRows=200&returnType=JSON"
        )

        response = requests.get(url)
        print("응답 상태 코드:", response.status_code)

        if response.status_code != 200:
            print("❌ API 요청 실패 (status != 200)")
            return

        try:
            data = response.json()
        except Exception as e:
            print(f"❌ 요청 또는 JSON 파싱 실패: {e}")
            return

        items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])

        if not items:
            print("⚠️ 받아온 데이터가 없습니다.")
            return

        for item in items:
            try:
                alert, created = Alert.objects.update_or_create(
                    country_code=item.get("country_iso_alp2", ""),
                    defaults={
                        "country_name": item.get("country_nm", ""),
                        "alarm_level": item.get("alarm_lvl", 0),
                        "continent_name": item.get("continent_nm", ""),
                        "written_dt": datetime.strptime(item.get("written_dt", "1900-01-01"), "%Y-%m-%d").date(),
                        "region_type": item.get("region_ty", ""),
                        "remark": item.get("remark", ""),
                        "map_url": item.get("map_download_url", ""),
                        "flag_url": item.get("flag_download_url", ""),
                    }
                )
                if created:
                    print(f"새로운 알림 저장: {alert}")
                else:
                    print(f"기존 알림 업데이트: {alert}")
            except Exception as e:
                print(f"⚠️ DB 저장 오류: {e}")

        print("완료!")

