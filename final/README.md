# 🌳 대구 함지산 산불 NDVI 분석 대시보드

> **Sentinel-2 위성영상으로 산불 피해를 정량화하는 인터랙티브 Streamlit 대시보드**

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.51-red) ![Earth Engine](https://img.shields.io/badge/Earth_Engine-API-green) ![License](https://img.shields.io/badge/License-Academic-orange)

---

### 👤 작성자 정보

- **이름**: 최경민
- **학번**: 2022114376
- **소속**: 경북대학교 위치정보시스템학과
- **과목**: 2026-1학기 컴퓨팅사고와 SW 코딩

## 📌 프로젝트 소개

**2025년 4월 28일** 대구광역시 북구 함지산에서 발생한 산불(약 **260헥타르** 피해)의 식생 영향을 **Sentinel-2 위성영상**과 **NDVI(정규화 식생 지수)** 분석으로 정량화하는 인터랙티브 대시보드입니다.

뉴스에서는 "몇 헥타르 탔다"는 정보만 제공할 뿐, 실제 식생 피해가 얼마나 심각했는지 객관적으로 확인할 도구가 부족합니다. 이 대시보드는 코드 작성 없이 누구나 클릭 한 번으로 위성영상 기반 산불 피해 분석 결과를 확인할 수 있도록 설계되었습니다.

### 📊 핵심 분석 결과

| 항목 | 값 |
|------|-----|
| **산불 전 평균 NDVI** | 0.693 (2024-05-03) |
| **산불 후 평균 NDVI** | 0.484 (2025-05-08) |
| **변화율** | **-30.2%** (식생 약 30% 감소) |
| **분석 영역** | 함지산 중심 [128.5774, 35.9145] 반경 800m |

---

## ⭐ 핵심 기능

### 1️⃣ 위성영상 자동 수집 및 NDVI 계산
- Sentinel-2 영상에서 지정 시기·지역의 구름 적은 영상을 자동으로 가져와 식생지수(NDVI) 계산

### 2️⃣ 산불 전후 비교 시각화
- 산불 발생 전과 후 시점의 NDVI를 지도로 토글하며 직관적으로 비교

### 3️⃣ 인터랙티브 웹 대시보드
- 클릭 한 번으로 분석 실행, 결과(메트릭/지도/해석)를 한 화면에서 확인

---

## 🚀 빠른 시작 (Quick Start)

```bash
# 1. 저장소 클론
git clone https://github.com/2022114376-Gyungmin/python-project.git
cd python-project

# 2. 가상환경 생성 및 활성화
conda create -n gee python=3.11
conda activate gee

# 3. 라이브러리 설치
pip install streamlit earthengine-api geemap

# 4. Earth Engine 인증
earthengine authenticate

# 5. final 폴더로 이동 후 대시보드 실행
cd final
streamlit run app_final.py
```

→ 브라우저가 자동으로 열리고 `http://localhost:8501`에서 대시보드가 표시됩니다!

---

## 📋 사전 준비

### 1. Python 환경

- **Python 3.10 이상** 필요
- **Anaconda 권장** (가상환경 관리 용이)

Anaconda 설치: https://www.anaconda.com/download

### 2. Google Earth Engine 계정 ⭐

본 프로젝트는 Google Earth Engine API를 사용합니다. 계정 생성 절차:

1. [Earth Engine 가입 페이지](https://earthengine.google.com) 접속
2. **"Sign Up"** 클릭
3. Google 계정으로 로그인
4. 학생/연구자 정보 입력 (무료 사용)
5. **승인까지 1~2일 소요** → [Step 4-1에서 확인 방법 안내](#step-4-1-earth-engine-승인-상태-확인-)

### 3. Google Cloud 프로젝트

Earth Engine 사용을 위해 Google Cloud 프로젝트가 필요합니다:

1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 새 프로젝트 생성 (예: `my-ndvi-project`)
3. Earth Engine API 활성화
4. 프로젝트 ID 메모 → 이후 `app_final.py`에 입력

---

## 🛠️ 상세 설치 가이드

### Step 1: 저장소 클론

```bash
git clone https://github.com/2022114376-Gyungmin/python-project.git
cd python-project
```

### Step 2: Anaconda 가상환경 구축

```bash
# 가상환경 생성 (Python 3.11)
conda create -n gee python=3.11

# 가상환경 활성화
conda activate gee
```

> 💡 가상환경을 사용하는 이유: 라이브러리 충돌 방지 + 재현 가능한 환경 구축

### Step 3: 필수 라이브러리 설치

```bash
pip install streamlit earthengine-api geemap
```

**설치되는 라이브러리:**

| 라이브러리 | 용도 |
|----------|------|
| `streamlit` | 웹 대시보드 프레임워크 |
| `earthengine-api` | Google Earth Engine Python API |
| `geemap` | Earth Engine 지도 시각화 (foliumap 포함) |

### Step 4: Earth Engine 인증

```bash
earthengine authenticate
```

> 💡 브라우저가 열리며 Google 계정 로그인 → 인증 코드를 복사해서 터미널에 붙여넣기

만약 인증 에러가 발생하면 Python에서 다음과 같이 시도:
```python
import ee
ee.Authenticate(auth_mode='localhost')
```

### Step 4-1: Earth Engine 승인 상태 확인 ⭐

가입 후 승인까지 보통 **1~2일** 소요됩니다. 다음 3가지 방법으로 승인 완료 여부를 확인할 수 있습니다.

#### 방법 1: Code Editor 접속 (가장 빠름)

[code.earthengine.google.com](https://code.earthengine.google.com) 접속:

| 결과 | 의미 |
|------|------|
| ✅ Code Editor 화면이 정상적으로 열림 | **승인 완료** |
| ❌ "You don't have access" 메시지 | 승인 대기 또는 미승인 |
| ❌ 등록 페이지로 리다이렉트 | 가입 미완료 |

#### 방법 2: Python 코드로 확인 (실용적) ⭐

가상환경(`gee`)에서 다음 코드 실행:

```python
import ee

try:
    # 본인 프로젝트 ID로 변경
    ee.Initialize(project='your-project-id')
    
    # 간단한 테스트
    collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    first_image = collection.first()
    
    print("✅ Earth Engine 승인 완료!")
    print(f"테스트 영상 ID: {first_image.id().getInfo()}")
    
except Exception as e:
    print(f"❌ 에러: {e}")
```

**결과 해석**:

| 출력 | 상태 |
|------|------|
| `✅ Earth Engine 승인 완료!` + 영상 ID | 정상 작동 |
| `Earth Engine API has not been used in project...` | API 비활성화 → 방법 3 진행 |
| `Caller does not have required permission...` | 프로젝트 ID 오류 |
| `not enrolled in Earth Engine...` | 승인 대기 중 또는 미가입 |

#### 방법 3: Google Cloud Console에서 확인

1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 본인 프로젝트 선택
3. 좌측 메뉴: **"API 및 서비스"** → **"사용 설정된 API"**
4. **"Earth Engine API"** 검색
5. **"사용 설정됨"** 표시 확인

> 💡 API가 비활성화되어 있으면 **"사용 설정"** 버튼 클릭

#### ⏳ 승인 대기 중일 때

- 가입 시 사용한 Gmail로 **승인 알림 이메일** 도착 확인
- 학생/연구자는 보통 **1~2일 내** 빠르게 승인됨
- 승인 거부 시: 학생/연구자 정보를 더 자세히 입력하고 재신청

---

### Step 5: 프로젝트 ID 설정

`final/app_final.py` 파일을 열고 **Earth Engine 초기화 부분**의 프로젝트 ID를 본인 것으로 수정:

```python
# 변경 전
ee.Initialize(project='knu-project-ndvi-2026')

# 변경 후 (본인 프로젝트 ID로)
ee.Initialize(project='your-project-id')
```

### Step 6: 대시보드 실행

```bash
cd final
streamlit run app_final.py
```

→ 자동으로 브라우저가 열리고 `http://localhost:8501`에서 대시보드 확인 가능

---

## 📁 파일 구조

```
python-project/
├── README.md                                  # 본 문서
│
├── final/                                     # ⭐ 최종 결과물 (실행 폴더)
│   ├── NDVI_analyzer_final_module.py         # 분석 함수 모듈 (함수 4개)
│   └── app_final.py                           # Streamlit 대시보드 (메인 실행 파일)
│
├── create-function/                           # 함수 1, 2 개발 과정
├── mean-ndvi/                                 # 함수 3 개발 과정
├── compare-analysis/                          # 함수 4 개발 과정
│
└── docs/                                      # 프로젝트 문서
    ├── 진행보고서.md                          # 프로젝트 진행 보고서
    ├── 화면흐름설계.md                        # UI/UX 설계 문서
    └── images/
        └── 화면흐름도.svg                     # 화면 흐름도 이미지
```

---

## 🔧 코드 구조

### 핵심 파일 2개

| 파일 | 역할 | 줄 수 |
|------|------|------|
| `NDVI_analyzer_final_module.py` | 분석 함수 모듈 (재사용 가능) | 약 236줄 |
| `app_final.py` | Streamlit 대시보드 (사용자 인터페이스) | 약 251줄 |

> 💡 **모듈화 설계**: 분석 로직(`NDVI_analyzer_final_module.py`)과 UI(`app_final.py`)를 분리해 재사용성과 가독성 향상

### 함수 4개 구조

```
함수 1: get_sentinel2_image()
   ├─ 역할: Sentinel-2 위성영상 1장 가져오기
   └─ 핵심 메서드: filterBounds, filterDate, filter, first

함수 2: calculate_ndvi()
   ├─ 역할: NDVI 계산
   └─ 공식: (NIR - RED) / (NIR + RED)

함수 3: get_mean_ndvi()
   ├─ 역할: 영역 평균 NDVI 추출
   └─ 핵심 메서드: reduceRegion, getInfo

함수 4: compare_before_after() [메인 함수]
   ├─ 역할: 산불 전후 NDVI 비교
   └─ 함수 1, 2, 3을 순차 호출하는 '지휘자'
```

---

## 📊 사용 데이터

### 🛰️ 위성영상

- **위성**: Sentinel-2 (ESA, 유럽우주국)
- **해상도**: 10m (B4, B8 밴드)
- **재방문 주기**: 5일
- **카탈로그 ID**: `COPERNICUS/S2_SR_HARMONIZED`
- **이용 조건**: 무료 (공공 데이터)

### 📍 분석 영역

- **위치**: 함지산 산불 피해지 중심
- **좌표**: [128.5774, 35.9145]
- **반경**: 800m

### 📅 분석 시기

- **산불 전**: 2024년 5월 (작년 같은 계절)
- **산불 후**: 2025년 5월 (산불 직후)
- **이유**: 계절 효과를 제거한 정확한 비교

---

## 📖 NDVI 상세 설명

### 🌿 NDVI (Normalized Difference Vegetation Index, 정규화 식생 지수)

위성영상에서 식물이 얼마나 건강하게 자라고 있는지를 수치로 나타내는 지표입니다.

식물의 잎은 가시광선의 **빨간색(Red)은 흡수**하고 **근적외선(NIR)은 강하게 반사**하는 특성이 있는데, 이 두 파장의 차이를 이용해 계산합니다.

#### 🧮 계산식

```
                NIR - RED
   NDVI  =  ─────────────────
                NIR + RED
```

- **NIR (B8)**: 근적외선 (건강한 식물이 강하게 반사)
- **RED (B4)**: 빨강 (식물의 엽록소가 흡수)

#### 📊 값의 범위 (-1 ~ +1)

| NDVI 값 | 의미 |
|---------|------|
| `0.6 ~ 0.9` | 🌲 건강한 식생 (울창한 숲) |
| `0.2 ~ 0.5` | 🌱 잔디, 농작물 |
| `0 근처` | 🏙️ 맨땅, 도시 |
| `음수` | 💧 물, 눈, 구름 |

🔥 **산불이 발생하면** 식생이 손상되어 NDVI 값이 급격히 낮아집니다. 따라서 산불 전후의 NDVI를 비교하면 피해 정도를 객관적으로 확인할 수 있습니다.

### 같은 계절 비교의 중요성 ⭐

본 프로젝트의 핵심 트러블슈팅 결과:

- **❌ 잘못된 비교**: 4월 (이른 봄, 잎 없음) vs 5월 → 계절 효과로 결과 왜곡
- **✅ 올바른 비교**: 작년 5월 vs 올해 5월 → 계절 효과 제거, 산불 영향만 측정

---

## 🚨 트러블슈팅 가이드

### 0. Earth Engine 승인 미완료 ⭐

#### 🔴 문제
```
ee.ee_exception.EEException: Earth Engine API has not been used in project ...
ee.ee_exception.EEException: ... is not enrolled in Earth Engine
```

#### ✅ 해결
가입 후 1~2일 승인 대기가 필요합니다. 다음 코드로 승인 상태 확인:

```python
import ee
try:
    ee.Initialize(project='your-project-id')
    test = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').first()
    print(f"✅ 승인 완료! 영상 ID: {test.id().getInfo()}")
except Exception as e:
    print(f"❌ 미승인 또는 에러: {e}")
```

자세한 확인 방법은 [Step 4-1: Earth Engine 승인 상태 확인](#step-4-1-earth-engine-승인-상태-확인-) 섹션 참조.

---

### 1. Earth Engine 인증 에러

#### 🔴 문제
```
ee.Authenticate() OAuth compatibility error
```

#### ✅ 해결
```python
import ee
ee.Authenticate(auth_mode='localhost')
```

또는 터미널에서:
```bash
earthengine authenticate --auth_mode=notebook
```

---

### 2. 모듈을 찾을 수 없음

#### 🔴 문제
```
ModuleNotFoundError: No module named 'NDVI_analyzer_final_module'
```

#### ✅ 해결
- `app_final.py`와 `NDVI_analyzer_final_module.py`가 **같은 폴더**(`final/`)에 있는지 확인
- `final` 폴더 안에서 `streamlit run app_final.py` 실행
- 다른 폴더에서 실행 시 모듈 import 실패

---

### 3. 영상을 찾을 수 없음

#### 🔴 문제
```
TypeError: 'NoneType' object has no attribute ...
```

#### ✅ 해결
- 구름이 많은 시기일 가능성 → 다른 시기로 변경
- `cloud_threshold=10`을 `cloud_threshold=20`으로 늘려보기
- 분석 영역이 너무 작을 가능성 → `buffer(800)`을 `buffer(1500)` 등으로 조정

---

### 4. 프로젝트 ID 오류

#### 🔴 문제
```
ee.Initialize: Project not found
```

#### ✅ 해결
- `app_final.py`의 `ee.Initialize(project='...')`에 **본인 프로젝트 ID** 입력
- Google Cloud Console에서 프로젝트 ID 확인
- Earth Engine API가 활성화되어 있는지 확인

---

### 5. NDVI 결과가 예상과 다름 ⭐

#### 🔴 문제
- 산불 후 NDVI가 더 높게 나옴 (상식과 정반대)

#### ✅ 해결 (본 프로젝트의 핵심 교훈)
- **분석 영역 확인**: 산불 피해지보다 너무 크면 정상 식생이 평균을 흐림 → 적절한 반경으로 조정
- **계절 일치 확인** ⭐: 같은 계절끼리 비교해야 함 (예: 작년 5월 vs 올해 5월)
- **영상 날짜 확인**: 이른 봄 영상은 낙엽수에 잎이 없어 NDVI가 원래 낮음

> 💡 자세한 내용은 [`docs/진행보고서.md`](docs/진행보고서.md)의 "3.2 NDVI 결과 이상치" 섹션 참조

---

### 6. 라이브러리 설치 오류

#### 🔴 문제
```
ERROR: Could not install packages due to an OSError
```

#### ✅ 해결
```bash
# 가상환경 재생성
conda deactivate
conda remove -n gee --all
conda create -n gee python=3.11
conda activate gee

# pip 업그레이드 후 재설치
pip install --upgrade pip
pip install streamlit earthengine-api geemap
```

---

## 👥 예상 사용자

| 대상 | 활용 시나리오 |
|------|------------|
| 🙋 본인 | 위성영상 분석 학습 및 포트폴리오 |
| 🎓 관련 학과 재학생 | 식생/원격탐사 데이터 학습 자료 |
| 🔍 비전문가 | 산불 피해 현황을 직관적으로 확인 |
| 🌍 환경 연구자 | 산림 변화 추세 모니터링 도구 |

---

## 🌟 기대효과

✅ 원격탐사·식생지수(NDVI) 이론을 책으로 배우는 데 그치지 않고, Python을 적용해 실제 데이터로 구현해보는 경험

✅ Sentinel-2 데이터의 진입장벽을 완화시켜 누구나 접근 가능한 분석 도구 제공

✅ 산불 피해에 대해 뉴스로만 접할 수 있었던 사실을 NDVI라는 정량적 지표로 보완

✅ 분석 결과의 신뢰성을 보장하는 검증된 분석 방법론 (같은 계절 비교) 제공

✅ 향후 홍수·도시 개발·농경지 변화 등으로 분석 대상 확대 가능

---

## 🚀 향후 확장 계획

### 원래 비전 완성
- 사용자가 지역 + 시기를 자유롭게 선택할 수 있는 **범용 대시보드**
- 지도 클릭으로 좌표 입력 기능
- 날짜 선택 위젯 + 권장 시기 자동 추천
- 입력 검증 로직 (계절 일치 등)

### 다른 자연재해로 확장
- 산사태 피해 분석
- 홍수 영향 분석
- 가뭄 모니터링

### 응용 활용
- 위성영상 자동 분류 모델 연동
- NDWI(물), NDBI(건물) 등 다양한 정규화 지수 지원
- AI를 활용한 GIS 도구 설계

---

## 🛠️ 기술 스택

### 개발 환경
- **언어**: Python 3.11
- **가상환경**: Anaconda (`gee` 환경)
- **운영 체제**: Windows

### 주요 라이브러리
- `streamlit` - 웹 대시보드 프레임워크
- `earthengine-api` - Google Earth Engine API
- `geemap` (foliumap) - Earth Engine 지도 시각화

### 외부 서비스
- **Google Earth Engine** - 페타바이트급 위성영상 처리
- **Sentinel-2** - ESA 운영 위성영상 (10m 해상도)
- **Google Cloud Platform** - 프로젝트 인증

---

## 📚 추가 문서

상세 정보는 `docs/` 폴더 참조:

- 📋 [진행 보고서](docs/진행보고서.md) - 프로젝트 진행 과정 및 트러블슈팅 상세
- 🖥️ [화면 흐름 설계](docs/화면흐름설계.md) - UI/UX 설계 문서

---

## 🔗 참고 자료

- [Sentinel-2 위성 정보](https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2)
- [Google Earth Engine 공식 문서](https://developers.google.com/earth-engine)
- [Streamlit 공식 문서](https://docs.streamlit.io)
- [geemap 공식 문서](https://geemap.org)
- [NDVI 위키백과](https://ko.wikipedia.org/wiki/%EC%A0%95%EA%B7%9C%ED%99%94_%EC%8B%9D%EC%83%9D_%EC%A7%80%EC%88%98)

---

> 💡 본 프로젝트는 컴퓨팅사고와 SW코딩 과제 최종 결과물입니다.  
> AI(Claude)를 협업 도구로 활용했으며, **모든 결과는 직접 검증**했습니다.  
> "내가 먼저 원인을 파악해보고 AI를 활용하자"는 원칙으로 작업했습니다.
