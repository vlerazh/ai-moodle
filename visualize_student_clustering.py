import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import sys

try:
    student_data_scaled = pd.read_csv('data/processed_student_data.csv')
    print("[INFO] Data successfully loaded from 'data/processed_student_data.csv'.")
except FileNotFoundError:
    print("[ERROR] The file 'data/processed_student_data.csv' was not found. Please ensure the path is correct.")
    sys.exit(1)

if student_data_scaled.isnull().values.any():
    print("[ERROR] The data contains missing values (NaN). Check the data preprocessing.")
    print(student_data_scaled.isnull().sum())
    sys.exit(1)
else:
    print("[INFO] No missing values found in the data.")

if not all(student_data_scaled.dtypes.apply(lambda x: pd.api.types.is_numeric_dtype(x))):
    print("[ERROR] The data contains non-numeric columns. PCA requires only numeric data.")
    print(student_data_scaled.dtypes)
    sys.exit(1)
else:
    print("[INFO] All columns are numeric. Ready for PCA.")

try:
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(student_data_scaled)
    print("[INFO] PCA applied successfully.")
except Exception as e:
    print(f"[ERROR] Error during PCA application: {e}")
    sys.exit(1)

pca_df = pd.DataFrame(data=principal_components, columns=['PCA1', 'PCA2'])

plt.figure(figsize=(8, 6))
plt.scatter(pca_df['PCA1'], pca_df['PCA2'], c='blue', edgecolor='k', alpha=0.7)
plt.title('PCA of Student Data')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.grid(True)
plt.show()
print("[INFO] Visualization completed successfully.")
