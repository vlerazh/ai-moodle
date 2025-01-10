import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV

# Load the datasets
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

# One-hot encoding for categorical columns (Degree, Faculty, Gender, Status)
exploded_df = pd.get_dummies(exploded_df, columns=['Degree', 'Faculty', 'Gender', 'Status'], drop_first=True)

# Convert 'Category' into a numerical format (Label encoding)
label_encoder = LabelEncoder()
exploded_df['Category'] = label_encoder.fit_transform(exploded_df['Category'])

# Inspect the data after encoding
print(exploded_df.head())

# Define the target variable and features
X = exploded_df.drop(columns=['Student ID', 'First Name', 'Last Name', 'E-Library Book ID', 'Book ID', 'Enrollment Date', 'Subjects'])
y = exploded_df['Category']

# Check for any missing values in features
print(X.isnull().sum())

# Train-test split (80-20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training set size:", X_train.shape)
print("Test set size:", X_test.shape)

# Initialize the RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model on the training data
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
print("\nModel Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Get feature importances from the trained model
feature_importances = model.feature_importances_

# Create a DataFrame of feature names and their importance
importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

# Display the most important features
print(importance_df.head())

# # Example new student data (ensure the features match the ones used in training)
# new_student = {
#     'Age': [22],
#     'Degree_BSc in Computer Science': [1],
#     'Degree_MSc in Literature': [0],
#     'Faculty_Faculty of Arts': [0],
#     'Faculty_Faculty of Science': [1],
#     'Gender_Male': [1],
#     'Status_Active': [1]
# }

# new_student_df = pd.DataFrame(new_student)

# # Predict the book category for the new student
# predicted_category = model.predict(new_student_df)
# print("\nPredicted Book Category for New Student:", predicted_category[0])


# new_student = {
#     'Age': [22],
#     'Degree': ['BSc in Computer Science'],
#     'Faculty': ['Faculty of Science'],
#     'Gender': ['Male'],
#     'Status': ['Active'],
#     'E-Library Book ID': ['B021']  # Assuming the new student has this Book ID
# }

# # Convert the new student data into a DataFrame
# new_student_df = pd.DataFrame(new_student)

# # Merge the new student data with the book data
# new_student_df = pd.merge(new_student_df, book_df[['Book ID', 'Category']], left_on='E-Library Book ID', right_on='Book ID', how='left')

# # One-hot encode the categorical features in the same way as the training data
# new_student_df = pd.get_dummies(new_student_df, columns=['Degree', 'Faculty', 'Gender', 'Status'], drop_first=True)

# # Align the columns of the new student data with the training data
# missing_columns = set(X.columns) - set(new_student_df.columns)
# for col in missing_columns:
#     new_student_df[col] = 0

# # Reorder columns to match the training data
# new_student_df = new_student_df[X.columns]

# # Predict the book category for the new student
# predicted_category = model.predict(new_student_df)

# from sklearn.model_selection import GridSearchCV

# # Set up the parameter grid for GridSearch
# param_grid = {
#     'n_estimators': [100, 200],
#     'max_depth': [None, 10, 20],
#     'min_samples_split': [2, 5],
#     'min_samples_leaf': [1, 2]
# }

# # Set up GridSearchCV
# grid_search = GridSearchCV(estimator=RandomForestClassifier(), param_grid=param_grid, cv=5, scoring='accuracy')

# # Fit the grid search
# grid_search.fit(X_train, y_train)

# # Print the best parameters from grid search
# print("\nBest Hyperparameters:", grid_search.best_params_)
