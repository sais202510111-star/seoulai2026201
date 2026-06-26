import streamlit as st
import pandas as pd
import os

st.title("🛠️ 2. 데이터 전처리 (Data Preprocessing)")
st.markdown("데이터 분석 및 AI 모델링에 적합하도록 데이터를 정제하는 단계입니다.")

data_path = "Teen_Mental_Health_Dataset.csv"

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    
    st.markdown("---")
    st.subheader("🧼 데이터 정제 및 변환 시뮬레이션")
    
    # 전처리 선택지 제공 예시
    preprocess_option = st.checkbox("결측치 자동 처리 (정수형은 평균값, 범주형은 최빈값)")
    
    if preprocess_option:
        # 가상의 결측치 처리 로직
        processed_df = df.fillna(df.mode().iloc[0]) 
        st.success("✨ 결측치 처리가 완료되었습니다!")
        st.dataframe(processed_df.head(), use_container_width=True)
    else:
        st.info("위 체크박스를 선택하면 전처리 후의 데이터를 확인할 수 있습니다.")
        st.dataframe(df.head(), use_container_width=True)
        
    st.markdown("""
    ### ⚙️ 전처리 단계 요약
    1. **결측치(Missing Value) 처리**: 데이터 누락값 정제
    2. **인코딩(Encoding)**: 범주형 데이터(예: 성별, 학년)를 수치형으로 변환
    3. **스케일링(Scaling)**: 수치형 변수의 범위를 표준화/정규화
    """)
else:
    st.error("❌ 데이터셋을 찾을 수 없습니다.")
