import streamlit as st
import pandas as pd

# CSV 파일 불러오기 (같은 폴더에 'mbti_직업_취미.csv' 있어야 함)
df = pd.read_csv("mbti_직업_취미.csv")

# 웹앱 제목
st.title("MBTI로 알아보는 직업과 취미 추천")

# 사용자가 MBTI 선택
mbti_list = sorted(df['MBTI'].unique())  # 중복 제거 및 정렬
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요:", mbti_list)

# 선택된 MBTI에 맞는 직업과 취미 필터링
filtered = df[df['MBTI'] == selected_mbti]

# 결과 출력
if not filtered.empty:
    st.subheader(f"✅ {selected_mbti} 유형에게 추천되는 직업과 취미")
    for idx, row in filtered.iterrows():
        st.write(f"- 직업: {row['직업']}")
        st.write(f"- 취미: {row['취미']}")
else:
    st.warning("해당 MBTI에 대한 데이터가 없습니다.")
