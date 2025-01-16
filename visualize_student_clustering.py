import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

student_df = pd.read_csv('data/student_clustering_unsupervised.csv')

X = student_df[['Age', 'Degree', 'Faculty',
                'Gender', 'Status']]

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

student_df['PCA1'] = X_pca[:, 0]
student_df['PCA2'] = X_pca[:, 1]

plt.figure(figsize=(8, 6))
sns.scatterplot(x='PCA1', y='PCA2', hue='Cluster',
                data=student_df, palette='viridis', s=100)
plt.title('2D Visualization of Student Clusters using PCA')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title='Cluster')
plt.show()
