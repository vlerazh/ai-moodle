import pandas as pd
from sklearn.preprocessing import StandardScaler

student_data = pd.read_csv('data/mock_student_dataset.csv')

print("Original Dataset:")
print(student_data.head())

features = ['Age', 'Gender', 'Degree', 'Faculty']
student_data_selected = student_data[features]

student_data_encoded = pd.get_dummies(student_data_selected, drop_first=True)

print("\nEncoded Data:")
print(student_data_encoded.head())

scaler = StandardScaler()

student_data_scaled = scaler.fit_transform(student_data_encoded)

print("\nScaled Data (First 5 rows):")
print(student_data_scaled[:5])

processed_data = pd.DataFrame(
    student_data_scaled, columns=student_data_encoded.columns)

processed_data.to_csv('data/processed_student_data.csv', index=False)

print("\nData preprocessing complete. Processed data saved to 'data/processed_student_data.csv'.")
