# Streamlit 가져오기
import streamlit as st

# 페이지 제목
st.title("🔥 대구 함지산 산불 NDVI 분석 대시보드")

# 부제목
st.subheader("위성영상으로 보는 산불 피해")

# 일반 텍스트
st.write("안녕하세요! 이것은 제 첫 Streamlit 대시보드입니다.")

# 마크다운 텍스트
st.markdown("""
이 대시보드는 **2025년 4월 28일** 대구광역시 북구 함지산에서 발생한 
산불의 식생 피해를 분석합니다.

- 데이터: Sentinel-2 위성영상
- 분석 방법: NDVI (정규화 식생 지수)
- 비교: 작년 5월 vs 올해 5월
""")

# 구분선
st.divider()

# 버튼
if st.button("분석 시작 버튼 (테스트)"):
    st.write("버튼을 눌렀어요! 🎉")
    st.success("아직 분석은 안 하지만, 버튼이 동작해요!")

# 슬라이더
st.subheader("슬라이더 테스트")
value = st.slider("값을 선택하세요", 0, 100, 50)
st.write(f"선택한 값: {value}")

# 셀렉트박스
st.subheader("드롭다운 테스트")
region = st.selectbox("지역 선택", ["함지산", "의성", "달성"])
st.write(f"선택한 지역: {region}")

# 컬럼 (가로 배치)
st.subheader("컬럼 테스트")
col1, col2 = st.columns(2)
col1.metric("산불 전 NDVI", "0.693", "기준")
col2.metric("산불 후 NDVI", "0.484", "-30.2%")