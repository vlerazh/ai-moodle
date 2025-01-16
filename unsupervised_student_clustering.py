import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt

student_df = pd.read_csv('data/preprocessed_student_data.csv')

X = student_df.drop(columns=['Student ID', 'First Name', 'Last Name',
                             'Enrollment Date', 'Subjects', 'E-Library Book ID', 'Cluster'])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=4, n_init='auto', random_state=42)
student_df['Cluster'] = kmeans.fit_predict(X_scaled)

group_names = {
    0: 'Grupi i Studentëve me Performancë të Lartë',
    1: 'Grupi i Studentëve me Nevoja për Mbështetje Akademike',
    2: 'Grupi i Studentëve me Interes të Mesëm',
    3: 'Grupi i Studentëve që Përdorin Shpesh Bibliotekën E-Librari'
}

student_df['Cluster Name'] = student_df['Cluster'].map(group_names)

print(student_df[['Cluster', 'Cluster Name']].drop_duplicates())

plt.figure(figsize=(10, 6))
sns.countplot(x='Cluster Name', data=student_df, palette='viridis')
plt.title('Shpërndarja e Grupeve të Parashikuara')
plt.xlabel('Emri i Grupit')
plt.ylabel('Numri i Studentëve')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

print(student_df['Cluster Name'].value_counts())

student_df.to_csv(
    'data/student_clustering_unsupervised_with_names.csv', index=False)
