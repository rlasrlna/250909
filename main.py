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
    df.columns = df.columns.str.strip()  # 컬럼 공백 제거
    
    st.subheader("CSV 컬럼 확인")
    st.write(df.columns.tolist())
    
    # 3. MBTI 컬럼 찾기 (자동 감지)
    possible_mbti_cols = ['MBTI', 'Mbti', 'mbti', 'Type', 'type']
    mbti_col = None
    for col in possible_mbti_cols:
        if col in df.columns:
            mbti_col = col
            break
    
    if mbti_col is None:
        st.error("CSV 파일에 MBTI 컬럼이 없습니다. 컬럼명을 확인해주세요.")
    else:
        # 4. MBTI 선택
        mbti_options = df[mbti_col].unique()
        selected_mbti = st.selectbox("MBTI 유형 선택", mbti_options)
        
        # 5. 선택된 MBTI 데이터 필터링
        mbti_data = df[df[mbti_col] == selected_mbti]
        
        st.subheader(f"{selected_mbti} 유형에 추천되는 직업과 취미")
        # '직업'과 '취미' 컬럼도 자동 공백 제거
        for col in ['직업', '취미']:
            if col not in mbti_data.columns:
                st.warning(f"CSV에 '{col}' 컬럼이 없습니다.")
        st.write(mbti_data[['직업', '취미']].dropna())
        
        # 6. 직업 빈도 그래프
        if '직업' in mbti_data.columns:
            job_chart = alt.Chart(mbti_data).mark_bar().encode(
                x=alt.X('직업', sort='-y'),
                y='count()',
                tooltip=['직업', 'count()']
            ).properties(
                title=f"{selected_mbti} 유형의 직업 분포"
            )
            st.altair_chart(job_chart, use_container_width=True)
