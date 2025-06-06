# TripGuard
멋쟁이사자처럼 13기 여기톤 대비 토이 프로젝트입니다.

<br>

## 🗂️ 데이터 초기화 (Seed)

본 프로젝트는 외교부 API로부터 여행 안전 정보 및 재외공관 데이터를 수집하지만,

- API 호출 시 네트워크/SSL 오류 발생 가능성
- API 응답 데이터의 변경 가능성
- 시연 환경에서 일관된 데이터 유지 필요

등을 고려하여 **초기 데이터를 담은 seed 파일(`countries_seed.json`)** 을 제공합니다.

### ✅ 사용 방법

#### 1. 마이그레이션 먼저 실행
**python manage.py migrate**

#### 2. seed 파일 로드
**python manage.py loaddata countries_seed.json**


> ⚠️ 반드시 migrate를 먼저 실행한 후 loaddata를 수행해주세요.

<hr>

### **📦 포함된 데이터 모델**

- Embassy: 재외공관 정보
- EmbassyHomepage: 재외공관 홈페이지
- SafetyNotice: 유의 지역 공지
- CountrySafety: 일반 안전 공지
