import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="MBTI 직업/취미 추천", layout="wide")
st.title("MBTI 기반 직업 & 취미 추천 앱")

# -----------------------
# 1. CSV 파일 읽기
# -----------------------
try:
    df = pd.read_csv("mbti_data.csv")
    df.columns = df.columns.str.strip()  # 컬럼 공백 제거
except FileNotFoundError:
    st.warning("CSV 파일을 찾을 수 없습니다. 업로드를 사용하세요.")
    df = pd.DataFrame()

# -----------------------
# 2. CSV 업로드 기능
# -----------------------
uploaded_file = st.file_uploader("원하는 CSV 파일 업로드 (선택)", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    st.success("CSV 파일 업로드 완료!")

# -----------------------
# 3. CSV 확인
# -----------------------
if not df.empty:
    st.subheader("데이터 미리보기")
    st.dataframe(df)

    # MBTI 컬럼 자동 감지
    possible_mbti_cols = ['MBTI', 'Mbti', 'mbti', 'Type', 'type']
    mbti_col = next((col for col in possible_mbti_cols if col in df.columns), None)

    if mbti_col is None:
        st.error("CSV 파일에 MBTI 컬럼이 없습니다. 컬럼명을 확인해주세요.")
    else:
        # MBTI 선택
        mbti_options = df[mbti_col].unique()
        selected_mbti = st.selectbox("MBTI 유형 선택", mbti_options)

        # 선택된 MBTI 데이터 필터링
        mbti_data = df[df[mbti_col] == selected_mbti]

        st.subheader(f"{selected_mbti} 유형에 추천되는 직업과 취미")
        for col in ['직업', '취미']:
            if col not in mbti_data.columns:
                st.warning(f"CSV에 '{col}' 컬럼이 없습니다.")
        st.write(mbti_data[['직업', '취미']].dropna())

        # 직업 빈도 그래프
        if '직업' in mbti_data.columns:
            job_chart = alt.Chart(mbti_data).mark_bar().encode(
                x=alt.X('직업', sort='-y'),
                y='count()',
                tooltip=['직업', 'count()']
            ).properties(
                title=f"{selected_mbti} 유형의 직업 분포"
            )
            st.altair_chart(job_chart, use_container_width=True)
else:
    st.info("CSV 파일이 없으면 샘플 데이터로 앱을 실행할 수도 있습니다.")
