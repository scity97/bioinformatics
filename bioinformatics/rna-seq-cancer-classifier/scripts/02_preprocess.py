import pandas as pd
import numpy as np

# 파일 경로
counts_path = "./data/merged_counts.csv"
meta_path = "./data/metadata.tsv"  # 필요시 파일명에 맞게 수정
output_path = "./data/preprocessed_data.csv"

# 1. count 데이터 불러오기
counts_df = pd.read_csv(counts_path, index_col=0)

# 2. 로그 변환 (log2(count + 1))
log_df = np.log2(counts_df + 1)

# 3. 저발현 유전자 필터링 (모든 샘플 평균 < 1 제거)
filtered_df = log_df[log_df.mean(axis=1) > 0]

# 4. 메타데이터 불러오기
meta_df = pd.read_csv(meta_path, sep='\t')  # .csv면 sep=','로

# 5. 샘플 ID 기준으로 라벨 붙이기
# 전제: metadata에 'sample_id', 'label' (0=normal, 1=tumor) 컬럼이 있어야 함
sample_labels = meta_df.set_index("sample_id")["label"]

# 6. X, y로 분리해서 저장 (선택)
filtered_df = filtered_df.T  # 샘플이 행, 유전자가 열

# 샘플 순서 맞추기
filtered_df["label"] = filtered_df.index.map(sample_labels)

# 라벨 없는 샘플 제거
filtered_df.dropna(subset=["label"], inplace=True)

# 결과 저장
filtered_df.to_csv(output_path)
print(f"✅ 전처리 완료! 저장 위치: {output_path}")
print("📊 샘플 개수:", filtered_df.shape[0])
print("✅ 포함된 샘플 목록:\n", filtered_df.index.tolist())
