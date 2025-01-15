import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report


student_df = pd.read_csv('data/mock_student_dataset.csv')
book_df = pd.read_csv('data/mock_e_library_dataset.csv')

# Merge student_df and book_df on the 'E-Library Book ID' column
merged_df = pd.merge(student_df, book_df, left_on='E-Library Book ID', right_on='Book ID', how='left')

# Drop 'Description' and 'Name' columns as they are not needed for clustering or prediction
merged_df = merged_df.drop(columns=['Name', 'Description'])

# Exploding the 'Subjects' column (convert string list to actual list)
merged_df['Subjects'] = merged_df['Subjects'].apply(eval)  # Convert string lists to actual lists

# Exploding the 'Subjects' column into multiple rows per student
exploded_df = merged_df.explode('Subjects').reset_index(drop=True)

# Initialize LabelEncoders for categorical columns
degree_encoder = LabelEncoder()
faculty_encoder = LabelEncoder()
gender_encoder = LabelEncoder()
status_encoder = LabelEncoder()

# Apply LabelEncoding to the categorical variables
exploded_df['Degree'] = degree_encoder.fit_transform(exploded_df['Degree'])
exploded_df['Faculty'] = faculty_encoder.fit_transform(exploded_df['Faculty'])
exploded_df['Gender'] = gender_encoder.fit_transform(exploded_df['Gender'])
exploded_df['Status'] = status_encoder.fit_transform(exploded_df['Status'])

# Convert 'Category' into a numerical format (Label encoding)
label_encoder = LabelEncoder()
exploded_df['Category'] = label_encoder.fit_transform(exploded_df['Category'])

# Focus on relevant features for prediction (Faculty, Degree, Gender, Status)
X = exploded_df[['Degree', 'Faculty', 'Gender', 'Status']].copy()
y = exploded_df['Category']

# Train-test split (80-20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the KNeighborsClassifier with hyperparameter tuning
param_grid = {
    'n_neighbors': [3, 5, 7, 9, 11],
    'weights': ['uniform', 'distance'],
    'metric': ['minkowski', 'euclidean', 'manhattan']
}

cv = KFold(n_splits=5, shuffle=True, random_state=42)
grid_search = GridSearchCV(estimator=KNeighborsClassifier(), param_grid=param_grid, cv=cv, scoring='accuracy', n_jobs=-1)

# Train the model on the training data
grid_search.fit(X_train, y_train)

# Get the best model from the grid search
best_model = grid_search.best_estimator_