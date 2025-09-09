import streamlit as st
import pandas as pd
import altair as alt

# =======================
# 앱 설정
# =======================
st.set_page_config(page_title="🌟 MBTI 직업/취미 추천", layout="wide")
st.title("🎨 MBTI 기반 직업 & 취미 추천 웹앱")
st.markdown("MBTI 유형을 선택하면 추천 직업, 취미, 특징을 확인하고, 직업 분포 그래프도 볼 수 있어요! 😊")

# =======================
# 사이드바: MBTI 선택 + CSV 업로드
# =======================
st.sidebar.header("설정")
uploaded_file = st.sidebar.file_uploader("CSV 파일 업로드 (선택)", type="csv")

# 샘플 MBTI 유형 선택
default_mbti = ["INTJ","ENFP","ISTP","ENTJ","ISFJ"]

# =======================
# CSV 데이터 불러오기
# =======================
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()  # 컬럼 공백 제거
    st.sidebar.success("CSV 업로드 완료!")
else:
    # 샘플 데이터
    df = pd.DataFrame({
        "MBTI":["INTJ","INTJ","ENFP","ENFP","ISTP","ISTP","ENTJ","ENTJ","ISFJ","ISFJ"],
        "직업":["연구원","소프트웨어 엔지니어","디자이너","마케팅 전문가","기계 엔지니어","파일럿","경영 컨설턴트","변호사","간호사","교사"],
        "취미":["독서","프로그래밍","그림 그리기","여행","자동차 수리","등산","체스","토론","정원 가꾸기","독서"],
        "설명":["창의적 분석","논리적 사고","창의적 활동","사람 중심","실용적 활동","도전적 성향","리더십","논리적 설득","배려","책임감"]
    })
    st.sidebar.info("CSV 없으면 샘플 데이터로 실행됩니다.")

# MBTI 컬럼 자동 감지
possible_mbti_cols = ['MBTI', 'Mbti', 'mbti', 'Type', 'type']
mbti_col = next((col for col in possible_mbti_cols if col in df.columns), None)

if mbti_col is None:
    st.error("CSV에 MBTI 컬럼이 없습니다. 컬럼명을 확인해주세요.")
else:
    # MBTI 선택
    mbti_options = df[mbti_col].unique()
    selected_mbti = st.sidebar.selectbox("MBTI 유형 선택", mbti_options)

    # MBTI별 데이터 필터링
    mbti_data = df[df[mbti_col]==selected_mbti]

    # =======================
    # 추천 내용 표시
    # =======================
    st.subheader(f"💡 {selected_mbti} 유형 특징 및 추천")
    for idx, row in mbti_data.iterrows():
        st.markdown(f"🎯 **직업:** {row['직업']}  |  🎨 **취미:** {row['취미']}  |  💡 **특징:** {row['설명']}")

    # =======================
    # 직업 분포 그래프
    # =======================
    if '직업' in mbti_data.columns:
        job_chart = alt.Chart(mbti_data).mark_bar(color="#FF6F61").encode(
            x=alt.X('직업', sort='-y'),
            y='count()',
            tooltip=['직업','count()']
        ).properties(title=f"{selected_mbti} 직업 추천 그래프")
        st.altair_chart(job_chart, use_container_width=True)

    # =======================
    # 취미 분포 그래프 (추가)
    # =======================
    if '취미' in mbti_data.columns:
        hobby_chart = alt.Chart(mbti_data).mark_bar(color="#6A5ACD").encode(
            x=alt.X('취미', sort='-y'),
            y='count()',
            tooltip=['취미','count()']
        ).properties(title=f"{selected_mbti} 취미 추천 그래프")
        st.altair_chart(hobby_chart, use_container_width=True)
