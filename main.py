# main.py
import streamlit as st
import pandas as pd
import altair as alt

st.title("MBTI 기반 직업 & 취미 추천 (샘플 데이터)")

# 샘플 데이터 생성
data = {
    "MBTI": ["INTJ", "INTJ", "ENFP", "ENFP", "ISTP", "ISTP", "ENTJ", "ENTJ"],
    "직업": ["연구원", "소프트웨어 엔지니어", "디자이너", "마케팅 전문가", "기계 엔지니어", "파일럿", "경영 컨설턴트", "변호사"],
    "취미": ["독서", "프로그래밍", "그림 그리기", "여행", "자동차 수리", "등산", "체스", "토론"]
}

df = pd.DataFrame(data)

st.subheader("샘플 데이터 미리보기")
st.dataframe(df)

# MBTI 유형 선택
mbti_options = df['MBTI'].unique()
selected_mbti = st.selectbox("MBTI 유형 선택", mbti_options)

# 선택된 MBTI 데이터 필터링
mbti_data = df[df['MBTI'] == selected_mbti]

st.subheader(f"{selected_mbti} 유형에 추천되는 직업과 취미")
st.write(mbti_data[['직업', '취미']])

# 직업 빈도 그래프
job_chart = alt.Chart(mbti_data).mark_bar().encode(
    x=alt.X('직업', sort='-y'),
    y='count()',
    tooltip=['직업', 'count()']
).properties(
    title=f"{selected_mbti} 유형의 직업 분포"
)

st.altair_chart(job_chart, use_container_width=True)
