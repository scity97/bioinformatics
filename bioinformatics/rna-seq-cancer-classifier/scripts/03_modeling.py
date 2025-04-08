import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 데이터 불러오기
data_path = "./data/preprocessed_data.csv"
df = pd.read_csv(data_path, index_col=0)

# 2. X, y 분리
X = df.drop(columns=["label"])
y = df["label"]

# 3. 학습/테스트 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. 예측 및 평가
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ 정확도: {acc:.2f}")

# 6. confusion matrix 시각화
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(4, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["Normal", "Cancer"], yticklabels=["Normal", "Cancer"])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("./figures/confusion_matrix.png")
plt.show()

# 7. 중요 유전자 상위 20개 시각화
importances = pd.Series(model.feature_importances_, index=X.columns)
top_genes = importances.sort_values(ascending=False).head(20)

plt.figure(figsize=(6, 8))
sns.barplot(x=top_genes.values, y=top_genes.index)
plt.title("Top 20 Important Genes")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.savefig("./figures/top_genes.png")
plt.show()
