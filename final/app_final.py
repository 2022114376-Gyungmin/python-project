"""
=================================================================
대구 함지산 NDVI 분석 대시보드 (app.py)
=================================================================

프로젝트: 대구 함지산 산불 NDVI 변화 분석
작성자: 최경민 (학번: 2022114376)
소속: 경북대학교 위치정보시스템학과

[실행방법]
1. conda activate gee
2. cd final 폴더
3. streamlit run app.py

=================================================================
"""

import streamlit as st
import ee
from NDVI_analyzer_final_module import compare_before_after

# =================================================================
# 페이지 기본 설정
# =================================================================

st.set_page_config(
    page_title = "대구 함지산 NDVI 분석",
    page_icon = "🌳",
    layout = "wide"
)

# =================================================================
# Earth Engine 초기화
# =================================================================

ee.Initialize(project = 'knu-project-ndvi-2026')

# =================================================================
# 헤더
# =================================================================

st.title("🌳 대구 함지산 NDVI 분석 대시보드")
st.markdown("### 위성영상 기반 식생 피해 정량화")
st.caption("경북대학교 위치정보시스템학과 | Sentinel-2 데이터")

st.divider()

# =================================================================
# 프로젝트 설명
# =================================================================

st.markdown("""
### 📍 프로젝트 개요

**2025년 4월 28일** 대구광역시 북구 함지산에서 발생한 산불은
**약 260헥타르**의 산림에 피해를 입혔습니다.

이 대시보드는 **Sentinel-2 위성영상**과 **NDVI (정규화 식생지수)** 분석으로
산불 피해를 정량적으로 측정합니다.
""")

st.info("""
**🔎 분석 방법**: 같은 계절끼리 비교 (작년 5월 vs 올해 5월)
계절 효과를 제거하고 순수 산불 영향만 측정합니다.
""")

st.divider()

# =================================================================
# 분석 실행 버튼
# =================================================================

st.markdown("### 🚀 NDVI 분석 실행")

if st.button("분석 시작", type = "primary", use_container_width = True):

    # 로딩 표시
    with st.spinner("위성영상 분석 중... (약 10~20초 소요)"):

        # 분석 영역: 함지산 산불 피해지 중심 반경 800m
        area = ee.Geometry.Point([128.5774, 35.9145]).buffer(800)

        # 비교 시기: 작년 5월 vs 올해 5월
        period_before = {'start': '2024-05-01', 'end': '2024-05-31'}
        period_after = {'start': '2025-05-01', 'end': '2025-05-31'}

        # 메인 분석 함수 호출
        result = compare_before_after(area, period_before, period_after)

    # 완료 메세지
    st.success("✅ 분석 완료!")

    st.divider()

    # =============================================================
    # 결과 표시
    # =============================================================

    st.markdown("### 📊 분석 결과")

    # 영상 날짜 표시
    col_d1, col_d2 = st.columns(2)
    col_d1.caption(f"📅 산불 전 영상: {result['date_before']}")
    col_d2.caption(f"📅 산불 후 영상: {result['date_after']}")

    # NDVI 숫자 비교 (메인 결과)
    col1, col2, col3 = st.columns(3)

    col1.metric(
        label = "산불 전 NDVI",
        value = f"{result['mean_before']:.3f}",
        delta = "기준 시점"
    )

    col2.metric(
        label = "산불 후 NDVI",
        value = f"{result['mean_after']:.3f}",
        delta = f"{result['percent_change']:.1f}%"
    )

    col3.metric(
        label = "변화량",
        value = f"{result['diff']:.3f}",
        delta = "식생 감소"
    )

    # 결과 해석
    st.markdown(f"""
    ### 🔍 결과 해석

    함지산 산불 피해 지역의 평균 NDVI가 **{result['mean_before']:.3f}**에서
    **{result['mean_after']:.3f}**로 감소했습니다.

    이는 **약 {abs(result['percent_change']):.1f}%의 식생 감소**를 의미하며,
    산불로 인한 식생 피해를 정량적으로 보여줍니다.
    """)

    # 상세 데이터 (펼침)
    with st.expander("📋 상세 분석 데이터 보기"):
        st.markdown(f"""
        **분석 영역**: 함지산 중심 반경 800m

        **사용 영상**:
        - 산불 전: {result['date_before']} (Sentinel-2)
        - 산불 후: {result['date_after']} (Sentinel-2)

        **NDVI 값**:
        - 산불 전: {result['mean_before']:.4f}
        - 산불 후: {result['mean_after']:.4f}
        - 차이: {result['diff']:.4f}
        - 변화율: {result['percent_change']:.2f}%

        **계산 공식**: NDVI = (B8 - B4) / (B8 + B4)
        
        **데이터 출처**: Copernicus Sentinel-2 (해상도 10m)
        """)