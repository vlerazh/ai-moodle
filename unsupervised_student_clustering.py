import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

student_data = pd.read_csv('data/processed_student_data.csv')

print("Original Dataset:")
print(student_data.head())

student_data_selected = student_data.select_dtypes(
    include=['float64', 'int64'])  # Numeric columns only

scaler = StandardScaler()
student_data_scaled = scaler.fit_transform(student_data_selected)

pca = PCA(n_components=2)
student_data_pca = pca.fit_transform(student_data_scaled)

pca_df = pd.DataFrame(student_data_pca, columns=['PCA1', 'PCA2'])

plt.figure(figsize=(8, 6))
sns.scatterplot(x='PCA1', y='PCA2', data=pca_df, s=100)
plt.title('PCA of Student Data')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.show()

kmeans = KMeans(n_clusters=3)
kmeans.fit(student_data_scaled)

pca_df['Cluster'] = kmeans.labels_

plt.figure(figsize=(8, 6))
sns.scatterplot(x='PCA1', y='PCA2', data=pca_df,
                hue='Cluster', palette='viridis', s=100)
plt.title('KMeans Clustering of Student Data')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.show()

pca_df.to_csv('data/student_clustering_results.csv', index=False)

print("\nClustering complete. Results saved to 'data/student_clustering_results.csv'.")
