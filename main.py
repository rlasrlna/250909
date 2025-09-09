# main.py
import streamlit as st
import pandas as pd
import altair as alt

st.title("MBTI 기반 직업 & 취미 추천")

# 1. CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드 (예: countriesMBTI_16types.csv)", type="csv")

if uploaded_file is not None:
    # 2. CSV 읽기
    df = pd.read_csv(uploaded_file)
    
    st.subheader("데이터 미리보기")
    st.dataframe(df)
    
    # 3. MBTI 선택
    mbti_options = df['MBTI'].unique()
    selected_mbti = st.selectbox("MBTI 유형 선택", mbti_options)
    
    # 4. 선택된 MBTI 데이터 필터링
    mbti_data = df[df['MBTI'] == selected_mbti]
    
    st.subheader(f"{selected_mbti} 유형에 추천되는 직업과 취미")
    st.write(mbti_data[['직업', '취미']])
    
    # 5. 직업 빈도 그래프
    job_chart = alt.Chart(mbti_data).mark_bar().encode(
        x=alt.X('직업', sort='-y'),
        y='count()',
        tooltip=['직업', 'count()']
    ).properties(
        title=f"{selected_mbti} 유형의 직업 분포"
    )
    
    st.altair_chart(job_chart, use_container_width=True)
