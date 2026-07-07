import pandas as pd
import numpy as np

# 1. 데이터 로드 (청소년 정신 건강 데이터 원장)
df_raw = pd.read_csv("Teen_Mental_Health_Dataset.csv")
df = df_raw.copy()

# 2. 변수 타입별 결측치(NaN) 자동 탐색 및 정제 수행
numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
categorical_features = df.select_dtypes(exclude=['int64', 'float64']).columns

# [수치형 변수] -> 결측치를 해당 변수의 '평균값(Mean)'으로 대체
if len(numeric_features) > 0:
    df[numeric_features] = df[numeric_features].fillna(df[numeric_features].mean())

# [범주형 변수] -> 결측치를 해당 변수의 '최빈값(Mode)'으로 대체
if len(categorical_features) > 0:
    for cat_col in categorical_features:
        if not df[cat_col].mode().empty:
            df[cat_col] = df[cat_col].fillna(df[cat_col].mode()[0])
        else:
            df[cat_col] = df[cat_col].fillna("Unknown")

# 3. IQR(사분위수 범위) 기반 이상치(Outlier) 탐색 및 정제 수행
# 데이터 손실을 막기 위해 행을 '삭제'하지 않고, '정상 범위 데이터의 평균'으로 치환
iqr_multiplier = 1.5  # 발표 표준 임계치

for num_col in numeric_features:
    q1 = df[num_col].quantile(0.25)  # 제 1사분위수 (25%)
    q3 = df[num_col].quantile(0.75)  # 제 3사분위수 (75%)
    iqr = q3 - q1                    # 사분위수 범위
    
    # 정상 데이터 통계적 한계 경계 설정
    lower_limit = q1 - (iqr_multiplier * iqr)
    upper_limit = q3 + (iqr_multiplier * iqr)
    
    # 경계를 벗어나는 극단 이상치 조건 마스킹
    outlier_condition = (df[num_col] < lower_limit) | (df[num_col] > upper_limit)
    
    if outlier_condition.sum() > 0:
        # 이상치를 제외한 '정상 데이터들만의 순수 평균값' 계산
        pure_mean = df.loc[~outlier_condition, num_col].mean()
        # 이상치 위치에 순수 평균값 주입 (정제 완료)
        df.loc[outlier_condition, num_col] = pure_mean

# 4. 전처리 전/후 DataFrame 최종 비교 검증용 테이블 생성
null_audit_table = pd.DataFrame({
    "정제 전 결측치 (Original)": df_raw.isnull().sum(),
    "정제 후 결측치 (Cleaned)": df.isnull().sum(),
    "정제 수행 수량 (Cleared)": df_raw.isnull().sum() - df.isnull().sum()
})

print("=== 결측치 정제 수행 진단 결과 ===")
print(null_audit_table)
