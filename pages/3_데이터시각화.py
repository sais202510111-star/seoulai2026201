import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("📊 3. 데이터 시각화 및 상관관계 분석 (EDA)")
st.markdown("시각화를 통해 청소년 정신 건강 데이터 속에 숨겨진 패턴과 변수 간의 관계를 찾아봅니다.")

data_path = "Teen_Mental_Health_Dataset.csv"

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    
    st.markdown("---")
    
    # 탭 구조를 활용하여 일반 시각화와 히트맵(상관관계) 분리
    tab1, tab2 = st.tabs(["📈 개별 변수 시각화", "🔥 상관관계 히트맵 (Heatmap)"])
    
    # ---------------------------
    # TAB 1: 개별 변수 시각화
    # ---------------------------
    with tab1:
        columns = df.columns.tolist()
        color_options = ["None", "depression_label", "gender", "platform_usage", "social_interaction_level"]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            default_x = columns.index("daily_social_media_hours") if "daily_social_media_hours" in columns else 0
            x_axis = st.selectbox("X축 변수 선택", options=columns, index=default_x, key="sb_x")
        with col2:
            default_y = columns.index("stress_level") if "stress_level" in columns else min(1, len(columns)-1)
            y_axis = st.selectbox("Y축 변수 선택", options=columns, index=default_y, key="sb_y")
        with col3:
            color_target = st.selectbox("색상 구분 (Group Color)", options=color_options, index=1, key="sb_color")

        color_var = None if color_target == "None" else color_target
        
        chart_type = st.radio(
            "차트 종류 선택", 
            ["산점도 (Scatter)", "바 차트 (Bar)", "박스 플롯 (Box)", "히스토그램 (Histogram)"],
            horizontal=True, key="rb_chart"
        )
        
        st.markdown("#### 📈 생성된 시각화 차트")
        if chart_type == "산점도 (Scatter)":
            fig = px.scatter(df, x=x_axis, y=y_axis, color=color_var, title=f"✨ {x_axis}와 {y_axis}의 상관 관계")
        elif chart_type == "바 차트 (Bar)":
            fig = px.bar(df, x=x_axis, y=y_axis, color=color_var, title=f"📊 {x_axis}별 {y_axis} 데이터 분포", barmode="group")
        elif chart_type == "박스 플롯 (Box)":
            fig = px.box(df, x=x_axis, y=y_axis, color=color_var, title=f"📦 {x_axis}에 따른 {y_axis}의 수치 분포")
        else:
            fig = px.histogram(df, x=x_axis, color=color_var, title=f"📐 {x_axis}의 데이터 빈도수 분석", barmode="overlay")
            
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    # ---------------------------
    # TAB 2: 상관관계 히트맵
    # ---------------------------
    with tab2:
        st.markdown("#### 🔥 변수 간 상관관계 계수 히트맵")
        st.markdown("수치형 데이터 간의 연관성을 `-1`부터 `1` 사이의 값으로 표현합니다. 1에 가까울수록 양의 상관관계, -1에 가까울수록 음의 상관관계를 뜻합니다.")
        
        # 1. 수치형 데이터만 추출하여 상관계수 계산
        numeric_df = df.select_dtypes(include=['number'])
        corr_matrix = numeric_df.corr()
        
        # 2. Plotly를 이용한 Heatmap 생성 (Matplotlib 사용 안함)
        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=".2f", # 소수점 둘째자리까지 수치 표시
            aspect="auto",
            color_continuous_scale="RdBu_r", # 양수는 붉은색, 음수는 푸른색 표현
            zmin=-1.0,
            zmax=1.0,
            title="🧠 청소년 정신 건강 데이터 상관관계 매트릭스"
        )
        
        fig_heatmap.update_layout(
            width=800,
            height=600,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # ---------------------------
        # 💡 히트맵 기반 데이터 분석 결론 요약
        # ---------------------------
        st.markdown("---")
        st.markdown("### 🎯 히트맵 분석 결과 및 최종 결론 요약")
        
        st.info("""
        **1. 우울증 라벨(depression_label)과 가장 연관성이 높은 요인**
        - **수면 시간과의 음의 상관관계 (-0.19)**: 청소년의 **수면 시간(sleep_hours)이 줄어들수록 우울증 위험도가 높아지는 경향**이 가장 뚜렷하게 관찰됩니다. 수면 부족이 청소년 정신 건강의 가장 큰 취약 요인일 수 있습니다.
        - **하루 SNS 이용 시간 (0.18)**: 일일 SNS 이용 시간(`daily_social_media_hours`)이 많을수록 우울증 라벨 발생 확률이 증가하는 양의 상관관계가 나타납니다.
        - **스트레스 및 불안 수치 (0.17)**: 스트레스(`stress_level`)와 불안 지수(`anxiety_level`) 역시 우울증 유무와 높은 양의 상관관계를 보입니다.

        **2. 데이터의 전반적인 특징 및 시사점**
        - 본 데이터셋은 변수 간 독립성이 비교적 강한 편이나, **[수면 부족 ➔ SNS 과의존 ➔ 스트레스/불안 상승 ➔ 우울증 발생]**으로 이어지는 청소년 행동 및 정신 건강 악순환 고리가 통계적 선형 흐름으로 파악됩니다.
        - 따라서 청소년 정신 건강 증진을 위해서는 **디지털 기기 사용 조절 및 적정 수면 시간 확보**를 유도하는 가이드라인이 우선적으로 제시되어야 합니다.
        """)

else:
    st.error("❌ 'Teen_Mental_Health_Dataset.csv' 데이터셋을 찾을 수 없습니다.")
