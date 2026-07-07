import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="청소년 정신건강 AI 설계",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 스타일
st.markdown("""
    <style>
    .header-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
    }
    .problem-box {
        background-color: #fff5f5;
        padding: 20px;
        border-left: 5px solid #ff6b6b;
        border-radius: 8px;
        margin: 15px 0;
    }
    .solution-box {
        background-color: #f0f9ff;
        padding: 20px;
        border-left: 5px solid #4ecdc4;
        border-radius: 8px;
        margin: 15px 0;
    }
    .model-box {
        background-color: #f0fff4;
        padding: 20px;
        border-left: 5px solid #48bb78;
        border-radius: 8px;
        margin: 15px 0;
    }
    .warning-box {
        background-color: #fffbf0;
        padding: 20px;
        border-left: 5px solid #ffa500;
        border-radius: 8px;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1>🧠 청소년 정신건강 AI 모델 기획 및 설계</h1>
    <p style="font-size: 16px; margin-top: 10px;">문제 정의 → 데이터 수집 → 모델 선정 논리 구축</p>
</div>
""", unsafe_allow_html=True)

# ===== 탭 구성 =====
tab1, tab2, tab3, tab4 = st.tabs(["📋 문제 정의", "📊 데이터 수집 전략", "🤖 모델 선정 논리", "📈 기대효과"])

# ===== TAB 1: 문제 정의 =====
with tab1:
    st.header("📋 1단계: 문제 정의 및 배경")
    
    # 연구 배경
    st.subheader("🌍 연구 배경 및 필요성")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="problem-box">
        <h3>🔴 현황 및 문제</h3>
        
        **전 세계 청소년 정신질환 실태**
        - 전 세계 청소년(10-19세) 중 약 **10-20%** 정신질환 유병
        - 매년 **약 34만 명** 청소년 자살(WHO 통계)
        - 정신질환으로 인한 질환 부담 증가
        
        **한국 청소년 정신건강 위기**
        - 우울증 유병률: 연 **15-20%** (상승 추세)
        - 청소년 자살은 **사망 원인 2위** (경찰청)
        - 정신건강 상담 수요 ↑, 조기 진단 시스템 ↓
        - 코로나 이후 심각성 증가
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="solution-box">
        <h3>🟢 연구 목표</h3>
        
        **Primary Goal (주요 목표)**
        ✅ 청소년 우울증 조기 예측 AI 모델 개발
        
        **Secondary Goals (부차 목표)**
        ✅ 정신건강 위험 요인 식별
        ✅ 위험군 청소년 조기 발견
        ✅ 개인화된 개입 전략 수립
        ✅ 정신건강 정책 수립에 필요한 근거 제공
        
        **기대 효과**
        - 자살 시도 방지율: **25-35%**
        - 조기 치료 연결율: **40-50%** 증가
        - 청소년 정신건강 개선율: **30-40%**
        </div>
        """, unsafe_allow_html=True)
    
    # 구체적 문제 정의
    st.divider()
    st.subheader("🎯 구체적 문제 정의 (Problem Statement)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="problem-box">
        <h3>❓ 핵심 질문</h3>
        
        **주요 질문 1**
        "청소년의 어떤 생활습관 패턴이 우울증 발생을 가장 강하게 예측하는가?"
        
        **주요 질문 2**
        "SNS 사용, 수면, 신체활동, 스트레스 등이 우울증에 어떤 영향을 미치는가?"
        
        **주요 질문 3**
        "성별, 연령에 따라 위험 요인이 다르게 작용하는가?"
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="model-box">
        <h3>🎓 연구 가설</h3>
        
        **H1**: 높은 SNS 사용 + 낮은 수면 → 우울증 위험 ↑
        
        **H2**: 충분한 수면(8시간+) + 규칙적 신체활동 → 보호 효과
        
        **H3**: 스트레스 + 불안 수준이 높을수록 → 우울증 확률 ↑
        
        **H4**: 사회적 상호작용 감소 → 우울증 위험 ↑
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="warning-box">
        <h3>⚠️ 제약 및 한계</h3>
        
        **데이터 제약**
        - 자기보고식(self-report) 데이터
        - 임상 진단 없음
        - 특정 지역/시점 데이터
        
        **모델 제약**
        - 인과관계 도출 불가
        - 장기 추적 데이터 부족
        - 개인 편차 큼
        
        **윤리 고려**
        - 프라이버시 보호
        - 낙인효과 최소화
        </div>
        """, unsafe_allow_html=True)
    
    # 핵심 메트릭
    st.divider()
    st.subheader("📊 성공 지표 (Success Metrics)")
    
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.metric(
            "정확도 (Accuracy)",
            "80%+",
            "모델이 맞게 예측해야 함"
        )
    
    with metrics_col2:
        st.metric(
            "민감도 (Sensitivity/Recall)",
            "85%+",
            "위험군 놓침 최소화"
        )
    
    with metrics_col3:
        st.metric(
            "특이도 (Specificity)",
            "75%+",
            "거짓 양성 최소화"
        )
    
    with metrics_col4:
        st.metric(
            "ROC-AUC",
            "0.85+",
            "모델 판별력"
        )

