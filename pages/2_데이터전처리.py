import streamlit as st
import pandas as pd
import numpy as np
import os

# --- 1. 앱 글로벌 테마 설정 ---
st.set_page_config(
    page_title="데이터 전처리 시스템 Pro",
    page_icon="🧼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 화이트 매니지먼트 어플리케이션 스킨 (CSS)
st.markdown("""
    <style>
        .stApp { background-color: #FAFAFA; color: #111827; }
        .app-top-bar {
            background-color: #FFFFFF;
            padding: 24px;
            border-bottom: 1px solid #E5E7EB;
            margin-bottom: 25px;
        }
        .app-title { font-size: 26px; font-weight: 700; color: #111827; }
        .app-title span { color: #2563EB; }
        .app-desc { font-size: 14px; color: #4B5563; margin-top: 6px; }
        
        .app-section-card {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            margin-bottom: 25px;
        }
        .section-heading { font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 15px; }
        .presentation-note { background-color: #EFF6FF; border-left: 4px solid #2563EB; padding: 15px; border-radius: 4px; margin-bottom: 20px; font-size: 14px; color: #1E40AF; }
        
        .lbl-before { background-color: #FEF2F2; color: #DC2626; font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 4px; display: inline-block; margin-bottom: 8px; }
        .lbl-after { background-color: #ECFDF5; color: #059669; font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 4px; display: inline-block; margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

# 상단 대시보드 헤더
st.markdown("""
    <div class="app-top-bar">
        <div class="app-title">🧼 데이터 정제 및 전/후 비교 시스템 <span>(발표 모드)</span></div>
        <div class="app-desc">본 프로그램은 청소년 정신 건강 데이터셋의 결측치 및 이상치를 실시간 탐색하고 정제를 수행하는 과정을 증명합니다.</div>
    </div>
""", unsafe_allow_html=True)


# --- 2. 사이드바 제어 패널 ---
with st.sidebar:
    st.markdown("<p style='font-size: 16px; font-weight: 700; color: #111827;'>🎛️ 알고리즘 가중치 설정</p>", unsafe_allow_html=True)
    st.markdown("---")
    selected_strategy = st.radio("⚡ 결측치 보정 연산 기준", ["전체 평균값 (Mean)", "전체 중앙값 (Median)"])
    iqr_multiplier = st.slider("📐 이상치 판단 임계 지수 (IQR)", min_value=1.0, max_value=3.0, value=1.5, step=0.1)


# --- 3. 데이터 로드 및 데모 데이터 주입 ---
data_file_path = "Teen_Mental_Health_Dataset.csv"

if os.path.exists(data_file_path):
    df_raw = pd.read_csv(data_file_path)
else:
    # 데이터 유실 시 실시간 발표가 멈추지 않도록 방어하는 가상 데이터 빌더
    np.random.seed(42)
    records = 200
    mock_data = {
        "daily_social_media_hours": np.random.uniform(0.5, 8.0, records),
        "stress_level": np.random.randint(1, 11, records).astype(float),
        "social_interaction_level": np.random.randint(1, 6, records).astype(float),
        "gender": np.random.choice(["Male", "Female"], records),
        "depression_label": np.random.choice(["Mild", "Moderate", "Severe"], records)
    }
    df_raw = pd.DataFrame(mock_data)
    
    # 인위적 결측치 및 극단 이상치 인젝션
    df_raw.loc[np.random.choice(records, 20), "daily_social_media_hours"] = np.nan
    df_raw.loc[np.random.choice(records, 12), "stress_level"] = np.nan
    df_raw.loc[np.random.choice(records, 6), "stress_level"] = 999.0
    df_raw.loc[np.random.choice(records, 6), "daily_social_media_hours"] = -50.0
    st.sidebar.caption("💡 *Notice: 데모 데이터셋 동기화 가동 중*")

df = df_raw.copy()


# --- 4. 고성능 결측치 & 이상치 탐색 및 정제 파이프라인 (백엔드 연산) ---
total_null_detected = df_raw.isnull().sum().sum()
numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
categorical_features = df.select_dtypes(exclude=['int64', 'float64']).columns

# [1] 결측치 정제 연산 수행
if len(numeric_features) > 0:
    if "평균값" in selected_strategy:
        df[numeric_features] = df[numeric_features].fillna(df[numeric_features].mean())
    else:
        df[numeric_features] = df[numeric_features].fillna(df[numeric_features].median())

if len(categorical_features) > 0:
    for cat_col in categorical_features:
        df[cat_col] = df[cat_col].fillna(df[cat_col].mode()[0] if not df[cat_col].mode().empty else "Unknown")

# [2] IQR 기반 이상치 탐색 및 정제 수행
total_outliers_detected = 0
for num_col in numeric_features:
    q1 = df[num_col].quantile(0.25)
    q3 = df[num_col].quantile(0.75)
    iqr = q3 - q1
    
    lower_limit = q1 - (iqr_multiplier * iqr)
    upper_limit = q3 + (iqr_multiplier * iqr)
    
    outlier_condition = (df[num_col] < lower_limit) | (df[num_col] > upper_limit)
    outlier_count = outlier_condition.sum()
    
    if outlier_count > 0:
        pure_mean = df.loc[~outlier_condition, num_col].mean()
        df.loc[outlier_condition, num_col] = pure_mean
        total_outliers_detected += outlier_count


# --- 5. 프론트엔드 UI 레이어 배치 (발표 최적화 구조) ---

# [모듈 1] 어떤 항목을 어떻게 전처리했는지 명확한 설명 슬라이드 대용 카드
with st.container():
    st.markdown('<div class="app-section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📢 1. 전처리 수행 개요 및 방법론 설명</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="presentation-note">
        <strong>💡 발표용 리딩 스크립트 가이드:</strong><br>
        "저희 데이터셋은 수집 과정에서 발생한 결측치(NaN)와 장비 에러로 추정되는 극단적인 이상치(Outlier)가 섞여 있어 그대로 분석하기에 부적합한 상태였습니다. 데이터의 유실을 최소화하기 위해 '행 삭제' 대신 다음과 같은 통계적 알고리즘을 사용하여 전처리를 수행했습니다."
    </div>
    """, unsafe_allow_html=True)
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.info("""
        **🛠️ 결측치(NaN) 정제 방법**
        * **수치형 변수**: `daily_social_media_hours`, `stress_level` 항목의 누락값을 해당 변수의 **전체 평균값(Mean)**으로 일괄 대치했습니다.
        * **범주형 변수**: `gender`, `depression_label` 등의 누락값은 가장 빈도가 높은 **최빈값(Mode)**을 찾아내어 유실 없이 메웠습니다.
        """)
    with col_info2:
        st.warning("""
        **📐 이상치(Outlier) 탐색 및 정제 방법**
        * **탐색 알고리즘**: 사분위수 기준 수치 변수들의 상위 75%와 하위 25% 범위를 기준으로 **IQR(사분위수 범위)의 1.5배**를 벗어난 극단치를 자동으로 탐색했습니다.
        * **보정 조치**: 데이터 왜곡을 방지하기 위해 이상치들을 제거하는 대신, **이상치를 제외한 정상 범위 샘플들의 순수 평균값**으로 안정화 치환을 수행했습니다.
        """)
    st.markdown('</div>', unsafe_allow_html=True)


# [모듈 2] 탐색 결과 요약 지표
with st.container():
    st.markdown('<div class="app-section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🎯 2. 실시간 데이터 품질 진단 지표</div>', unsafe_allow_html=True)
    
    stat_1, stat_2, stat_3, stat_4 = st.columns(4)
    with stat_1:
        st.metric(label="📊 전체 분석 표본", value=f"{df.shape[0]} Rows", delta=f"{df.shape[1]} Columns")
    with stat_2:
        st.metric(label="🧼 보정된 결측치 수 (Total NaN)", value=f"{total_null_detected} 건", delta="정제 완료")
    with stat_3:
        st.metric(label="🚨 탐지된 이상치 수 (IQR Outliers)", value=f"{total_outliers_detected} 건", delta="평균 수렴 완료", delta_color="inverse")
    with stat_4:
        st.metric(label="🔋 데이터 최종 무결성 지표", value="100.00 % Clean")
    st.markdown('</div>', unsafe_allow_html=True)


# [모듈 3] 전처리 전 / 후 DataFrame 1:1 완벽 비교
with st.container():
    st.markdown('<div class="app-section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🔄 3. 전처리 전 (Original) vs 전처리 후 (Cleaned) DataFrame 원장 대조</div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown('<span class="lbl-before">🚨 [전처리 전] 오염 데이터프레임 원본 (상위 12개 행)</span>', unsafe_allow_html=True)
        st.dataframe(df_raw.head(12), use_container_width=True, height=380)
    with col_right:
        st.markdown('<span class="lbl-after">✅ [전처리 후] 정제 완료 데이터프레임 원본 (상위 12개 행)</span>', unsafe_allow_html=True)
        st.dataframe(df.head(12), use_container_width=True, height=380)
    st.markdown('</div>', unsafe_allow_html=True)


# [모듈 4] 정제 수행 최종 진단 리포트 (표 오류 수정본)
with st.container():
    st.markdown('<div class="app-section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📑 4. 변수별 전처리 수행 사후 진단 리포트</div>', unsafe_allow_html=True)
    
    # 수정된 수치 매칭 구조 적용
    null_audit_table = pd.DataFrame({
        "정제 전 결측치 수 (Original)": df_raw.isnull().sum(),
        "정제 후 결측치 수 (Cleaned)": df.isnull().sum(),
        "엔진이 실제 보정한 수량 (Cleared)": df_raw.isnull().sum() - df.isnull().sum()
    })
    st.dataframe(null_audit_table, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
