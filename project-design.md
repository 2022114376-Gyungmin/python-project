# 🌳 설계 문서

## 프로젝트 제목
**대구 NDVI 대시보드 - 위성영상 기반 산불 피해지 식생 변화 분석**

## ⭐ 기능 목록

**[MUST]** Earth Engine 인증 및 초기화 작업

**[MUST]** Sentinel-2 위성영상 가져오기(지역, 날짜, 구름 비율 필터링)

**[MUST]** NDVI 계산 (B8과 B4 밴드 사용)

**[MUST]** NDVI 영상을 지도에 시각화

**[MUST]** 관심 지역의 평균 NDVI 값 추출

**[MUST]** 산불 전 / 산불 후 NDVI 비교

**[MUST]** Streamlit 인터랙티브 대시보드 만들기

**[NICE]** 사용자가 지역과 시기를 선택 가능하게 하기

**[NICE]** 여러 시기의 NDVI 시계열 그래프 그리기

**[NICE]** 분석 결과 CSV 파일로 저장

**[LATER]** NDWI, NDBI와 같은 다른 식생지수도 함께 비교

**[LATER]** 여러 산불 사례 동시 분석

**[LATER]** 회복 속도 자동 계산 기능


## 📊 데이터 설계

**1. 분석 영역 정보 (딕셔너리 활용)**
```python
study_area = {
    "name": "대구 함지산",
    "longitude": 128.6014,
    "latitude": 35.9156,
    "buffer_km": 5  # 분석 반경(km)
}
```

**2. 시각화 설정 (딕셔너리 활용)**
```python
vis_params_rgb = {
    "bands": ["B4", "B3", "B2"],
    "min": 0,
    "max": 3000
}
```
```python
vis_params_ndvi = {
    "min": 0,
    "max": 1,
    "palette": ["white", "yellow", "lightgreen", "green", "darkgreen"]
}
```

**3. 분석 시기 (딕셔너리 활용)**

값들은 예시이고 실제로 사용자가 직접 입력 예정
```python
period_before = {
    "label": "산불 전 (2025-04 초)",
    "start_date": "2025-04-01",
    "end_date": "2025-04-20"
}
```
```python
period_after = {
    "label": "산불 후 (2025-05 초)",
    "start_date": "2025-05-01",
    "end_date": "2025-05-20"
}
```

**4. NDVI 분석 결과 예시 (딕셔너리 활용)**

값들은 다 자동으로 계산되서 입력될 예정
```python
ndvi_result = {
    "period": "2025-04 초",
    "mean_ndvi": 0.65,
    "min_ndvi": 0.10,
    "max_ndvi": 0.85,
    "image_count": 3
}
```

**5. 여러 시기 결과 모음 (리스트 활용)**
```python
ndvi_results = []
```

## 🛠️ 함수 설계

```python
def get_sentinel2_image(area, start_date, end_date, cloud_threshold = 10):
    """조건에 맞는 Sentinel-2 위성영상 1장을 가져오기"""
    # 1. Sentinel-2 컬렉션 불러오기
    # 2. 좌표(area)로 필터링
    # 3. 날짜(start_date ~ end_date)로 필터링
    # 4. 구름 비율(cloud_threshold) 미만으로 필터링
    # 5. 첫 번째 영상 1장 반환
    pass


def calculate_ndvi(image):
    """위성영상에서 NDVI 계산"""
    # 1. B8(근적외선)과 B4(빨강) 밴드 사용
    # 2. NDVI = (B8 - B4) / (B8 + B4) 계산
    # 3. NDVI 영상 반환
    pass


def get_mean_ndvi(ndvi_image, area):
    """관심 지역의 평균 NDVI 값 추출"""
    # 1. 관심 영역(area) 안의 모든 픽셀 평균 계산
    # 2. 숫자 값 반환
    pass


def display_on_map(image, vis_params, layer_name):
    """지도에 영상 레이어 추가하여 시각화"""
    # 1. geemap.Map 객체 만들기
    # 2. addLayer로 영상 추가
    # 3. 지도 객체 반환
    pass


def compare_before_after(area, period_before, period_after):
    """산불 전후 NDVI 비교"""
    # 1. 산불 전 영상 가져오기 
    # 2. 산불 후 영상 가져오기 
    # 3. 각각 NDVI 계산
    # 4. 각각 평균 NDVI 추출
    # 5. 두 값 차이 계산
    # 6. 결과 딕셔너리 반환 {전: X, 후: Y, 차이: Z}
    pass
```

## 💻 화면 흐름 스케치