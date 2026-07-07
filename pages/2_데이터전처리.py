import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="청소년 정신 건강 데이터 EDA",
    page_icon="📊",
    layout="wide"
)

# --- 2. 깔끔한 UI를 위한 CSS 스타일 선언 ---
st.markdown("""
    <style>
        .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
        .sub-title { font-size: 14px; color: #4B5563; margin-bottom: 20px; }
        .section-header { font-size: 20px; font-weight: bold; color: #1E3A8A; margin-top: 25px; margin-bottom: 15px; border-bottom: 2px solid #DBEAFE; padding-bottom: 5px; }
        .metric-box { background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 데이터 전처리 및 정제 (EDA) 대시보드</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">결측치 및 이상치 탐색, 데이터 정제 수행, 전처리 전/후 DataFrame을 직관적으로 비교합니다.</div>', unsafe_allow_html=True)

# --- 3. 데이터 로드 및 자동 예제 생성 (GitHub에서 안 터지게 막는 안전장치) ---
data_path = "Teen_Mental_Health_Dataset.csv"

if os.path.exists(data_path):
    df_raw = pd.read_csv(data_path)
else:
    # 💡 파일이 없을 경우 테스트용 가상 데이터를 자동으로 생성하여 에러 방지
    np.random.seed(42)
    n_samples = 200
    mock_data = {
        "daily_social_media_hours": np.random.uniform(1, 8, n_samples),
        "stress_level": np.random.randint(1, 10, n_samples).astype(float),
        "gender": np.random.choice(["Male", "Female"], n_samples),
        "depression_label": np.random.choice(["Mild", "Moderate", "Severe"], n_samples)
    }
    df_raw = pd.DataFrame(mock_data)
    
    # 일부러 결측치(NaN)와 이상치(Outlier) 주입
    df_raw.loc[np.random.choice(n_samples, 15), "daily_social_media_hours"] = np.nan
    df_raw.loc[np.random.choice(n_samples, 10), "stress_level"] = np.nan
    df_raw.loc[np.random.choice(n_samples, 5), "stress_level"] = 99.0  # 상한 이상치
    df_raw.loc[np.random.choice(n_samples, 5), "daily_social_media_hours"] = -5.0  # 하한 이상치
    
    st.info("💡 GitHub 저장소에 'Teen_Mental_Health_Dataset.csv'가 없어서 임시 데모 데이터로 구동 중입니다. 파일 업로드 시 실제 데이터로 변경됩니다.")

# 원본 복사
df = df_raw.copy()

# ---------------------------------------------------------
# ⚙️ [단계 1] 결측치 탐색 및 정제 수행
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
# ⚙️ [단계 2] IQR 기반 이상치 탐색 및 정제 수행
# ---------------------------------------------------------
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
replaced_outlier_count = 0
outlier_summary = {}

for col in numeric_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
    outlier_cnt = outlier_mask.sum()
    outlier_summary[col] = outlier_cnt
    
    if outlier_cnt > 0:
        # 이상치를 제외한 정상 범위의 평균값으로 대체
        normal_mean = df.loc[~outlier_mask, col].mean()
        df.loc[outlier_mask, col] = normal_mean
        replaced_outlier_count += outlier_cnt

# ---------------------------------------------------------
# 📊 [단계 3] 요약 메트릭 및 전/후 DataFrame 비교 출력
# ---------------------------------------------------------
st.markdown('<div class="section-header">🔍 1. 결측치 & 이상치 정제 요약 리포트</div>', unsafe_allow_html=True)

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(label="📊 전체 데이터 크기", value=f"{df.shape[0]} 행 × {df.shape[1]} 열")
with col_m2:
    st.metric(label="🧼 정제된 결측치 (NaN)", value=f"{total_raw_null} 개", delta="처리 완료", delta_color="normal")
with col_m3:
    st.metric(label="🚨 정제된 이상치 (IQR 기준)", value=f"{replaced_outlier_count} 개", delta="평균값 대체 완료", delta_color="inverse")

st.markdown('<div class="section-header">🔄 2. 전처리 전 vs 후 DataFrame 완벽 비교</div>', unsafe_allow_html=True)

# 탭 레이아웃으로 깔끔하게 비교 데이터 배치
tab1, tab2, tab3 = st.tabs(["📄 상위 데이터셋 샘플 비교", "📉 결측치(NaN) 정제 결과", "📈 수치 통계량(이상치 제거 반영) 변화"])

with tab1:
    col_raw, col_clean = st.columns(2)
    with col_raw:
        st.subheader("🚨 전처리 전 (Original)")
        st.dataframe(df_raw.head(10), use_container_width=True)
    with col_clean:
        st.subheader("✅ 전처리 후 (Cleaned)")
        st.dataframe(df.head(10), use_container_width=True)

with tab2:
    st.subheader("💡 변수별 결측치 잔존 수비교")
    null_comp = pd.DataFrame({
        "전처리 전 (Original)": df_raw.isnull().sum(),
        "전처리 후 (Cleaned)": df.isnull().sum()
    })
    st.dataframe(null_comp.T, use_container_width=True)

with tab3:
    st.subheader("💡 주요 수치형 지표 기술통계 비교")
    if len(numeric_cols) > 0:
        selected_col = st.selectbox("통계량 변화를 볼 변수를 고르세요:", numeric_cols)
        stat_comp = pd.DataFrame({
            "전처리 전 (Original)": df_raw[selected_col].describe(),
            "전처리 후 (Cleaned)": df[selected_col].describe()
        })
        st.dataframe(stat_comp, use_container_width=True)
    else:
        st.write("비교할 수치형 변수가 없습니다.")

# ---------------------------------------------------------
# 🎛️ [단계 4] 정제 데이터 시각화 패널
# ---------------------------------------------------------
st.markdown('<div class="section-header">🎛️ 3. 정제 완료 데이터 고급 시각화 패널</div>', unsafe_allow_html=True)

all_columns = df.columns.tolist()
available_colors = ["None"] + [c for c in ["depression_label", "gender"] if c in all_columns]

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    x_axis = st.selectbox("📌 X축 변수", options=all_columns, index=0)
with col_s2:
    y_axis = st.selectbox("📌 Y축 변수", options=all_columns, index=min(1, len(all_columns)-1))
with col_s3:
    color_var = st.selectbox("🎨 범례 그룹화색상", options=available_colors, index=0)

color_target = None if color_var == "None" else color_var
chart_type = st.radio("📊 차트 형태 선택", ["산점도 (Scatter)", "바 차트 (Bar)", "박스 플롯 (Box)", "히스토그램 (Histogram)"], horizontal=True)

try:
    if chart_type == "산점도 (Scatter)":
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_target, title=f"✨ {x_axis}와 {y_axis} 산점도 분석", template="plotly_white")
    elif chart_type == "바 차트 (Bar)":
        df_grouped = df.groupby([x_axis] + ([color_target] if color_target else [])).mean(numeric_only=True).reset_index()
        fig = px.bar(df_grouped, x=x_axis, y=y_axis, color=color_target, title=f"📊 {x_axis}별 {y_axis} 평균 바 차트", barmode="group", template="plotly_white")
    elif chart_type == "박스 플롯 (Box)":
        fig = px.box(df, x=x_axis, y=y_axis, color=color_target, title=f"📦 {x_axis}에 따른 {y_axis} 분포 (이상치 정제 완료)", points="all", template="plotly_white")
    elif chart_type == "히스토그램 (Histogram)":
        fig = px.histogram(df, x=x_axis, color=color_target, title=f"📐 {x_axis} 빈도 히스토그램", barmode="overlay", template="plotly_white")
        
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"⚠️ 선택한 변수 조합으로 해당 차트를 그릴 수 없습니다. 변수 타입을 변경해 주세요. (에러내용: {e})")
