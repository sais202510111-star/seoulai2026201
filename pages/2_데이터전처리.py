import streamlit as st
import pandas as pd
import numpy as np
import os

# ==========================================
# 1. 글로벌 화이트 앱 테마 정의
# ==========================================
st.set_page_config(
    page_title="DataClean Engine Pro",
    page_icon="🧼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 깨끗하고 직관적인 화이트 모드 어플리케이션 스킨 (CSS)
st.markdown("""
    <style>
        /* 기본 배경 및 텍스트 톤앤매너 */
        .stApp { background-color: #FAFAFA; color: #111827; }
        
        /* 플랫하고 모던한 상단 바 */
        .app-top-bar {
            background-color: #FFFFFF;
            padding: 20px 24px;
            border-bottom: 1px solid #E5E7EB;
            margin-bottom: 25px;
        }
        .app-title { font-size: 24px; font-weight: 700; color: #111827; letter-spacing: -0.5px; }
        .app-title span { color: #2563EB; }
        .app-desc { font-size: 13px; color: #6B7280; margin-top: 4px; }
        
        /* 구조화된 화이트 웹앱 카드 */
        .app-section-card {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            margin-bottom: 25px;
        }
        .section-badge { display: inline-block; background-color: #F3F4F6; color: #374151; font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 6px; margin-bottom: 10px; text-transform: uppercase; }
        .section-heading { font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 15px; }
        
        /* 대조 라벨 프리셋 */
        .lbl-before { background-color: #FEF2F2; color: #DC2626; font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 4px; display: inline-block; margin-bottom: 8px; }
        .lbl-after { background-color: #ECFDF5; color: #059669; font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 4px; display: inline-block; margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- [상단 대시보드 헤더 바] ---
st.markdown("""
    <div class="app-top-bar">
        <div class="app-title">🧼 DataClean <span>Engine Pro</span></div>
        <div class="app-desc">결측치 및 이상치 탐색부터 자동 정제, 정제 전/후 데이터프레임 구조의 원장 대조 검증을 수행합니다.</div>
    </div>
""", unsafe_allow_html=True)


# ==========================================
# 2. 실시간 컨트롤러 패널 (사이드바)
# ==========================================
with st.sidebar:
    st.markdown("<p style='font-size: 16px; font-weight: 700; color: #111827;'>🎛️ 정제 옵션 패널</p>", unsafe_allow_html=True)
    st.caption("파이프라인 연산 기준을 정의합니다.")
    st.markdown("---")
    
    selected_strategy = st.radio("⚡ 수치형 결측치 보정 기준", ["전체 평균값 (Mean)", "전체 중앙값 (Median)"])
    iqr_multiplier = st.slider("📐 이상치 탐색 임계 지수 (IQR)", min_value=1.0, max_value=3.0, value=1.5, step=0.1)
    
    st.markdown("---")
    st.caption("본 프로그램은 입력 데이터 원장을 실시간 추적 연산하여 데이터 무결성을 검증합니다.")


# ==========================================
# 3. 데이터 인젝션 허브 (유실 방지용 데모 셋 탑재)
# ==========================================
data_file_path = "Teen_Mental_Health_Dataset.csv"

if os.path.exists(data_file_path):
    df_raw = pd.read_csv(data_file_path)
else:
    # 깃허브 배포 시 에러 방지용으로 자동 가동되는 가상 청소년 정신건강 프로파일 데이터셋
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
    
    # [과제 정렬] 인위적 품질 저하 요소 주입 (결측치 및 극단 이상치)
    df_raw.loc[np.random.choice(records, 20), "daily_social_media_hours"] = np.nan
    df_raw.loc[np.random.choice(records, 12), "stress_level"] = np.nan
    df_raw.loc[np.random.choice(records, 6), "stress_level"] = 999.0  # 아웃라이어
    df_raw.loc[np.random.choice(records, 6), "daily_social_media_hours"] = -50.0  # 아웃라이어
    st.sidebar.caption("💡 *Notice: 시뮬레이션 데이터 샌드박스 가동 중*")

# 정제 처리를 위한 동기화 원장 생성
df = df_raw.copy()


# ==========================================
# ⚙️ 4. 고성능 결측치 & 이상치 탐색 및 정제 파이프라인 (백엔드)
# ==========================================
# [1] 원본 결측치 탐색
total_null_detected = df_raw.isnull().sum().sum()
numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
categorical_features = df.select_dtypes(exclude=['int64', 'float64']).columns

# [2] 결측치 데이터 정제 수행 (벡터화 기법 가속)
if len(numeric_features) > 0:
    if "평균값" in selected_strategy:
        df[numeric_features] = df[numeric_features].fillna(df[numeric_features].mean())
    else:
        df[numeric_features] = df[numeric_features].fillna(df[numeric_features].median())

if len(categorical_features) > 0:
    for cat_col in categorical_features:
        df[cat_col] = df[cat_col].fillna(df[cat_col].mode()[0] if not df[cat_col].mode().empty else "Unknown")

# [3] IQR 기반 이상치 탐색 및 정제 수행
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
        # 정상 범위 데이터의 평균값으로 정제 치환
        pure_mean = df.loc[~outlier_condition, num_col].mean()
        df.loc[outlier_condition, num_col] = pure_mean
        total_outliers_detected += outlier_count


# ==========================================
# 📱 5. 어플리케이션 인터랙티브 UI 레이어 (프론트엔드)
# ==========================================

# 모듈 1: 실시간 데이터 품질 분석 모니터링 현황판
with st.container():
    st.markdown('<div class="app-section-card">', unsafe_allow_html=True)
    st.markdown('<span class="section-badge">Pipeline Status</span>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🎯 1. 결측치 및 이상치 실시간 탐색 보고</div>', unsafe_allow_html=True)
    
    stat_1, stat_2, stat_3, stat_4 = st.columns(4)
    with stat_1:
        st.metric(label="📊 총 분석 대상 구조", value=f"{df.shape[0]} Rows", delta=f"{df.shape[1]} Columns")
    with stat_2:
        st.metric(label="🧼 발견 및 정제된 결측치 (NaN)", value=f"{total_null_detected} 건", delta="보정 즉시 반영")
    with stat_3:
        st.metric(label="🚨 탐지 및 격리된 이상치 (IQR)", value=f"{total_outliers_detected} 건", delta="대체 완료", delta_color="inverse")
    with stat_4:
        st.metric(label="🔋 최종 무결성 상태", value="100 % Clean" if df.isnull().sum().sum() == 0 else "연산 오류")
    st.markdown('</div>', unsafe_allow_html=True)


# 모듈 2: 전처리 전 / 후 DataFrame 원장 1:1 전면 비교 (핵심 주문 기능)
with st.container():
    st.markdown('<div class="app-section-card">', unsafe_allow_html=True)
    st.markdown('<span class="section-badge">Data Integrity Split View</span>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🔄 2. 전처리 전 (Original) vs 전처리 후 (Cleaned) DataFrame 원장 비교</div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown('<span class="lbl-before">🚨 [전처리 전] 수정 전 원본 데이터프레임 스냅샷</span>', unsafe_allow_html=True)
        st.dataframe(df_raw.head(15), use_container_width=True, height=450)
    with col_right:
        st.markdown('<span class="lbl-after">✅ [전처리 후] 엔진 정제 완료 데이터프레임 원장</span>', unsafe_allow_html=True)
        st.dataframe(df.head(15), use_container_width=True, height=450)
    st.markdown('</div>', unsafe_allow_html=True)


# 모듈 3: 디테일 분석 검증 세부 보고서 탭 구조
with st.container():
    st.markdown('<div class="app-section-card">', unsafe_allow_html=True)
    st.markdown('<span class="section-badge">Analytical Report</span>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📑 3. 데이터 정제 수행 결과 및 통계량 검증 보고서</div>', unsafe_allow_html=True)
    
    report_tab1, report_tab2 = st.tabs([
        "📋 각 변수(Column)별 결측치 소실율 최종 진단표",
        "📊 이상치 치환에 따른 기초 기술 통계량 추이 대조"
    ])
    
    with report_tab1:
        st.markdown("<p style='font-size:13px; color:#4B5563; margin-bottom:15px;'>각 변수명별 누락 데이터가 완벽히 메워졌는지 수치로 검증하는 매트릭스입니다.</p>", unsafe_allow_html=True)
        null_audit_table = pd.DataFrame({
            "정제 전 결측치 수 (Original)": df_raw.isnull().sum(),
            "정제 후 결측치 수 (Cleaned)": df.isnull().sum(),
            "보정 가동 수량": df_raw.isnull().sum() - df.isnull().sum()
        })
        st.dataframe(null_audit_table.T, use_container_width=True)
        
    with report_tab2:
        st.markdown("<p style='font-size:13px; color:#4B5563; margin-bottom:15px;'>이상치 범위 이탈자가 정상 범위 평균으로 치환되면서 보정된 컬럼별 기술 통계 지표입니다.</p>", unsafe_allow_html=True)
        if len(numeric_features) > 0:
            target_metric_col = st.selectbox("실시간 모니터링할 변수(컬럼) 선택:", numeric_features)
            
            summary_audit_df = pd.DataFrame({
                "정제 전 기초통계량 (Original)": df_raw[target_metric_col].describe(),
                "정제 후 기초통계량 (Cleaned)": df[target_metric_col].describe()
            })
            st.dataframe(summary_audit_df.style.format("{:.3f}"), use_container_width=True)
        else:
            st.info("비교 대상 수치형 인프라가 부재합니다.")
            
    st.markdown('</div>', unsafe_allow_html=True)
