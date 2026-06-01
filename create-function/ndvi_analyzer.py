"""
대구 함지산 NDVI 분석기
경북대학교 위치정보시스템학과 프로젝트

2025년 4월 28일 발생한 대구 함지산 산불의 식생 피해를
Sentinel-2 위성영상의 NDVI로 분석하는 모듈.

분석 방법: 같은 계절 비교 (작년 5월 vs 올해 5월)
"""

import ee


def get_sentinel2_image(area, start_date, end_date, cloud_threshold=10):
    """주어진 조건의 Sentinel-2 영상 1장 가져오기"""
    return (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
            .filterBounds(area)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloud_threshold))
            .first())


def calculate_ndvi(image):
    """위성영상에서 NDVI 계산: (B8 - B4) / (B8 + B4)"""
    return image.normalizedDifference(['B8', 'B4']).rename('NDVI')


def get_mean_ndvi(ndvi_image, area):
    """관심 지역의 평균 NDVI 값 추출"""
    mean_dict = ndvi_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=area,
        scale=10,
        maxPixels=1e9
    )
    return mean_dict.get('NDVI').getInfo()


def compare_before_after(area, period_before, period_after, cloud_threshold=10):
    """산불 전후 NDVI 비교 분석"""
    # 산불 전
    img_before = get_sentinel2_image(area, period_before['start'], period_before['end'], cloud_threshold)
    ndvi_before = calculate_ndvi(img_before)
    mean_before = get_mean_ndvi(ndvi_before, area)
    date_before = ee.Date(img_before.get('system:time_start')).format('YYYY-MM-dd').getInfo()

    # 산불 후
    img_after = get_sentinel2_image(area, period_after['start'], period_after['end'], cloud_threshold)
    ndvi_after = calculate_ndvi(img_after)
    mean_after = get_mean_ndvi(ndvi_after, area)
    date_after = ee.Date(img_after.get('system:time_start')).format('YYYY-MM-dd').getInfo()

    # 변화 계산
    diff = mean_after - mean_before
    percent_change = (diff / mean_before) * 100

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