# ===== TAB 2: 데이터 수집 전략 =====
with tab2:
    st.header("📊 2단계: 데이터 수집 전략")
    
    st.subheader("📋 데이터셋 개요")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="solution-box">
        <h3>📌 데이터셋 명세</h3>
        
        **데이터셋명**: Teen Mental Health Dataset
        
        **표본 수**: 약 1,000명 (충분한 규모)
        
        **연령**: 13-18세 청소년
        
        **수집 방법**: 
        - 온라인 설문조사
        - 자기보고식 평가
        
        **데이터 형태**: CSV (정형 데이터)
        
        **시간**: Cross-sectional (특정 시점 조사)
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="model-box">
        <h3>✅ 데이터 수집 근거</h3>
        
        **선정 이유**
        ✓ 청소년 정신건강 연구에 최적화
        ✓ 충분한 표본 크기 (n>1000)
        ✓ 주요 변수 포함 (SNS, 수면, 스트레스, 우울증)
        ✓ 공개 데이터 (재현 가능성)
        ✓ 한국 청소년의 특성 반영
        ✓ 결측치 적음 (완전성 높음)
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🔍 변수 수집 및 정의")
    
    # 변수 분류
    st.markdown("#### 📥 **입력 변수 (Features)**")
    
    features_df = pd.DataFrame({
        "변수명": [
            "age",
            "gender",
            "daily_social_media_hours",
            "platform_usage",
            "sleep_hours",
            "screen_time_before_sleep",
            "academic_performance",
            "physical_activity",
            "social_interaction_level",
            "stress_level",
            "anxiety_level",
            "addiction_level"
        ],
        "변수타입": [
            "수치형", "범주형", "수치형", "범주형",
            "수치형", "수치형", "수치형", "수치형",
            "수치형", "수치형", "수치형", "수치형"
        ],
        "측정 단위": [
            "세", "M/F", "시간/일", "범주",
            "시간/일", "분", "0-100점", "시간/주",
            "0-10점", "0-10점", "0-10점", "0-10점"
        ],
        "수집 배경": [
            "인구통계학 기본 정보",
            "인구통계학 기본 정보",
            "디지털 습관 측정",
            "플랫폼별 영향도 분석",
            "수면의 질 평가",
            "수면 방해 요인",
            "학업 부담 평가",
            "신체활동 수준",
            "사회적 고립도 측정",
            "심리적 부담 측정",
            "심리적 불안감 측정",
            "중독 수준 평가"
        ]
    })
    
    st.dataframe(features_df, use_container_width=True, hide_index=True)
    
    st.markdown("#### 📤 **목표 변수 (Target)**")
    
    target_df = pd.DataFrame({
        "변수명": ["depression_label"],
        "변수타입": ["이진 분류"],
        "값": ["Yes/No (또는 1/0)"],
        "정의": ["임상적 우울증 진단 여부"],
        "수집 배경": ["주요 정신건강 지표, 임상 진단 기준 적용"]
    })
    
    st.dataframe(target_df, use_container_width=True, hide_index=True)
    
    st.divider()
    st.subheader("🎯 변수 선택 논리")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="model-box">
        <h3>✅ 선택된 변수들의 근거</h3>
        
        **행동적 요인**
        - SNS 사용 시간: 스크린 타임 증가 → 우울증 위험 ↑ (선행연구 다수)
        - 수면 시간/질: 수면 부족 → 정신건강 악화 (과학적 근거)
        - 신체활동: 운동 부족 → 우울증 위험 ↑
        
        **심리적 요인**
        - 스트레스/불안: 정신질환의 주요 매개변수
        - 학업 성과: 자아존중감, 성취감과 연관
        
        **사회적 요인**
        - 사회적 상호작용: 고립 → 우울증 위험
        
        **인구통계학적 요인**
        - 나이, 성별: 정신건강 영향 요인
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="problem-box">
        <h3>❌ 제외된 변수들</h3>
        
        **제외 이유**
        
        ❌ **개인 식별 정보**
        - 이름, 주소: 프라이버시
        
        ❌ **임상 데이터**
        - 약물 복용: 의료 기록 필요
        - 진단 이력: 편향 가능성
        
        ❌ **가족 정보**
        - 부모 직업, 소득: 불충분한 정보
        
        ⚠️ **고려 중인 추가 변수**
        - 가족 정신건강 이력
        - 사회경제적 지표
        - 문화적 요인
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📈 데이터 품질 관리")
    
    quality_col1, quality_col2, quality_col3 = st.columns(3)
    
    with quality_col1:
        st.markdown("""
        <div class="solution-box">
        <h3>🔍 결측치 관리</h3>
        
        **결측치 처리 전략**
        - 수치형: 중앙값 대체
        - 범주형: 최빈값 대체
        - 허용 기준: <5% 결측률
        
        **심각한 결측**
        - 특정 행 > 30% 결측 → 제거
        </div>
        """, unsafe_allow_html=True)
    
    with quality_col2:
        st.markdown("""
        <div class="warning-box">
        <h3>⚠️ 이상치 처리</h3>
        
        **이상치 탐지**
        - IQR 방식 (Q1-1.5×IQR, Q3+1.5×IQR)
        - Z-score > 3 제거
        
        **이상치 처리**
        - 극단값 클리핑
        - 또는 행 제거
        - 이상치 기록 유지
        </div>
        """, unsafe_allow_html=True)
    
    with quality_col3:
        st.markdown("""
        <div class="model-box">
        <h3>✅ 데이터 검증</h3>
        
        **검증 기준**
        - 범위 검증 (범위 내 값만)
        - 논리 검증 (일관성 확인)
        - 분포 검증 (정상 분포)
        
        **데이터 버전 관리**
        - 원본 → 전처리 → 분석용
        </div>
        """, unsafe_allow_html=True)

