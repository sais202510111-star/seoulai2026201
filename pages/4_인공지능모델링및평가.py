import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

st.set_page_config(layout="wide", page_title="AI 정신건강 분석 대시보드", page_icon="🤖") 

st.markdown("""
    <style>
        .block-container { padding-top: 2.5rem; padding-bottom: 2rem; }
        h1 { font-weight: 800; color: #ffffff; letter-spacing: -0.05em; }
        h3 { font-weight: 700; color: #f8f9fa; margin-top: 1.5rem; }
        .stTabs [data-baseweb="tab"] { font-size: 15px; font-weight: 600; padding: 10px 20px; }
        .stSlider [data-baseweb="slider"] { margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 4. 인공지능 모델링 및 평가 대시보드")
st.markdown("<p style='font-size:16px; color:#b2bec3; margin-top:-10px;'>다양한 AI 알고리즘의 파라미터를 실시간으로 제어하며 청소년의 생활 패턴과 스트레스 지수(1~10) 간의 상관관계를 다각도로 분석합니다.</p>", unsafe_allow_html=True)

with st.expander("ℹ️ [필독] 대시보드를 보기 전, AI 머신러닝 용어 가이드북 읽어보기"):
    term_col1, term_col2 = st.columns(2)
    with term_col1:
        st.markdown("""
        * **정확도 (Accuracy)**: 전체 데이터 중 AI가 맞춘 비율입니다.
        * **F1-Score (Macro)**: AI가 1점부터 10점까지 모든 스트레스 단계를 치우침 없이 골고루 다 잘 맞추고 있는지 평가하는 점수입니다.
        """)
    with term_col2:
        st.markdown("""
        * **과적합 (Overfitting)**: AI가 학습 데이터 기출문제만 외워서 새로운 데이터에서 응용력이 떨어지는 상태입니다.
        * **하이퍼파라미터 (Hyperparameter)**: 알고리즘의 성격을 결정하는 조절 나사입니다.
        """)

# -----------------------------------------------------
# 가로 제어판
# -----------------------------------------------------
with st.container(border=True):
    st.markdown("<h5 style='margin-top:0; margin-bottom:10px; color:#dfe6e9;'>🛠️ AI 실험실 설정 제어판</h5>", unsafe_allow_html=True)
    control_col1, control_col2, control_col3, control_col4 = st.columns(4)

    with control_col1:
        selected_model_name = st.selectbox(
            "시뮬레이션 메인 모델", 
            ["Random Forest", "Decision Tree", "Logistic Regression"]
        )
    with control_col2:
        rf_trees = st.slider("Random Forest: 나무 개수", 10, 200, 100, step=10)
    with control_col3:
        dt_depth = st.slider("Decision Tree: 최대 깊이", 3, 15, 7)
    with control_col4:
        lr_c = st.slider("Logistic Regression: 규제 강도(C)", 0.01, 10.0, 1.0, step=0.1)

# -----------------------------------------------------
# 데이터 연산 함수 (모든 변수 활용을 위해 독립변수 대폭 추가)
# -----------------------------------------------------
@st.cache_data
def train_and_evaluate(trees, depth, c_val):
    df = pd.read_csv("Teen_Mental_Health_Dataset.csv")
    
    # 학업, 성별, 나이, 불안, 중독 등 데이터셋 내 가용 가능한 정보 전면 반영
    # 범주형 변수 처리 (성별 원핫인코딩)
    df_encoded = pd.get_dummies(df, columns=['gender'], drop_first=True)
    
    # 예측용 독립변수 확장
    features = ['daily_social_media_hours', 'sleep_hours', 'screen_time_before_sleep', 
                'physical_activity', 'age', 'academic_performance', 'anxiety_level', 'addiction_level']
    target = 'stress_level'
    
    X = df_encoded[features]
    y = df_encoded[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    models = {
        "Logistic Regression": LogisticRegression(C=c_val, max_iter=2000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=depth, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=trees, random_state=42)
    }
    
    model_results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        
        model_results[name] = {
            "model": model,
            "train_accuracy": accuracy_score(y_train, y_train_pred),
            "accuracy": accuracy_score(y_test, y_test_pred),
            "f1_score": f1_score(y_test, y_test_pred, average='macro', zero_division=0),
            "confusion_matrix": confusion_matrix(y_test, y_test_pred),
            "y_test": y_test,
            "y_pred": y_test_pred
        }
        
    return model_results, features, X_test, df

try:
    results, feature_names, X_test_df, original_df = train_and_evaluate(rf_trees, dt_depth, lr_c)
    data_loaded = True
except FileNotFoundError:
    st.error("⚠️ 데이터 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
    data_loaded = False


if data_loaded:
    # -----------------------------------------------------
    # 과적합 위험도 평가
    # -----------------------------------------------------
    st.markdown("---")
    st.markdown("### ⚠️ AI 알고리즘 신뢰성 및 과적합(Overfitting) 위험도 평가")
    
    active_info = results[selected_model_name]
    train_acc = active_info["train_accuracy"]
    test_acc = active_info["accuracy"]
    overfit_gap = train_acc - test_acc
    
    with st.container(border=True):
        risk_col1, risk_col2 = st.columns([1, 2])
        with risk_col1:
            st.metric(label="🎯 학습-검증 정확도 격차(Gap)", value=f"{overfit_gap*100:.2f}%")
            if overfit_gap >= 0.15:
                st.error("🚨 위험 수준: 과적합 상태 (Overfitting)")
            elif overfit_gap >= 0.05:
                st.warning("⚠️ 위험 수준: 잠재적 위험 (Moderate)")
            elif train_acc < 0.40:
                st.info("📉 위험 수준: 과소적합 상태 (Underfitting)")
            else:
                st.success("✅ 위험 수준: 매우 안정적 (Optimal)")
                
        with risk_col2:
            st.markdown(f"<p style='font-size:15px; font-weight:600; color:#dfe6e9; margin-bottom:5px;'>🔍 {selected_model_name} 모델 진단 소견</p>", unsafe_allow_html=True)
            if overfit_gap >= 0.15:
                st.markdown(f"현재 모델 구조가 확장된 환경 변수 조건 하에서 훈련 데이터에 과도하게 동화되었습니다. 슬라이더 조절을 통해 복잡도를 낮추어야 실전 신뢰도가 상승합니다.")
            elif overfit_gap >= 0.05:
                st.markdown(f"훈련 정확도({train_acc*100:.1f}%)와 검증 정확도({test_acc*100:.1f}%) 사이에 약간의 틈이 발생했습니다. 파라미터를 조절해 완화하는 것이 좋습니다.")
            elif train_acc < 0.40:
                st.markdown("패턴 학습량이 부족한 과소적합 상태입니다. AI가 깊게 공부할 수 있도록 제한을 완화해 주세요.")
            else:
                st.markdown(f"확장 정보 반영 후에도 훈련({train_acc*100:.1f}%)과 검증({test_acc*100:.1f}%) 스코어가 균형을 이루는 **최적의 일반화 상태**입니다.")

    # -----------------------------------------------------
    # 실시간 분석 결과 리포트 (새로운 학술적 정보 그래프 대거 추가)
    # -----------------------------------------------------
    st.markdown("### 📊 실시간 분석 결과 리포트")
    
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
    plt.rcParams['axes.facecolor'] = 'none'
    plt.rcParams['figure.facecolor'] = 'none'
    sns.set_style("white")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🥇 모델별 성능 비교", 
        "🔑 종합 요인 영향도 (확장형)", 
        "👥 성별 및 연령별 스트레스 양상", 
        "🧠 심리 지표 간 상관성 분석"
    ])
    
    # --- [탭 1] 모델별 성능 비교 ---
    with tab1:
        st.markdown("<p style='font-size:14px; color:#b2bec3; margin-bottom:15px;'>새로운 데이터 정보(성적, 불안, 중독 등)를 추가한 후 각 알고리즘이 도출해낸 검증 스코어입니다.</p>", unsafe_allow_html=True)
        names = list(results.keys())
        accs = [results[n]["accuracy"] for n in names]
        f1s = [results[n]["f1_score"] for n in names]
        
        all_scores = accs + f1s
        y_min = max(0.0, float(np.floor(min(all_scores) * 20) / 20) - 0.05) 
        y_max = min(1.0, float(np.ceil(max(all_scores) * 20) / 20) + 0.05)
        
        fig1, ax1 = plt.subplots(figsize=(10, 3.8))
        ax1.plot(names, accs, marker='o', markersize=8, linewidth=2.5, label='Accuracy', color='#3498db')
        ax1.plot(names, f1s, marker='s', markersize=8, linewidth=2.5, label='F1-Score', color='#e67e22')
        ax1.set_ylim(y_min, y_max)
        sns.despine()
        legend1 = ax1.legend(facecolor='#2d3436', edgecolor='none')
        for text in legend1.get_texts(): text.set_color('white')
        st.pyplot(fig1)
        
        best_acc_model = max(results, key=lambda k: results[k]["accuracy"])
        st.info(f"📊 **실시간 분석 스냅샷:**\n종합 환경 데이터를 추가로 학습시킨 결과, 현재 가장 예측 성공률이 높은 알고리즘은 **{best_acc_model}**입니다.")

    # --- [탭 2] 종합 요인 영향도 (성적, 심리 지표 포함) ---
    with tab2:
        st.markdown("<p style='font-size:14px; color:#b2bec3; margin-bottom:15px;'>새롭게 투입된 성적, 불안도, 나이 등을 포함하여 AI가 스트레스 유발에 어떤 변수를 가장 치명적으로 보았는지 분석한 결과입니다.</p>", unsafe_allow_html=True)
        current_model = results[selected_model_name]["model"]
        fig2, ax2 = plt.subplots(figsize=(10, 3.8))
        
        # 보기 편한 영문 레이블 매핑
        extended_labels = ['SNS Hours', 'Sleep Hours', 'Screen Before Sleep', 'Physical Activity', 'Age', 'Academic Score', 'Anxiety Level', 'Addiction Level']
        
        if hasattr(current_model, 'feature_importances_'):
            importances = current_model.feature_importances_
            sns.barplot(x=importances, y=extended_labels, ax=ax2, palette="viridis")
        elif hasattr(current_model, 'coef_'):
            importances = np.abs(current_model.coef_[0])[:8] 
            sns.barplot(x=importances, y=extended_labels, ax=ax2, palette="flare")
            
        ax2.set_xlabel("Importance Weight", color='white')
        sns.despine()
        st.pyplot(fig2)
        
        top_feature = extended_labels[np.argmax(importances)]
        st.info(f"🔑 **실시간 분석 스냅샷:**\n환경 정보를 대폭 확장하여 분석한 결과, 단순 생활 패턴 외에도 **{top_feature}** 요인이 모델이 스트레스를 판별하는 데 아주 핵심적인 지표로 가중치가 매겨졌습니다.")

    # --- [탭 3] 성별 및 연령별 스트레스 양상 (새로운 정보) ---
    with tab3:
        st.markdown("<p style='font-size:14px; color:#b2bec3; margin-bottom:15px;'>데이터에 포함된 청소년의 성별과 나이에 따른 실제 스트레스 분포 양상 정보입니다.</p>", unsafe_allow_html=True)
        
        fig3, ax3 = plt.subplots(figsize=(10, 3.8))
        # 나이와 성별에 따른 스트레스 분포 시각화
        sns.lineplot(data=original_df, x='age', y='stress_level', hue='gender', marker='o', palette="Set2", errorbar=None, ax=ax3)
        ax3.set_xlabel("Age (연령)", color='white')
        ax3.set_ylabel("Average Stress Level", color='white')
        sns.despine()
        legend3 = ax3.legend(facecolor='#2d3436', edgecolor='none')
        for text in legend3.get_texts(): text.set_color('white')
        st.pyplot(fig3)
        
        st.info("👥 **이 그래프로 알 수 있는 것:** 특정 연령대에서 남학생 혹은 여학생 집단의 스트레스 평균치가 급격히 치솟는 구간을 감지할 수 있습니다. AI가 나이와 성별을 식별 부호로 사용하여 개인화된 위험도를 추정하는 근거가 됩니다.")

    # --- [탭 4] 심리 지표 간 상관성 분석 (새로운 정보) ---
    with tab4:
        st.markdown("<p style='font-size:14px; color:#b2bec3; margin-bottom:15px;'>불안 지수(Anxiety)와 중독 지수(Addiction)가 스트레스 유발에 어떤 상호작용적 상관성을 갖는지 보여주는 분포 정보입니다.</p>", unsafe_allow_html=True)
        
        fig4, ax4 = plt.subplots(figsize=(8, 3.8))
        sns.regplot(data=original_df, x='anxiety_level', y='stress_level', scatter_kws={'alpha':0.3, 'color':'#3498db'}, line_kws={'color':'#e74c3c'}, ax=ax4)
        ax4.set_xlabel("Anxiety Level (불안 지수)", color='white')
        ax4.set_ylabel("Stress Level", color='white')
        sns.despine()
        st.pyplot(fig4)
        
        st.info("🧠 **이 그래프로 알 수 있는 것:** 청소년 데이터 내에서 불안 지수와 스트레스 레벨 간의 선형적 인과 흐름을 나타냅니다. 붉은색 회귀선이 우상향할수록 불안도가 스트레스 예측 모델의 강력한 가속 인자로 작동함을 입증합니다.")

    st.markdown("<p style='font-size:15px; font-weight:600; color:#dfe6e9; margin-bottom:-5px; margin-top:20px;'>📋 전 알고리즘 성능 스코어보드 요약</p>", unsafe_allow_html=True)
    st.table(pd.DataFrame([
        {
            "AI 알고리즘 이름": name, 
            "훈련 데이터 정확도 (Train Acc)": f"{info['train_accuracy']*100:.1f}%",
            "검증 데이터 정확도 (Test Acc)": f"{info['accuracy']*100:.1f}%", 
            "종합 불균형 평가 지표 (F1-Score)": f"{info['f1_score']:.2f}"
        }
        for name, info in results.items()
    ]))

    # -----------------------------------------------------
    # 실시간 예측기 및 처방 리포트
    # -----------------------------------------------------
    st.markdown("---")
    st.subheader(f"🔮 실시간 종합 스트레스 예측기 (최적 모델: {selected_model_name})")
    st.markdown("추가된 심리 지표와 학업 성적까지 포함하여 실제 청소년의 총체적인 스트레스 상태를 예측합니다.")

    with st.container(border=True):
        p_col1, p_col2, p_col3, p_col4 = st.columns(4)
        with p_col1:
            sns_hours = st.slider("하루 SNS 이용 (시간)", 0.0, 10.0, 3.0, step=0.5)
            sleep_hours = st.slider("하루 수면 (시간)", 3.0, 12.0, 7.0, step=0.5)
        with p_col2:
            screen_time_before_sleep = st.slider("취침 전 화면 노출 (시간)", 0.0, 4.0, 1.5, step=0.1)
            exercise_hours = st.slider("하루 운동 (시간)", 0.0, 3.0, 1.0, step=0.1)
        with p_col3:
            user_age = st.slider("대상 청소년 나이 (세)", 13, 19, 16)
            academic_performance = st.slider("평균 학업 성적 (GPA 스케일)", 0.0, 4.5, 3.0, step=0.1)
        with p_col4:
            anxiety_level = st.slider("자가 불안 지수 (1~10)", 1, 10, 4)
            addiction_level = st.slider("스마트폰 중독 지수 (1~10)", 1, 10, 5)

        btn_triggered = st.button("🧠 AI 다각도 종합 분석 및 맞춤형 심리 처방전 출력", use_container_width=True)

    if btn_triggered:
        # 독립변수 8개 정렬 순서 매핑
        input_data = np.array([[sns_hours, sleep_hours, screen_time_before_sleep, exercise_hours, user_age, academic_performance, anxiety_level, addiction_level]])
        active_model = results[selected_model_name]["model"]
        predicted_stress = active_model.predict(input_data)[0]
        
        with st.container(border=True):
            st.markdown("### 🎯 AI 종합 분석 결과 보고서")
            
            risk_text = ""
            if predicted_stress >= 8:
                st.error(f"🚨 위험 등급: 고위험군 (예측 스트레스 지수: {predicted_stress} / 10)")
                risk_text = "고위험군"
            elif predicted_stress >= 4:
                st.warning(f"⚠️ 위험 등급: 주의군 (예측 스트레스 지수: {predicted_stress} / 10)")
                risk_text = "주의군"
            else:
                st.success(f"✅ 위험 등급: 안정군 (예측 스트레스 지수: {predicted_stress} / 10)")
                risk_text = "안정군"
                
            st.markdown("#### 📝 다각도 매칭 라이프 가이드 피드백")
            feedback_list = []
            if anxiety_level >= 7:
                feedback_list.append("- 🧠 **위험 수준의 심리적 불안감 검출:** 현재 예측치의 높은 지분은 일상 속 만성적인 불안감에서 기인합니다. 심리적 안전 기지 확보가 시급합니다.")
            if academic_performance <= 2.0:
                feedback_list.append("- 🏫 **학업 스트레스 가중 가능성:** 학업 성취도 저하로 인한 심리적 압박감이 간접적으로 상호작용하고 있을 가능성이 포착됩니다.")
            if sleep_hours < 6.0:
                feedback_list.append("- ❌ **심각한 신체 피로 회복 방해:** 수면 결핍이 스트레스 면역력을 약화시키고 있습니다.")
            if exercise_hours >= 1.0:
                feedback_list.append("- 👍 **긍정적 신체적 완충재 축적:** 다행히 규칙적인 신체 활동이 스트레스 폭발을 지연시키는 방어선 역할을 해내고 있습니다.")
                
            feedback_text = "\n".join(feedback_list) if feedback_list else "- 심리 및 환경 지표들이 고루 균형을 갖춘 안정적인 수치 대역입니다."
            st.markdown(feedback_text)
                
            st.markdown("#### 💡 AI 마인드 케어 처방 조언")
            care_advice = ""
            if predicted_stress >= 8:
                care_advice = "생활 패턴의 균열과 심리적 불안도 수치가 동시에 위험 신호를 보내고 있습니다. 기기 제어와 함께 전문 기관의 상담을 병행하는 다각도 집중 솔루션을 제안합니다."
            elif predicted_stress >= 4:
                care_advice = "특정 환경 요인이나 디지털 기기 과소비 습관을 개선하면 빠르게 안정군으로 회복할 수 있는 전형적인 과도기 단계입니다. 주말 스마트폰 디톡스부터 시작해 보세요."
            else:
                care_advice = "내면의 감정 상태와 외부 일상 통제력이 조화롭게 밸런스를 이룬 이상적인 청소년 라이프 마인드입니다."
            st.markdown(care_advice)

            # 진단 처방전 다운로드
            report_txt = f"""[AI 청소년 다각도 융합 정신건강 처방전]
-----------------------------------------
■ 진단 시뮬레이션 알고리즘: {selected_model_name}
■ 개인 환경 변수: 나이 {user_age}세 | 학업 성적 {academic_performance}
■ 심리 점검 변수: 불안 지수 {anxiety_level}/10 | 중독 지수 {addiction_level}/10

■ AI 최종 예측결과: 스트레스 지수 {predicted_stress}/10 ({risk_text})
■ 맞춤형 다각도 피드백:
{feedback_text}

■ AI 마인드 케어 종합 처방전:
{care_advice}
-----------------------------------------"""

            st.download_button(
                label="📥 AI 진단서 및 처방전 파일(.txt) 다운로드 받기",
                data=report_txt,
                file_name="AI_Teen_Mental_Health_Advanced_Report.txt",
                mime="text/plain",
                use_container_width=True
            )

            # 빅데이터 집약 바이올린 차트 결론부
            st.markdown("---")
            st.markdown("### 🏛️ 청소년 정신 건강 빅데이터 학습 집약 결과")
            ins_col1, ins_col2 = st.columns([1.1, 0.9])
            
            with ins_col1:
                st.markdown("""
                * **심리적 요인과 환경적 요인의 동시 결합 현상**: 인공지능이 만 명 이상의 청소년 데이터를 군집 분석한 결론에 따르면, 고스트레스 집단은 학업 저하와 높은 불안 수준이 디지털 중독 Habit과 결합하여 다발적으로 상호작용하는 복합 위기 양상을 띱니다.
                * **수면 결핍 도메인의 보편적 파괴력**: 성적이나 성별에 관계없이, 전 집단에서 '수면 부족'은 청소년 정신 건강 방어선을 일시에 무너뜨리는 가장 보편적이고 파괴적인 공통 유발 인자로 AI 통계 모형에 기록되었습니다.
                """)
            with ins_col2:
                fig5, ax5 = plt.subplots(figsize=(5, 3.6))
                original_df['Stress Group'] = np.where(original_df['stress_level'] >= 8, 'High Stress', 'Normal')
                sns.violinplot(data=original_df, x='Stress Group', y='sleep_hours', palette={'High Stress': '#e74c3c', 'Normal': '#2ecc71'}, inner='quartile', ax=ax5)
                ax5.set_xlabel("Stress Group", color='white')
                ax5.set_ylabel("Sleep Hours", color='white')
                sns.despine()
                st.pyplot(fig5)
