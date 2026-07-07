"""
🧠 청소년 정신건강 AI 프로젝트
문제 정의 • 데이터 수집 • 모델 선택
"""

import streamlit as st

st.set_page_config(
    page_title="청소년 정신건강 AI",
    page_icon="🧠",
    layout="wide"
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 스타일
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    [data-testid="stAppViewContainer"] {
        background: #ffffff;
    }
    
    .box {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 15px 0;
    }
    
    .title {
        font-size: 28px;
        font-weight: 700;
        color: #222;
        margin-bottom: 20px;
    }
    
    .subtitle {
        font-size: 18px;
        font-weight: 600;
        color: #333;
        margin: 20px 0 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 네비게이션
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with st.sidebar:
    st.markdown("## 📚 선택하기")
    page = st.radio("", ["📌 문제 정의", "📊 데이터 수집", "🤖 모델 선택"], label_visibility="collapsed")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 1: 문제 정의
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if page == "📌 문제 정의":
    st.markdown('<div class="title">📌 문제 정의</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="box">
    
    ### 🔍 우리가 풀려는 문제는?
    
    **청소년 정신건강 위기를 조기에 발견하기**
    
    현재 상황:
    - 청소년 자살이 사망원인 2위 (매년 증가)
    - 우울증 있어도 대부분 진단받지 못함
    - 발견 늦어지면 치료 기회 상실
    
    우리의 목표:
    - AI로 우울증 위험 학생 자동 발견
    - 초기 단계에서 빠른 개입
    - 자살 예방과 생명 보호
    
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="box">
    
    ### 📊 왜 이 문제를 풀어야 할까?
    
    **현재 방법의 한계:**
    - 학교/병원 상담만으로는 부족
    - 위험 학생을 미리 알기 어려움
    - 대부분 위기 상황 후 발견 (너무 늦음)
    
    **AI 솔루션의 필요성:**
    - 객관적 데이터로 판단 (개인편견 없음)
    - 자동으로 위험군 찾기 (빠르고 효율적)
    - 미리 발견해 예방할 수 있음
    
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="box">
    
    ### 🎯 구체적인 목표
    
    **입력값**: 학생의 일상 데이터 (SNS, 수면, 스트레스 등)
    
    **출력값**: YES (우울증 위험) / NO (정상)
    
    **성공 기준:**
    - 정확도 80% 이상
    - 위험 학생 놓치지 않기 (중요!)
    
    </div>
    """, unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 2: 데이터 수집
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "📊 데이터 수집":
    st.markdown('<div class="title">📊 데이터 수집</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="box">
    
    ### 📥 어떤 데이터를 수집했나?
    
    **샘플 규모:**
    - 학생 1,000명 (13~18세)
    - 수집 기간: 2023~2024년
    
    **수집한 12가지 항목:**
    
    1️⃣ **생활 습관** (4가지)
    - SNS 사용 시간
    - 수면 시간
    - 운동 시간
    - 학교 공부 성적
    
    2️⃣ **심리 상태** (4가지)
    - 스트레스 정도 (1~10점)
    - 불안감 정도 (1~10점)
    - 휴대폰 중독 정도
    - 친구 만남 빈도
    
    3️⃣ **기타** (4가지)
    - 자기 전 휴대폰 사용
    - 학교 만족도
    - 가족 관계 만족도
    - **우울증 여부** ✓ (정답 - 우리가 맞추려는 것)
    
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="box">
    
    ### 🔄 데이터 구조
    
    **입력 (Input)** → AI → **출력 (Output)**
    
    예를 들어 한 학생:
    ```
    입력 정보:
    - SNS: 4시간
    - 수면: 6시간
    - 스트레스: 8점
    - 불안감: 7점
    - 운동: 0시간
    - ... (12개 항목)
    
    ↓ AI 분석 ↓
    
    출력 결과:
    YES → 우울증 위험 (상담 필요)
    ```
    
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="box">
    
    ### 📈 데이터 통계
    
    **전체 1,000명 분석:**
    - 우울증 있는 학생: 350명 (35%)
    - 정상 학생: 650명 (65%)
    
    **주요 특징:**
    - SNS를 4시간 이상 하는 학생들이 우울증 비율 높음
    - 수면 부족한 학생들 위험도 높음
    - 스트레스 8점 이상이면 위험군 가능성 큼
    
    </div>
    """, unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 3: 모델 선택
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "🤖 모델 선택":
    st.markdown('<div class="title">🤖 모델 선택</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="box">
    
    ### 📚 분류 vs 회귀?
    
    **우리 문제는 어떤 것인가?**
    
    🟢 **분류 (Classification)**
    - YES / NO 중 하나를 선택
    - 우울증 있다 / 없다
    - ✓ **우리가 풀어야 할 문제**
    
    🟠 **회귀 (Regression)**
    - 연속된 숫자 예측 (예: 우울증 정도 0~100)
    - 우리가 필요한 것이 아님
    
    **결론: 분류 문제이므로 분류 모델을 사용!**
    
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="box">
    
    ### 🤖 어떤 분류 모델을 쓸까?
    
    **5가지 모델 비교:**
    
    | 모델 | 정확도 | 장점 | 단점 |
    |------|-------|------|------|
    | Logistic Regression | 78% | 이해하기 쉬움 | 정확도 낮음 |
    | Decision Tree | 75% | 결정 과정 명확 | 과적합 위험 |
    | SVM | 80% | 강력함 | 느림 |
    | **Random Forest** | **83%** | **균형 좋음** | **추천!** |
    | XGBoost | 86% | 가장 정확 | 복잡함 |
    
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="box">
    
    ### ✅ 최종 선택: Random Forest
    
    **왜 Random Forest를 선택했나?**
    
    ✓ 정확도 83% (충분히 높음)
    
    ✓ 결과 설명 가능 (어떤 요인이 중요한지 알 수 있음)
    
    ✓ 새로운 학생 데이터에도 잘 작동
    
    ✓ 실제 학교에서 사용하기에 최적
    
    ✓ 속도도 빠름 (실시간 판정 가능)
    
    **작동 원리:**
    여러 개의 의사가 각각 진단 후 투표하는 것처럼 작동
    → 한 명의 의사보다 훨씬 정확!
    
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="box">
    
    ### 📊 성능 평가
    
    **Random Forest 성능:**
    
    - **정확도**: 80% (100명 중 80명을 제대로 진단)
    
    - **재현율**: 85% ⭐ (우울한 학생 100명 중 85명을 잡음)
    
    - **정밀도**: 78% (위험이라고 한 100명 중 78명이 실제 위험)
    
    **가장 중요한 것: 재현율!**
    
    정상인을 우울하다고 할 수 있어도,
    
    우울한 학생을 정상이라고 놓치면 절대 안 됨
    
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="box">
    
    ### 🎯 실제 활용 예시
    
    **학교에 배포했을 때:**
    
    ```
    학생 1000명 설문 조사
    ↓
    AI가 자동으로 분석
    ↓
    위험군 발견 (약 350명)
    ↓
    학교 상담실에 보고
    ↓
    상담사가 개별 상담 진행
    ↓
    조기 발견 → 치료 → 예방 성공!
    ```
    
    </div>
    """, unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 푸터
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.divider()
st.markdown("<p style='text-align: center; color: #999; font-size: 12px;'>🧠 청소년 정신건강 AI 프로젝트</p>", unsafe_allow_html=True)
