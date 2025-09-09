import streamlit as st
import pandas as pd
import altair as alt

# CSV 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

st.title("🌍 세계 MBTI 지도 시각화")
st.write("국가별로 가장 비율이 높은 MBTI 유형을 지도에 표시합니다.")

# Country 컬럼과 MBTI 16유형 열 분리
country_col = "Country"
mbti_cols = [c for c in df.columns if c != country_col]

# 각 나라별 MBTI 최빈(최대 비율) 유형 구하기
df_long = df.melt(id_vars=[country_col], value_vars=mbti_cols,
                  var_name="MBTI", value_name="Percent")

df_max = df_long.loc[df_long.groupby(country_col)["Percent"].idxmax()].reset_index(drop=True)

# ----------------------------
# 국가별 위도/경도 매핑 데이터 (샘플, 필요에 따라 확장)
# ----------------------------
country_coords = {
    "South Korea": (37.5665, 126.9780),
    "United States": (38.9072, -77.0369),
    "United Kingdom": (51.5074, -0.1278),
    "France": (48.8566, 2.3522),
    "Germany": (52.5200, 13.4050),
    "Japan": (35.6895, 139.6917),
    "Brazil": (-15.7939, -47.8828),
    "Canada": (45.4215, -75.6972),
    "Australia": (-35.2809, 149.1300),
    "India": (28.6139, 77.2090),
    "China": (39.9042, 116.4074),
    "Russia": (55.7558, 37.6173),
    "Mexico": (19.4326, -99.1332),
    "Italy": (41.9028, 12.4964),
    "Spain": (40.4168, -3.7038),
}

coords_df = pd.DataFrame([
    {"Country": k, "lat": v[0], "lon": v[1]} for k, v in country_coords.items()
])

# df_max와 좌표 데이터 병합
df_plot = pd.merge(df_max, coords_df, on="Country", how="inner")

# Altair scatter plot (위도/경도)
chart = alt.Chart(df_plot).mark_circle(size=200).encode(
    longitude="lon:Q",
    latitude="lat:Q",
    color="MBTI:N",
    tooltip=["Country", "MBTI", "Percent"]
).properties(
    width=800,
    height=400,
    title="국가별 최다 MBTI 유형 지도"
)

st.altair_chart(chart, use_container_width=True)

# ----------------------------
# 특정 MBTI 선택 → 지도 강조
# ----------------------------
st.subheader("특정 MBTI 유형 지도에서 보기")
selected_mbti = st.selectbox("MBTI 유형 선택", mbti_cols)

df_selected = df_plot[df_plot["MBTI"] == selected_mbti]

chart_selected = alt.Chart(df_selected).mark_circle(size=300, color="red").encode(
    longitude="lon:Q",
    latitude="lat:Q",
    tooltip=["Country", "MBTI", "Percent"]
).properties(
    width=800,
    height=400,
    title=f"{selected_mbti} 비율이 가장 높은 국가 지도"
)

st.altair_chart(chart_selected, use_container_width=True)

st.info("📌 좌표가 없는 국가는 표시되지 않습니다. 필요시 country_coords 사전에 추가하세요.")