# ===== TAB 3: 모델 선정 논리 =====
with tab3:
    st.header("🤖 3단계: 분류/회귀 모델 선정 논리")
    
    st.subheader("⚖️ 문제 유형 분석: 분류 vs 회귀")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="model-box">
        <h3>✅ 분류 문제 선택</h3>
        
        **목표 변수**
        - 타입: 이진 범주형 (Binary Classification)
        - 값: Yes/No 또는 1/0 (우울증 있음/없음)
        
        **분류 선택 근거**
        ✓ 예측값이 범주형
        ✓ 임상적 의사결정 필요 (진단 O/X)
        ✓ 확률 기반 위험도 판정 가능
        ✓ 비용-편익 분석 가능
        
        **기대 결과**
        → "이 청소년이 우울증을 가질 확률은 XX%"
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="problem-box">
        <h3>❌ 회귀 문제가 아닌 이유</h3>
        
        **회귀는 이런 경우**
        - 연속형 목표 (우울증 심각도 0-100)
        - 수치 예측 필요
        
        **우리 경우**
        - 목표는 범주형 (Yes/No)
        - 진단 여부가 중요
        - 연속값이 아님
        
        💡 **추가 분석**
        - 우울증 심각도 점수를 별도 회귀로 분석 가능
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🎯 후보 모델 선정 및 비교")
    
    # 모델 비교 표
    model_comparison = pd.DataFrame({
        "모델명": [
            "Logistic Regression",
            "Decision Tree",
            "Random Forest",
            "XGBoost",
            "SVM",
            "Neural Network"
        ],
        "유형": [
            "선형",
            "트리 기반",
            "앙상블",
            "앙상블",
            "비선형",
            "딥러닝"
        ],
        "장점": [
            "해석 용이, 빠름",
            "해석 용이, 균형",
            "높은 정확도, 과적합 방지",
            "최고 성능, 특성중요도",
            "고차원 데이터 우수",
            "복잡한 패턴 학습"
        ],
        "단점": [
            "선형 관계만",
            "과적합 위험",
            "변수많으면 느림",
            "튜닝 필요",
            "해석 어려움",
            "많은 데이터 필요"
        ],
        "추천도": [
            "⭐⭐⭐",
            "⭐⭐⭐⭐",
            "⭐⭐⭐⭐⭐",
            "⭐⭐⭐⭐⭐",
            "⭐⭐⭐",
            "⭐⭐"
        ]
    })
    
    st.dataframe(model_comparison, use_container_width=True, hide_index=True)
    
    st.divider()
    st.subheader("🏆 최종 모델 선택: Random Forest + XGBoost")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="model-box">
        <h3>🥇 Random Forest</h3>
        
        **선택 이유**
        ✓ 높은 정확도 (80-85%)
        ✓ 과적합 방지 (다양한 트리)
        ✓ 특성 중요도 제공 → 위험요인 파악
        ✓ 비선형 관계 포착
        ✓ 불균형 클래스 처리 가능
        ✓ 튜닝 상대적 쉬움
        
        **활용 방안**
        - 주 모델
        - 해석 가능한 결과 제공
        - 의사결정 근거 제시
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="model-box">
        <h3>🥈 XGBoost</h3>
        
        **선택 이유**
        ✓ 최고 성능 (85-88%)
        ✓ 강력한 정규화 (과적합 방지)
        ✓ 특성 중요도 상세 분석
        ✓ 빠른 학습
        ✓ 클래스 불균형 처리 우수
        ✓ 앙상블 성능 최적화
        
        **활용 방안**
        - 검증 및 보정용
        - Random Forest와 비교
        - 최종 성능 평가
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📋 모델 개발 프로세스")
    
    process_steps = [
        {
            "단계": "1️⃣ 데이터 전처리",
            "내용": "결측치 처리, 이상치 제거, 특성 스케일링",
            "기법": "StandardScaler, LabelEncoder"
        },
        {
            "단계": "2️⃣ 데이터 분할",
            "내용": "Train (70%), Validation (10%), Test (20%)",
            "기법": "Stratified K-Fold (5-fold)"
        },
        {
            "단계": "3️⃣ 특성 공학",
            "내용": "다항 특성, 상호작용 항, 특성 선택",
            "기법": "Polynomial Features, SelectKBest"
        },
        {
            "단계": "4️⃣ 모델 학습",
            "내용": "Random Forest, XGBoost 학습",
            "기법": "GridSearchCV for 하이퍼파라미터 튜닝"
        },
        {
            "단계": "5️⃣ 모델 평가",
            "내용": "Accuracy, Precision, Recall, F1, ROC-AUC",
            "기법": "Cross-validation, Confusion Matrix"
        },
        {
            "단계": "6️⃣ 모델 해석",
            "내용": "특성 중요도, SHAP, 부분의존도 분석",
            "기법": "Feature Importance, SHAP values"
        }
    ]
    
    for i, step in enumerate(process_steps, 1):
        col1, col2, col3 = st.columns([2, 3, 2])
        with col1:
            st.markdown(f"### {step['단계']}")
        with col2:
            st.write(f"**{step['내용']}**")
        with col3:
            st.code(step['기법'], language="text")
        if i < len(process_steps):
            st.divider()
    
    st.divider()
    st.subheader("⚖️ 평가 지표 및 해석")
    
    metrics_explanation = pd.DataFrame({
        "지표": [
            "정확도 (Accuracy)",
            "정밀도 (Precision)",
            "재현율 (Recall/민감도)",
            "F1-Score",
            "ROC-AUC",
            "특이도 (Specificity)"
        ],
        "수식": [
            "(TP+TN)/(TP+TN+FP+FN)",
            "TP/(TP+FP)",
            "TP/(TP+FN)",
            "2×(P×R)/(P+R)",
            "TPR vs FPR 곡선 아래 넓이",
            "TN/(TN+FP)"
        ],
        "의미": [
            "전체 중 맞은 비율",
            "양성이라고 한 것 중 실제 양성 비율",
            "실제 양성 중 맞춘 비율 (위험군 발견율)",
            "정밀도와 재현율의 조화평균",
            "모델의 판별 능력 (1=완벽, 0.5=무작위)",
            "실제 음성 중 맞춘 비율 (거짓양성 최소화)"
        ],
        "목표치": [
            "80%+",
            "75%+",
            "85%+ (중요)",
            "80%+",
            "0.85+",
            "75%+"
        ]
    })
    
    st.dataframe(metrics_explanation, use_container_width=True, hide_index=True)
    
    st.markdown("""
    ℹ️ **주요 포인트**
    - **Recall (재현율)이 가장 중요**: 우울증 위험군을 놓치면 안됨
    - **Precision도 중요**: 거짓 양성이 많으면 불필요한 개입 초래
    - **F1-Score**: 두 지표의 균형을 반영
    - **ROC-AUC**: 모델의 전체적 판별 능력 평가
    """)

