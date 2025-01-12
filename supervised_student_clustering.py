import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Load the student dataset
student_data = pd.read_csv('data/mock_student_dataset.csv')

print("Initial Data Preview:")
print(student_data.head())

# Add mock 'Study Group' labels if not already in the data
if 'Study Group' not in student_data.columns:
    import numpy as np
    np.random.seed(42)  # For reproducibility
    student_data['Study Group'] = np.random.choice(
        ['Group 1', 'Group 2', 'Group 3'], size=len(student_data))
    print("Mock 'Study Group' column added.")

# Select features and target
features = ['Age', 'Gender', 'Degree', 'Faculty']
X = student_data[features]
y = student_data['Study Group']

# Encode categorical variables
label_encoders = {}
for col in ['Gender', 'Degree', 'Faculty']:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Ensure 'data' directory exists
os.makedirs('data', exist_ok=True)

# Save the scaler for future use in the 'data' folder
joblib.dump(scaler, 'data/scaler.pkl')

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42)

# Train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print("\nModel Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save the trained model in the 'data' folder
joblib.dump(model, 'data/random_forest_model.pkl')

print("\nModel and scaler saved successfully in the 'data' directory.")
