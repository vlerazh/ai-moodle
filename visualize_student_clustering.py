import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

student_data = pd.read_csv('data/mock_student_dataset.csv')

features = ['Age', 'Degree', 'Faculty', 'Gender']

student_data_encoded = pd.get_dummies(student_data[features], drop_first=True)

scaler = StandardScaler()
student_data_scaled = scaler.fit_transform(student_data_encoded)

pca = PCA(n_components=2)
principal_components = pca.fit_transform(student_data_scaled)

pca_df = pd.DataFrame(data=principal_components, columns=['PCA1', 'PCA2'])

plt.figure(figsize=(8, 6))
plt.scatter(pca_df['PCA1'], pca_df['PCA2'], c='blue', edgecolor='k', alpha=0.7)
plt.title('PCA of Student Data')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.show()