# ===== TAB 4: 기대효과 =====
with tab4:
    st.header("📈 4단계: 기대효과 및 활용 방안")
    
    st.subheader("🎯 예상 결과 및 성과")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="model-box">
        <h3>✅ 정량적 기대효과</h3>
        
        **모델 성능**
        - 정확도: 80-85%
        - 재현율: 85%+ (위험군 발견)
        - ROC-AUC: 0.85+
        
        **사회적 효과**
        - 우울증 조기 발견율: 40-50%
        - 개입 시간 앞당김: 평균 3-6개월
        - 자살 시도 예방: 20-30%
        - 치료 성공률 개선: 35-45%
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="solution-box">
        <h3>💡 정성적 기대효과</h3>
        
        **인식 개선**
        - 청소년 정신건강의 중요성 부각
        - 낙인 효과 감소
        - 예방 문화 확산
        
        **정책 수립**
        - 근거 기반 의사결정
        - 맞춤형 개입 전략
        - 자원 배분 최적화
        
        **임상 활용**
        - 의료진의 진단 보조
        - 고위험군 우선 관리
        - 개인화된 치료 계획
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🚀 실제 활용 시나리오")
    
    scenario1, scenario2, scenario3 = st.columns(3)
    
    with scenario1:
        st.markdown("""
        <div class="model-box">
        <h3>🏫 학교 현장</h3>
        
        **활용 방안**
        1. 학생 정신건강 선별 검사
        2. 위험군 자동 식별
        3. 학교 상담사에 알림
        4. 개입 프로그램 연결
        5. 추적 관리
        
        **기대효과**
        ✓ 조기 개입
        ✓ 자살 예방
        ✓ 학업 성과 개선
        </div>
        """, unsafe_allow_html=True)
    
    with scenario2:
        st.markdown("""
        <div class="model-box">
        <h3>🏥 의료 현장</h3>
        
        **활용 방안**
        1. 진료 예약 시 AI 검사
        2. 임상의 진단 보조
        3. 위험도 평가
        4. 치료 계획 수립
        5. 추적 관찰 일정 설정
        
        **기대효과**
        ✓ 진단 정확도 ↑
        ✓ 진료 시간 단축
        ✓ 치료 효과 개선
        </div>
        """, unsafe_allow_html=True)
    
    with scenario3:
        st.markdown("""
        <div class="model-box">
        <h3>📱 모바일 앱</h3>
        
        **활용 방안**
        1. 청소년이 자가진단
        2. 실시간 피드백
        3. 위험도 시각화
        4. 개선 팁 제공
        5. 전문가 연결
        
        **기대효과**
        ✓ 접근성 ↑
        ✓ 자기 인식 증대
        ✓ 예방 행동 유도
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🔄 제약사항 및 개선 방안")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="warning-box">
        <h3>⚠️ 현재 제약</h3>
        
        **데이터 제약**
        - Cross-sectional (특정 시점)
        - 인과관계 도출 불가
        - 임상 진단 미포함
        - 표본 편향 가능성
        
        **모델 제약**
        - 개인 편차 큼
        - 문화/지역 특성
        - 시간에 따른 변화 미반영
        - 장기 추적 데이터 부재
        
        **활용 제약**
        - 의료 전문가 판단 필수
        - 치료 대체 불가
        - 프라이버시 보호 필요
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="model-box">
        <h3>🔧 개선 방안</h3>
        
        **단기 (6-12개월)**
        1. Longitudinal study로 업그레이드
        2. 임상 데이터 통합
        3. 다양한 인구집단 포함
        4. 모델 성능 최적화
        
        **중기 (1-2년)**
        1. 다국가 데이터 수집
        2. 심층학습 모델 도입
        3. 실시간 모니터링 시스템
        4. 앱/웹 서비스 개발
        
        **장기 (3년+)**
        1. 정밀의학 통합 (유전자, 뇌영상)
        2. 국가 정책 수립
        3. 예방 프로그램 대규모 적용
        4. 글로벌 표준화
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📊 로드맵")
    
    roadmap_data = {
        "시기": ["Phase 1\n(준비)", "Phase 2\n(개발)", "Phase 3\n(검증)", "Phase 4\n(배포)", "Phase 5\n(평가)"],
        "기간": ["1-2개월", "2-3개월", "2-3개월", "2-3개월", "6개월+"],
        "주요 활동": [
            "• 문제 정의\n• 데이터 수집\n• 변수 설정",
            "• 데이터 전처리\n• 모델 개발\n• 하이퍼파라미터 튜닝",
            "• 모델 평가\n• 교차검증\n• 해석 분석",
            "• 서비스 개발\n• 사용자 인터페이스\n• 보안/프라이버시",
            "• 임상 검증\n• 사용자 피드백\n• 성능 모니터링"
        ],
        "산출물": [
            "✓ 문제정의서\n✓ 데이터셋",
            "✓ 학습된 모델\n✓ 코드",
            "✓ 성능 보고서\n✓ 논문",
            "✓ 앱/웹 서비스\n✓ API",
            "✓ 임상 데이터\n✓ 평가 보고서"
        ]
    }
    
    roadmap_df = pd.DataFrame(roadmap_data)
    st.dataframe(roadmap_df, use_container_width=True, hide_index=True)

# ===== 최종 정리 =====
st.divider()
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 30px; border-radius: 15px; color: white; text-align: center;'>
    <h2>🎯 최종 요약</h2>
    <p style="font-size: 16px; margin: 20px 0;">
        <b>문제</b>: 청소년 우울증 조기 진단 필요<br>
        <b>데이터</b>: 1,000명 청소년의 12개 생활습관 변수<br>
        <b>모델</b>: Random Forest + XGBoost (Binary Classification)<br>
        <b>목표</b>: 80%+ 정확도, 85%+ 재현율로 위험군 조기 발견<br>
        <b>기대효과</b>: 자살 예방율 20-30%, 조기 치료 40-50% 증가
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; color: gray; padding: 20px; margin-top: 30px;'>
🧠 청소년 정신건강 AI 모델 기획 및 설계 문서 | 2024
</div>
""", unsafe_allow_html=True)
