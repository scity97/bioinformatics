import os
import pandas as pd

# 데이터 폴더 경로 설정
data_dir = "./data"
output_path = "./data/merged_counts.csv"

# count 파일 리스트 불러오기
count_files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]

# 병합을 위한 빈 데이터 프레임
merged_df = None

for filename in count_files:
    sample_id = filename.replace(".txt","")
    filepath = os.path.join(data_dir, filename)

    # 파일 불러오기
    df = pd.read_csv(filepath, sep='\t', header=None, names=["Gene", sample_id])

    # 유전자 이름을 인덱스로 설정
    df.set_index("Gene", inplace=True)

    # 첫 번째 파일이면 merged_df에 저장, 아니면 join
    if merged_df is None:
        merged_df = df
    else:
        merged_df = merged_df.join(df, how="outer")

# 결측치(NaN)는 0으로 대체
merged_df.fillna(0, inplace=True)

# 결과 저장
merged_df.to_csv(output_path)
print(f"병합 완료! 저장 경로: {output_path}")