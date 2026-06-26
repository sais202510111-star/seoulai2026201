import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("📊 3. 데이터 시각화 (EDA)")
st.markdown("시각화를 통해 청소년 정신 건강 데이터 속에 숨겨진 패턴을 찾아봅니다.")

data_path = "Teen_Mental_Health_Dataset.csv"

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    
    st.markdown("---")
    
    # 시각화할 컬럼 선택 숏컷 (실제 CSV 컬럼명에 맞게 변경 필요)
    columns = df.columns.tolist()
    
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("X축 변수 선택", options=columns, index=0)
    with col2:
        y_axis = st.selectbox("Y축 변수 선택(수치형 추천)", options=columns, index=min(1, len(columns)-1))
        
    chart_type = st.radio("차트 종류 선택", ["산점도 (Scatter)", "바 차트 (Bar)", "박스 플롯 (Box)"])
    
    st.markdown("#### 📈 생성된 시각화 차트")
    if chart_type == "산점도 (Scatter)":
        fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{x_axis}와 {y_axis}의 관계")
    elif chart_type == "바 차트 (Bar)":
        fig = px.bar(df, x=x_axis, y=y_axis, title=f"{x_axis}별 {y_axis} 합계/평균")
    else:
        fig = px.box(df, x=x_axis, y=y_axis, title=f"{x_axis}에 따른 {y_axis} 분포")
        
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("❌ 데이터셋을 찾을 수 없습니다.")
