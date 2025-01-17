import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans

# Load datasets
student_df = pd.read_csv('data/mock_student_dataset.csv')
book_df = pd.read_csv('data/mock_e_library_dataset.csv')

# Combine first and last names for full name
student_df['Full Name'] = student_df['First Name'] + " " + student_df['Last Name']

# Map E-Library Book IDs to Book Names
book_id_to_name = dict(zip(book_df['Book ID'], book_df['Name']))
student_df['Books Reading'] = student_df['E-Library Book ID'].apply(
    lambda x: ', '.join([book_id_to_name.get(book_id.strip(), 'Unknown') for book_id in str(x).split(',')])
)

# Encode categorical features with separate encoders
degree_encoder = LabelEncoder()
faculty_encoder = LabelEncoder()
status_encoder = LabelEncoder()
books_encoder = LabelEncoder()

student_df['Degree'] = degree_encoder.fit_transform(student_df['Degree'])
student_df['Faculty'] = faculty_encoder.fit_transform(student_df['Faculty'])
student_df['Status'] = status_encoder.fit_transform(student_df['Status'])
student_df['Encoded Books Reading'] = books_encoder.fit_transform(student_df['Books Reading'])

# Clustering
X = student_df[['Degree', 'Faculty', 'Status', 'Encoded Books Reading']]
kmeans = KMeans(n_clusters=5, random_state=42)
student_df['Cluster'] = kmeans.fit_predict(X)

# Creative group names based on reading habits
group_names = {
    0: "Literature Enthusiasts",
    1: "Tech Savvy Explorers",
    2: "Future Leaders",
    3: "Philosophers & Thinkers",
    4: "Science Seekers"
}

# Streamlit App
st.set_page_config(page_title="Student Group Clustering Dashboard", layout="wide")
st.title("\U0001F4DA Student Group Clustering Dashboard")

# Sidebar for Student Selection
st.sidebar.header("\U0001F50D Search Student")
selected_student_name = st.sidebar.selectbox("Select a student:", student_df['Full Name'].values)
selected_student = student_df[student_df['Full Name'] == selected_student_name].iloc[0]

# Display Student Profile
st.subheader(f"\U0001F9D1‍\U0001F393 Student Profile: {selected_student['Full Name']}")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown(f"**\U0001F393 Degree Program:** {degree_encoder.inverse_transform([selected_student['Degree']])[0]}")
    st.markdown(f"**\U0001F3E2 Faculty:** {faculty_encoder.inverse_transform([selected_student['Faculty']])[0]}")

with col2:
    st.markdown(f"**\U0001F4D6 Books Reading:** {selected_student['Books Reading']}")
    st.markdown(f"**\U0001F4CA Group:** {group_names[selected_student['Cluster']]}")

with col3:
    st.markdown(f"**\U0001F4C5 Enrollment Date:** {selected_student['Enrollment Date']}")
    st.markdown(f"**\U0001F516 Status:** {'Active' if selected_student['Status'] == 1 else 'Inactive'}")

# Cluster Overview
st.subheader("\U0001F4CA Cluster Overview")
for cluster_id, group in student_df.groupby('Cluster'):
    with st.expander(f"{group_names[cluster_id]} ({len(group)} Students)"):
        group['Degree'] = group['Degree'].apply(lambda x: degree_encoder.inverse_transform([x])[0])
        group['Faculty'] = group['Faculty'].apply(lambda x: faculty_encoder.inverse_transform([x])[0])
        st.dataframe(group[['Full Name', 'Faculty', 'Degree', 'Books Reading']].reset_index(drop=True))

# Chatbot Placeholder
st.subheader("\U0001F4AC Group Chatbot")
st.info("Chat functionality will be available soon for student group interactions.")
