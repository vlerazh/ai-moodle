import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import seaborn as sns
import matplotlib.pyplot as plt

student_df = pd.read_csv('data/preprocessed_student_data.csv')

X = student_df.drop(columns=['Cluster'])
y = student_df['Cluster']

X = X.select_dtypes(include=['float64', 'int64'])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

student_df['Predicted Cluster'] = model.predict(X)

print(student_df['Predicted Cluster'].value_counts())

numerical_columns = student_df.select_dtypes(
    include=['float64', 'int64']).columns

group_summary = student_df[numerical_columns].groupby(
    student_df['Predicted Cluster']).mean()
print(group_summary)

group_names = {
    0: 'Grupi i Studentëve të Sociologjisë',
    1: 'Grupi i Studentëve të Shkencave',
    2: 'Grupi i Studentëve të Biologjisë',
    3: 'Grupi i Studentëve Aktivë dhe të Rinj'
}

student_df['Cluster Name'] = student_df['Predicted Cluster'].map(group_names)
print(student_df[['Predicted Cluster', 'Cluster Name']].drop_duplicates())

plt.figure(figsize=(10, 6))
sns.countplot(x='Cluster Name', data=student_df, palette='viridis')
plt.title('Shpërndarja e Grupeve të Parashikuara')
plt.xlabel('Emri i Grupit')
plt.ylabel('Numri i Studentëve')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

student_df.to_csv('data/student_clustering_supervised.csv', index=False)
