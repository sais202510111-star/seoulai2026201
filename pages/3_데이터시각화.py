import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 페이지 기본 설정
st.set_page_config(
    page_title="데이터 시각화 (EDA)",
    page_icon="📊",
    layout="wide"
)

st.title("📊 청소년 정신 건강 데이터 시각화 결과 보고서")
st.markdown("우리 데이터셋의 주요 핵심 항목들을 5가지 대표 시각화 기법을 통해 각각 개별 그래프로 시각화한 결과입니다.")

data_path = "Teen_Mental_Health_Dataset.csv"

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    
    # ----------------------------------------------------------------
    # 📦 1. 박스 차트 (Box Plot) 영역
    # ----------------------------------------------------------------
    st.markdown("---")
    st.subheader("📦 1. 박스 차트 (Box Plot) : 성별에 따른 정서 지표 분포 범위")
    st.markdown("성별 그룹별로 청소년들의 스트레스, 불안감, 중독 수준의 사분위 범위와 중앙값을 직관적으로 비교합니다.")
    
    box_col1, box_col2, box_col3 = st.columns(3)
    with box_col1:
        fig_box1 = px.box(df, x="gender", y="stress_level", color="gender", title="성별에 따른 스트레스 지수 분포", template="plotly_white", color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_box1, use_container_width=True)
    with box_col2:
        fig_box2 = px.box(df, x="gender", y="anxiety_level", color="gender", title="성별에 따른 불안감 수준 분포", template="plotly_white", color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_box2, use_container_width=True)
    with box_col3:
        fig_box3 = px.box(df, x="gender", y="addiction_level", color="gender", title="성별에 따른 스마트폰 중독도 분포", template="plotly_white", color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_box3, use_container_width=True)

    # ----------------------------------------------------------------
    # 🎻 2. 분포 차트 (Violin Plot) 영역
    # ----------------------------------------------------------------
    st.markdown("---")
    st.subheader("🎻 2. 분포 차트 (Violin Plot) : 플랫폼별 SNS 사용 현황 및 수면 밀도")
    st.markdown("주로 사용하는 SNS 플랫폼 유형에 따라 하루 평균 사용 시간과 수면 시간의 데이터 밀집 패턴(지형 구조)을 확인합니다.")
    
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        fig_viol1 = px.violin(df, x="platform_usage", y="daily_social_media_hours", color="platform_usage", box=True, points="all", title="주 사용 플랫폼별 하루 SNS 시간 밀도", template="plotly_white", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_viol1, use_container_width=True)
    with v_col2:
        fig_viol2 = px.violin(df, x="platform_usage", y="sleep_hours", color="platform_usage", box=True, points="all", title="주 사용 플랫폼별 일일 수면 시간 밀도", template="plotly_white", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_viol2, use_container_width=True)

    # ----------------------------------------------------------------
    # 📐 3. 히스토그램 (Histogram) 영역
    # ----------------------------------------------------------------
    st.markdown("---")
    st.subheader("📐 3. 히스토그램 (Histogram) : 핵심 건강 요소의 학생 빈도수 조사")
    st.markdown("우리 데이터에 포함된 청소년들의 실제 수면 시간과 취침 전 스마트폰 사용 시간이 어떤 형태로 분포되어 있는지 빈도를 측정합니다.")
    
    h_col1, h_col2 = st.columns(2)
    with h_col1:
        fig_hist1 = px.histogram(df, x="sleep_hours", title="전체 학생들의 수면 시간 빈도 분포", nbins=15, template="plotly_white", color_discrete_sequence=["#3b82f6"])
        st.plotly_chart(fig_hist1, use_container_width=True)
    with h_col2:
        fig_hist2 = px.histogram(df, x="screen_time_before_sleep", title="전체 학생들의 취침 전 화면 시청 시간 빈도 분포", nbins=15, template="plotly_white", color_discrete_sequence=["#ef4444"])
        st.plotly_chart(fig_hist2, use_container_width=True)

    # ----------------------------------------------------------------
    # 🔥 4. 상관관계 지도 (Heatmap) 영역
    # ----------------------------------------------------------------
    st.markdown("---")
    st.subheader("🔥 4. 상관관계 지도 (Heatmap) : 전체 수치 변수 간 연관성 분석 격차판")
    st.markdown("데이터셋에 있는 모든 수치형 데이터 항목들을 한자리에 모아 서로 얼마나 밀접하게 동맹 혹은 반비례 관계를 갖는지 수치 톤으로 요약합니다.")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    corr_matrix = df[numeric_cols].corr()
    
    fig_heatmap = px.imshow(
        corr_matrix, text_auto=".2f", aspect="auto",
        color_continuous_scale="RdBu_r", zmin=-1.0, zmax=1.0,
        title="🧠 데이터 변수 간 피어슨 상관계수 행렬 격자판"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # ----------------------------------------------------------------
    # ✨ 5. 흐름 산점도 (Scatter Plot) 영역
    # ----------------------------------------------------------------
    st.markdown("---")
    st.subheader("✨ 5. 흐름 산점도 (Scatter Plot) : 리스크 요인별 추세선과 흐름")
    st.markdown("개별 청소년의 데이터 포인트를 사방에 뿌려 원인 지표의 변화에 따른 정신건강 결과 수치의 실시간 경향을 추적합니다.")
    
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        fig_scat1 = px.scatter(df, x="daily_social_media_hours", y="stress_level", color="gender", trendline="ols", title="SNS 사용 시간 증가에 따른 스트레스 흐름과 추세선", opacity=0.7, template="plotly_white")
        st.plotly_chart(fig_scat1, use_container_width=True)
    with s_col2:
        fig_scat2 = px.scatter(df, x="sleep_hours", y="anxiety_level", color="gender", trendline="ols", title="평균 수면 시간 변화에 따른 불안 지수 흐름과 추세선", opacity=0.7, template="plotly_white")
        st.plotly_chart(fig_scat2, use_container_width=True)

else:
    st.error("❌ 'Teen_Mental_Health_Dataset.csv' 파일을 불러올 수 없습니다. 경로를 확인해 주세요.")
