from django.test import TestCase

# Create your tests here
from .models import TravelAlert
from datetime import datetime

class TravelAlertModelTest(TestCase):
    def setUp(self):
        TravelAlert.objects.create(
            alarm_level=1,
            continent_code="10",
            continent_name="아주",
            continent_name_eng="Asia",
            country_name="중국",
            country_name_eng="China",
            country_code="CN",
            region_type="일부",
            remark="특별여행주의보 지정 지역을 제외한 지역",
            written_date=datetime.strptime("2025-05-21", "%Y-%m-%d").date(),
            flag_url="https://opendata.mofa.go.kr:8444/fileDownload/images/country_images/flags/182/20241007_182058339.jpeg",
            map_url="https://opendata.mofa.go.kr:8444/fileDownload/images/country_images/maps/182/20220329_151915875.gif",
            danger_map_url="https://www.0404.go.kr/imgsrc.mofa?atch_file_id=COUNTRY_189&file_sn=3"
        )

    def test_china_country_name(self):
        alert = TravelAlert.objects.get(country_code="CN")
        self.assertEqual(alert.country_name, "중국")

    def test_alarm_level_value(self):
        alert = TravelAlert.objects.get(country_code="CN")
        self.assertEqual(alert.alarm_level, 1)

    def test_written_date(self):
        alert = TravelAlert.objects.get(country_code="CN")
        self.assertEqual(alert.written_date.strftime("%Y-%m-%d"), "2025-05-21")

    def test_flag_url_valid(self):
        alert = TravelAlert.objects.get(country_code="CN")
        self.assertTrue(alert.flag_url.startswith("https://"))
