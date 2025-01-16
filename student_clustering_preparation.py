import pandas as pd
from sklearn.preprocessing import LabelEncoder

student_df = pd.read_csv('data/mock_student_dataset.csv')

degree_encoder = LabelEncoder()
faculty_encoder = LabelEncoder()
gender_encoder = LabelEncoder()
status_encoder = LabelEncoder()

student_df['Degree'] = degree_encoder.fit_transform(student_df['Degree'])
student_df['Faculty'] = faculty_encoder.fit_transform(student_df['Faculty'])
student_df['Gender'] = gender_encoder.fit_transform(student_df['Gender'])
student_df['Status'] = status_encoder.fit_transform(student_df['Status'])

student_df['Cluster'] = student_df['Faculty']

student_df.to_csv('data/preprocessed_student_data.csv', index=False)

print("Data preprocessing complete. Preprocessed data saved to 'data/preprocessed_student_data.csv'.")
