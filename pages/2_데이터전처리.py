import streamlit as st
import pandas as pd
import numpy as np
import os

# --- 1. 앱 페이지 설정 ---
st.set_page_config(
    page_title="Data Clean Pro App",
    page_icon="🧼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. 전문 대시보드용 CSS 스타일 기법 apply ---
st.markdown("""
    <style>
        /* 메인 백그라운드 및 폰트 세팅 */
        .reportview-container { background: #F8FAFC; }
        
        /* 앱 헤더 스타일 */
        .app-header { 
            padding: 20px; 
            background: linear-gradient(135deg, #1E3A8A, #3B82F6); 
            color: white; 
            border-radius: 10px; 
            margin-bottom: 25px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        .app-title { font-size: 26px; font-weight: bold; margin: 0; }
        .app-subtitle { font-size: 13px; opacity: 0.9; margin-top: 5px; }
        
        /* 섹션 카드 스타일 */
        .status-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border: 1px solid #E2E8F0;
            margin-bottom: 20px;
        }
        .card-title { font-size: 16px; font-weight: bold; color: #1E3A8A; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- App 상단 헤더 ---
st.markdown("""
    <div class="app-header">
        <div class="app-title">🧼 데이터 정제 및 전/후 비교 시스템 (Data Clean Pro)</div>
        <div class="app-subtitle">결측치와 IQR 기반 이상치를 실시간 탐색하고 정제 전/후의 데이터프레임을 완벽하게 비교 분석합니다.</div>
    </div>
""", unsafe_allow_html=True)

# --- 3. 사이드바 컨트롤러 (앱 느낌 물씬 나도록 구성) ---
with st.sidebar:
    st.markdown("### 🎛️ 애플리케이션 제어")
    st.info("이 앱은 업로드된 데이터셋의 무결성을 검증하고 원클릭으로 결측치 및 이상치를 보정합니다.")
    
    st.markdown("---")
    st.markdown("**정제 프로세스 기준**")
    st.write("- **수치형 결측치:** 컬럼 평균값(Mean) 대체")
    st.write("- **범주형 결측치:** 컬럼 최빈값(Mode) 대체")
    st.write("- **이상치 탐지:** IQR (Q1 - 1.5*IQR ~ Q3 + 1.5*IQR)")
    st.write("- **이상치 처리:** 정상 범위 내 평균값 대체")

# --- 4. 데이터 로드 및 데모 데이터 안전장치 ---
data_path = "Teen_Mental_Health_Dataset.csv"

if os.path.exists(data_path):
    df_raw = pd.read_csv(data_path)
else:
    # 파일이 없는 비상 상황을 위한 Mock 데이터셋 생성 (에러 방지용)
    np.random.seed(42)
    n_samples = 150
    mock_data = {
        "daily_social_media_hours": np.random.uniform(1, 8, n_samples),
        "stress_level": np.random.randint(1, 10, n_samples).astype(float),
        "gender": np.random.choice(["Male", "Female"], n_samples),
        "depression_label": np.random.choice(["Mild", "Moderate", "Severe"], n_samples)
    }
    df_raw = pd.DataFrame(mock_data)
    
    # 인위적 결측치 & 이상치 주입
    df_raw.loc[np.random.choice(n_samples, 12), "daily_social_media_hours"] = np.nan
    df_raw.loc[np.random.choice(n_samples, 8), "stress_level"] = np.nan
    df_raw.loc[np.random.choice(n_samples, 4), "stress_level"] = 99.0  # 극단적 상한 이상치
    df_raw.loc[np.random.choice(n_samples, 4), "daily_social_media_hours"] = -10.0  # 극단적 하한 이상치
    
    st.sidebar.warning("⚠️ CSV 파일이 없어 데모 데이터로 가동 중입니다.")

# 데이터 카피본 생성
df = df_raw.copy()

# ---------------------------------------------------------
# ⚙️ 핵심 로직 1: 결측치(NaN) 탐색 및 정제 수행
# ---------------------------------------------------------
raw_null_counts = df_raw.isnull().sum()
total_raw_null = raw_null_counts.sum()

replaced_null_count = 0
for col in df.columns:
    null_cnt = df[col].isnull().sum()
    if null_cnt > 0:
        if df[col].dtype in ['int64', 'float64']:
            df[col] = df[col].fillna(df[col].mean())
        else:
            mode_val = df[col].mode()[0] if not df[col].mode().empty else "Unknown"
            df[col] = df[col].fillna(mode_val)
        replaced_null_count += null_cnt

# ---------------------------------------------------------
# ⚙️ 핵심 로직 2: IQR 기반 이상치(Outlier) 탐색 및 정제 수행
# ---------------------------------------------------------
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
replaced_outlier_count = 0

for col in numeric_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
    outlier_cnt = outlier_mask.sum()
    
    if outlier_cnt > 0:
        normal_mean = df.loc[~outlier_mask, col].mean()
        df.loc[outlier_mask, col] = normal_mean
        replaced_outlier_count += outlier_cnt


# ---------------------------------------------------------
# 📊 화면 배치: 현황 스코어보드 (KPI Metrics)
# ---------------------------------------------------------
st.markdown('<div class="card-title">📈 1. 데이터 품질 요약 지표</div>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="전체 데이터 크기", value=f"{df.shape[0]} 행 × {df.shape[1]} 열")
with m2:
    st.metric(label="탐지된 결측치(NaN)", value=f"{total_raw_null} 개", delta="자동 정제 완료")
with m3:
    st.metric(label="탐지된 이상치(IQR 기준)", value=f"{replaced_outlier_count} 개", delta="평균값 대체 완료", delta_color="inverse")
with m4:
    st.metric(label="데이터 정제 상태", value="100% Clean" if df.isnull().sum().sum() == 0 else "미완료")


# ---------------------------------------------------------
# 🔄 화면 배치: 전처리 전/후 DataFrame 완벽 비교 파트
# ---------------------------------------------------------
st.markdown("---")
st.markdown('<div class="card-title">🔄 2. 전처리 전 (Original) vs 전처리 후 (Cleaned) 데이터 비교</div>', unsafe_allow_html=True)

# 탭 구조를 활용한 영역 분할
tab1, tab2, tab3 = st.tabs([
    "📄 원본/정제본 데이터프레임 실시간 비교", 
    "📊 변수별 결측치(NaN) 클렌징 결과", 
    "📈 기술 통계량 변화 분석 (이상치 보정 확인)"
])

# 탭 1: 실제 데이터프레임 양옆으로 띄워서 비교하기
with tab1:
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("<b style='color:#EF4444;'>🚨 [전처리 전] 원본 데이터프레임 (상위 15개 행)</b>", unsafe_allow_html=True)
        st.dataframe(df_raw.head(15), use_container_width=True)
    with col_right:
        st.markdown("<b style='color:#10B981;'>✅ [전처리 후] 정제 완료 데이터프레임 (상위 15개 행)</b>", unsafe_allow_html=True)
        st.dataframe(df.head(15), use_container_width=True)

# 탭 2: 결측치 현황 테이블 비교
with tab2:
    st.markdown("##### 🔍 각 변수(Column)별 결측치 잔존 상태 비교 테이블")
    null_comparison_matrix = pd.DataFrame({
        "전처리 전 결측치 개수 (Original)": df_raw.isnull().sum(),
        "전처리 후 결측치 개수 (Cleaned)": df.isnull().sum()
    })
    st.dataframe(null_comparison_matrix, use_container_width=True)

# 탭 3: 이상치 대체로 인한 수치 통계 변화 확인
with tab3:
    st.markdown("##### 🔍 수치형 변수의 기술 통계 정보 변화량")
    st.caption("이상치가 제거되면서 변수의 최댓값(max), 최솟값(min), 표준편차(std) 등이 정상 범위로 보정된 것을 확인할 수 있습니다.")
    
    if len(numeric_cols) > 0:
        selected_target_col = st.selectbox("통계량 변화를 모니터링할 변수를 선택하세요:", numeric_cols)
        
        statistical_summary = pd.DataFrame({
            "전처리 전 통계량 (Original)": df_raw[selected_target_col].describe(),
            "전처리 후 통계량 (Cleaned)": df[selected_target_col].describe()
        })
        st.dataframe(statistical_summary, use_container_width=True)
    else:
        st.info("데이터셋 내에 분석할 수 있는 수치형 변수가 존재하지 않습니다.")
