import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# Load the datasets
student_df = pd.read_csv('data/mock_student_dataset.csv')
book_df = pd.read_csv('data/mock_e_library_dataset.csv')

# Merge student_df and book_df on the 'E-Library Book ID' column
merged_df = pd.merge(student_df, book_df, left_on='E-Library Book ID', right_on='Book ID', how='left')

# Drop 'Description' and 'Name' columns as they are not needed for clustering or prediction
# merged_df = merged_df.drop(columns=['Name', 'Description'])

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

# Evaluate the model
y_pred = best_model.predict(X_test)

# Create Streamlit UI
st.title("Student Information and Book Category Prediction")

# Student Input Form
# Define degree-to-faculty mapping based on your provided classes
degree_to_faculty = {
    "BSc in Computer Science": ["Faculty of Science"],
    "BSc in Mathematics": ["Faculty of Science"],
    "BSc in Physics": ["Faculty of Science"],
    "MSc in Literature": ["Faculty of Arts"],
    "MSc in Biology": ["Faculty of Science"],
    "BEng in Mechanical Engineering": ["Faculty of Engineering"],
    "BSc in Chemistry": ["Faculty of Science"],
    "BA in Psychology": ["Faculty of Social Sciences"],
    "MSc in Sociology": ["Faculty of Social Sciences"]
}

degree_options = list(degree_to_faculty.keys())

# Student Input Form
with st.form(key='student_form'):
    st.subheader("Enter Student Details")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    
    # Categorical fields - dynamically populate from dataset
    degree_options = merged_df['Degree'].dropna().unique()
    degree = st.selectbox("Degree", degree_options)
    
    faculty_options = merged_df['Faculty'].dropna().unique()
    faculty = st.selectbox("Faculty", faculty_options)
    
    gender_options = merged_df['Gender'].dropna().unique()
    gender = st.selectbox("Gender", gender_options)
    
    status_options = merged_df['Status'].dropna().unique()
    status = st.selectbox("Status", status_options)
    
    submit_button = st.form_submit_button(label="Submit")

# Process the input and make prediction
if submit_button:
    if not first_name or not last_name:
        st.error("Please enter both First Name and Last Name.")
    else:
        # Prepare the input data for prediction
        input_data = {
            'Degree': [degree],
            'Faculty': [faculty],
            'Gender': [gender],
            'Status': [status],
        }
        
        # Convert to DataFrame
        input_df = pd.DataFrame(input_data)
        
        # Apply the same LabelEncoder transformations to the input data
        input_df['Degree'] = degree_encoder.transform(input_df['Degree'])
        input_df['Faculty'] = faculty_encoder.transform(input_df['Faculty'])
        input_df['Gender'] = gender_encoder.transform(input_df['Gender'])
        input_df['Status'] = status_encoder.transform(input_df['Status'])

        # Predict the category using the trained model
        prediction = best_model.predict(input_df)
        predicted_category = label_encoder.inverse_transform(prediction)[0]

        # Display the result
        st.subheader(f"Predicted Book Category: {predicted_category}")

        # Show potential books related to the predicted category
        related_books = merged_df[merged_df['Category'] == predicted_category]['Name'].unique()
        st.write(f"Potential Books for this Category:")
        st.write(related_books)
