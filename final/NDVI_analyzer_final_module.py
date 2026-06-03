"""
================================================================
대구 함지산 NDVI 분석기 (ndvi_analyzer.py)
================================================================

프로젝트: 대구 함지산 산불 NDVI 변화 분석
작성자: 최경민 (학번: 2022114376)
소속: 경북대학교 위치정보시스템학과
작성일: 2026-05-30

[프로젝트 개요]
2025년 4월 28일 대구광역시 북구 함지산에서 발생한 산불의
식생 피해를 Sentinel-2 위성영상으로 분석한다.
산불 피해 면적은 약 260헥타르에 달하며, 본 분석은 NDVI
(정규화 식생 지수)를 활용하여 피해를 정량적으로 측정한다.

[분석 방법]
- NDVI 계산: (B8 - B4) / (B8 + B4)
  · B8: 근적외선 (식물이 강하게 반사)
  · B4: 빨강 (식물이 흡수)
- 같은 계절 비교: 작년 5월 vs 올해 5월
  · 계절 효과를 제거하고 순수 산불 영향만 측정
- 분석 영역: 함지산 산불 피해지 중심 반경 800m

[모듈 구성]
1. get_sentinel2_image()    : Sentinel-2 영상 1장 가져오기
2. calculate_ndvi()         : NDVI 계산
3. get_mean_ndvi()          : 영역 평균 NDVI 추출
4. compare_before_after()   : 산불 전후 비교 (메인 함수)

[사용 예시]
    import ee
    ee.Initialize(project='knu-project-ndvi-2026')
    
    from ndvi_analyzer import compare_before_after
    
    area = ee.Geometry.Point([128.5774, 35.9145]).buffer(800)
    period_before = {'start': '2024-05-01', 'end': '2024-05-31'}
    period_after = {'start': '2025-05-01', 'end': '2025-05-31'}
    
    result = compare_before_after(area, period_before, period_after)
    print(f"변화율: {result['percent_change']:.1f}%")
================================================================
"""

import ee


# =========================================================
# 함수 1: Sentinel-2 영상 가져오기
# =========================================================
def get_sentinel2_image(area, start_date, end_date, cloud_threshold=10):
    """
    지정된 조건의 Sentinel-2 영상 1장을 Earth Engine에서 가져온다.
    
    여러 필터를 거쳐 가장 적합한 영상 1장을 반환한다:
    - filterBounds : 지정 영역을 포함하는 영상만
    - filterDate   : 지정 기간 내 영상만
    - filter(구름) : 구름 비율이 한계 미만인 영상만
    - first()      : 첫 번째 영상 1장 선택
    
    매개변수:
        area (ee.Geometry): 분석 영역 (Point + buffer 형태)
        start_date (str): 시작 날짜, 'YYYY-MM-DD' 형식
        end_date (str): 끝 날짜, 'YYYY-MM-DD' 형식
        cloud_threshold (int): 구름 비율 한계 (%), 기본값 10
    
    반환값:
        ee.Image: 조건에 맞는 Sentinel-2 영상 1장
    """
    # Sentinel-2 컬렉션 불러오기 (대기 보정 영상)
    image = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
             # 분석 영역을 포함하는 영상만 필터링
             .filterBounds(area)
             # 지정 기간 내 영상만 필터링
             .filterDate(start_date, end_date)
             # 구름 비율이 한계 미만인 영상만 필터링
             .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloud_threshold))
             # 첫 번째 영상 1장 선택
             .first())
    
    return image


# =========================================================
# 함수 2: NDVI 계산
# =========================================================
def calculate_ndvi(image):
    """
    위성영상에서 NDVI (정규화 식생 지수)를 계산한다.
    
    NDVI 공식: (B8 - B4) / (B8 + B4)
    - B8: 근적외선 (NIR) - 식물이 강하게 반사
    - B4: 빨강 (Red)    - 식물이 흡수
    
    NDVI 값의 의미:
    - 0.7 ~ 0.9: 풍부한 식생 (숲)
    - 0.3 ~ 0.7: 보통 식생 (잔디, 농경지)
    - 0.0 ~ 0.3: 식생 적음 (도시, 맨땅)
    - 음수      : 물, 구름
    
    매개변수:
        image (ee.Image): Sentinel-2 영상
    
    반환값:
        ee.Image: NDVI 영상 (-1 ~ 1 범위, 밴드명 'NDVI')
    """
    # normalizedDifference가 (B8 - B4) / (B8 + B4) 공식을 자동 계산
    # rename으로 결과 밴드 이름을 'NDVI'로 지정 (가독성 향상)
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    
    return ndvi


