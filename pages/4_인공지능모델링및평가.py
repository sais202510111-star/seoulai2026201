import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

st.title("🤖 4. 인공지능 모델링 및 평가")
st.markdown("다양한 AI 모델을 학습시켜 성능을 비교하고, 가장 우수한 모델을 선택해 청소년의 **스트레스 지수(1~10)**를 예측합니다.")

# 1. 데이터 로드 및 여러 모델 학습/평가 (캐싱 적용)
@st.cache_data
def train_and_compare_models():
    # 데이터 불러오기
    df = pd.read_csv("Teen_Mental_Health_Dataset.csv")
    
    # 독립변수(Features)와 종속변수(Target) 설정
    features = ['daily_social_media_hours', 'sleep_hours', 'screen_time_before_sleep', 'physical_activity']
    target = 'stress_level'
    
    X = df[features]
    y = df[target]
    
    # 데이터 분할 (80% 학습, 20% 검증)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 비교할 3가지 모델 정의
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
    }
    
    model_results = {}
    best_model_name = None
    best_f1 = -1
    
    # 각 모델별 학습 및 평가
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)
        
        model_results[name] = {
            "model": model,
            "accuracy": acc,
            "f1_score": f1
        }
        
        # F1-Score 기준으로 가장 우수한 모델 선정
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name

    return model_results, best_model_name, features

# 모델 학습 실행
try:
    results, best_name, feature_names = train_and_compare_models()
    data_loaded = True
except FileNotFoundError:
    st.error("파일을 찾을 수 없습니다. 'Teen_Mental_Health_Dataset.csv' 파일이 올바른 경로에 있는지 확인해주세요.")
    data_loaded = False

if data_loaded:
    st.markdown("---")
    st.subheader("📊 AI 모델별 성능 비교")
    st.markdown("스트레스 지수를 예측하기 위해 3가지 알고리즘을 학습시킨 결과입니다. (정밀한 평가를 위해 데이터 불균형을 고려한 F1-Score를 기준으로 비교합니다.)")

    # 표(DataFrame) 형태로 보기 쉽게 출력
    summary_data = []
    for name, info in results.items():
        summary_data.append({
            "AI 모델 이름": name,
            "정확도 (Accuracy)": f"{info['accuracy']*100:.1f}%",
            "F1-Score (Macro)": f"{info['f1_score']:.2f}"
        })
    st.table(pd.DataFrame(summary_data))

    # 최적 모델 안내 보기
    st.success(f"🏆 **선택된 최적의 모델:** `{best_name}` (F1-Score가 가장 높아 최종 예측기로 채택되었습니다.)")

    # 모델 상세 설명 (접어두기 기능 활용)
    with st.expander("ℹ️ 학습된 AI 모델 알고리즘 설명 보기"):
        st.markdown("""
        * **로지스틱 회귀 (Logistic Regression)**
            * 입력 데이터와 출력 클래스 간의 선형적인 관계를 확률로 계산하는 모델입니다. 계산이 빠르고 직관적이지만, 복잡한 패턴을 잡기엔 한계가 있습니다.
        * **의사결정나무 (Decision Tree)**
            * '수면 시간이 5시간 미만인가?'와 같이 스무고개처럼 데이터를 조건에 따라 가지치기하며 분류하는 모델입니다. 직관적이지만 과적합(오버피팅)되기 쉽습니다.
        * **랜덤 포레스트 (Random Forest)**
            * 여러 개의 의사결정나무를 만들어서 투표(앙상블)를 통해 최종 결론을 내는 모델입니다. 나무 하나보다 훨씬 똑똑하고 과적합을 잘 예방하여 일반적으로 성능이 우수합니다.
        """)

    st.markdown("---")
    st.subheader(f"🔮 실시간 스트레스 지수 예측기 (최적 모델: {best_name})")
    st.markdown("아래 정보를 입력하면 선정된 최적의 AI 모델이 스트레스 레벨(1~10)을 예측합니다.")

    # 입력 폼
    predict_col1, predict_col2 = st.columns(2)

    with predict_col1:
        sns_hours = st.slider("하루 평균 SNS 사용 시간 (시간)", 0.0, 10.0, 3.0, step=0.5)
        sleep_hours = st.slider("하루 평균 수면 시간 (시간)", 3.0, 12.0, 7.0, step=0.5)

    with predict_col2:
        screen_time_before_sleep = st.slider("취침 전 전자기기 화면 사용 시간 (시간)", 0.0, 4.0, 1.5, step=0.1)
        exercise_hours = st.slider("하루 평균 운동 시간 (시간)", 0.0, 3.0, 1.0, step=0.1)

    if st.button("🧠 AI 스트레스 예측 결과 보기"):
        input_data = np.array([[sns_hours, sleep_hours, screen_time_before_sleep, exercise_hours]])
        
        # 선택된 최적의 모델을 가져와서 예측 수행
        best_model = results[best_name]["model"]
        predicted_stress = best_model.predict(input_data)[0]
        
        st.markdown("### 🎯 AI 예측 결과")
        
        if predicted_stress >= 8:
            st.error(f"🚨 **위험 수준: 높음 (예측 스트레스 지수: {predicted_stress} / 10)**")
            st.markdown("AI 분석 결과 스트레스 수치가 매우 높게 예측되었습니다. 충분한 수면을 취하고 전자기기 사용을 줄이는 등의 관리가 필요합니다.")
        elif predicted_stress >= 4:
            st.warning(f"⚠️ **위험 수준: 보통 (예측 스트레스 지수: {predicted_stress} / 10)**")
            st.markdown("적당한 수준의 스트레스를 겪고 있습니다. 누적되지 않도록 취미나 가벼운 운동으로 환기해 주세요.")
        else:
            st.success(f"✅ **위험 수준: 낮음 (예측 스트레스 지수: {predicted_stress} / 10)**")
            st.markdown("스트레스 지수가 아주 안정적입니다! 현재의 건강한 생활 패턴을 잘 유지해 주세요.")