# =========================================================
# 함수 3: 평균 NDVI 추출
# =========================================================
def get_mean_ndvi(ndvi_image, area):
    """
    NDVI 영상에서 분석 영역의 평균값을 숫자로 추출한다.
    
    reduceRegion으로 영역 내 모든 픽셀을 평균값 1개로 축소.
    영상 픽셀이 수만 개라 비교가 어려우므로,
    이 함수로 단일 숫자로 만들어야 비교/그래프/통계가 가능.
    
    매개변수:
        ndvi_image (ee.Image): calculate_ndvi()로 만든 NDVI 영상
        area (ee.Geometry): 분석 영역
    
    반환값:
        float: 평균 NDVI 값 (예: 0.693)
    """
    # 영역 내 모든 픽셀의 평균값 계산
    mean_dict = ndvi_image.reduceRegion(
        reducer=ee.Reducer.mean(),   # 평균 계산 reducer
        geometry=area,                # 분석 영역
        scale=10,                     # 픽셀 크기 (Sentinel-2 = 10m)
        maxPixels=1e9                 # 최대 픽셀 수 (안전장치, 10억)
    )
    
    # 딕셔너리에서 NDVI 키의 값 꺼내기 + Google 서버에서 실제 숫자 가져오기
    mean_value = mean_dict.get('NDVI').getInfo()
    
    return mean_value


# =========================================================
# 함수 4: 산불 전후 비교 (메인 분석 함수)
# =========================================================
def compare_before_after(area, period_before, period_after, cloud_threshold=10):
    """
    산불 전후 두 시기의 NDVI를 비교 분석한다.
    
    함수 1, 2, 3을 순서대로 호출하여 산불 전후를 자동 비교.
    영상 정보, NDVI 값, 변화율 등 모든 결과를 딕셔너리로 반환.
    
    [동작 순서]
    1. 산불 전 영상 가져오기 → NDVI 계산 → 평균 추출 → 날짜 기록
    2. 산불 후 영상 가져오기 → NDVI 계산 → 평균 추출 → 날짜 기록
    3. 차이 계산 (산불 후 - 산불 전)
    4. 변화율 계산 ((차이 / 산불 전) × 100)
    5. 모든 결과를 딕셔너리로 묶어 반환
    
    매개변수:
        area (ee.Geometry): 분석 영역
        period_before (dict): 산불 전 시기
                              {'start': 'YYYY-MM-DD', 'end': 'YYYY-MM-DD'}
        period_after (dict): 산불 후 시기
                             {'start': 'YYYY-MM-DD', 'end': 'YYYY-MM-DD'}
        cloud_threshold (int): 구름 비율 한계 (%), 기본값 10
    
    반환값:
        dict: 비교 결과 (8개 항목)
        {
            'mean_before' (float):       산불 전 평균 NDVI
            'mean_after' (float):        산불 후 평균 NDVI
            'date_before' (str):         산불 전 영상 촬영일
            'date_after' (str):          산불 후 영상 촬영일
            'diff' (float):              차이 (산불 후 - 산불 전)
            'percent_change' (float):    변화율 (%)
            'ndvi_before_image' (ee.Image): 산불 전 NDVI 영상 (시각화용)
            'ndvi_after_image' (ee.Image):  산불 후 NDVI 영상 (시각화용)
        }
    """
    
    # ---------- 산불 전 처리 ----------
    # 영상 1장 가져오기
    img_before = get_sentinel2_image(
        area,
        period_before['start'],
        period_before['end'],
        cloud_threshold
    )
    # NDVI 계산
    ndvi_before = calculate_ndvi(img_before)
    # 평균 NDVI 추출
    mean_before = get_mean_ndvi(ndvi_before, area)
    # 영상 촬영 날짜 추출 (검증용)
    date_before = ee.Date(
        img_before.get('system:time_start')
    ).format('YYYY-MM-dd').getInfo()
    
    # ---------- 산불 후 처리 ----------
    # 영상 1장 가져오기
    img_after = get_sentinel2_image(
        area,
        period_after['start'],
        period_after['end'],
        cloud_threshold
    )
    # NDVI 계산
    ndvi_after = calculate_ndvi(img_after)
    # 평균 NDVI 추출
    mean_after = get_mean_ndvi(ndvi_after, area)
    # 영상 촬영 날짜 추출 (검증용)
    date_after = ee.Date(
        img_after.get('system:time_start')
    ).format('YYYY-MM-dd').getInfo()
    
    # ---------- 변화량 계산 ----------
    # 차이: 산불 후 - 산불 전 (음수면 감소)
    diff = mean_after - mean_before
    # 변화율 (%): (차이 / 산불 전) × 100
    percent_change = (diff / mean_before) * 100
    
    # ---------- 결과를 딕셔너리로 묶어 반환 ----------
    return {
        'mean_before': mean_before,
        'mean_after': mean_after,
        'date_before': date_before,
        'date_after': date_after,
        'diff': diff,
        'percent_change': percent_change,
        'ndvi_before_image': ndvi_before,
        'ndvi_after_image': ndvi_after
    }
