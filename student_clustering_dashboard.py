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

# Save original Degree and Faculty names for display
original_degree = student_df['Degree']
original_faculty = student_df['Faculty']

# Encode categorical features
label_encoder = LabelEncoder()
student_df['Degree'] = label_encoder.fit_transform(student_df['Degree'])
student_df['Faculty'] = label_encoder.fit_transform(student_df['Faculty'])
student_df['Status'] = label_encoder.fit_transform(student_df['Status'])
student_df['Encoded Books Reading'] = label_encoder.fit_transform(student_df['Books Reading'])

# Clustering
X = student_df[['Degree', 'Faculty', 'Status', 'Encoded Books Reading']]
kmeans = KMeans(n_clusters=3, random_state=42)
student_df['Cluster'] = kmeans.fit_predict(X)

# Group names
group_names = {
    0: "Computer Science Student Group",
    1: "Social Sciences Student Group",
    2: "Law Student Group"
}

# Streamlit App
st.set_page_config(page_title="Student Group Clustering Dashboard", layout="wide")
st.title("📚 Student Group Clustering Dashboard")

# Sidebar for Student Selection
st.sidebar.header("🔍 Search Student")
selected_student_name = st.sidebar.selectbox("Select a student:", student_df['Full Name'].values)
selected_student = student_df[student_df['Full Name'] == selected_student_name].iloc[0]

# Display Student Profile
st.subheader(f"🧑‍🎓 Student Profile: {selected_student['Full Name']}")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown(f"**🎓 Degree Program:** {original_degree[selected_student.name]}")
    st.markdown(f"**🏢 Faculty:** {original_faculty[selected_student.name]}")

with col2:
    st.markdown(f"**📖 Books Reading:** {selected_student['Books Reading']}")
    st.markdown(f"**📊 Group:** {group_names[selected_student['Cluster']]}")

with col3:
    st.markdown(f"**📅 Enrollment Date:** {selected_student['Enrollment Date']}")
    st.markdown(f"**🔖 Status:** {'Active' if selected_student['Status'] == 1 else 'Inactive'}")

# Cluster Overview
st.subheader("📊 Cluster Overview")
for cluster_id, group in student_df.groupby('Cluster'):
    with st.expander(f"{group_names[cluster_id]} ({len(group)} Students)"):
        st.dataframe(group[['Full Name', 'Faculty', 'Degree', 'Books Reading', 'Encoded Books Reading']].reset_index(drop=True))

# Chatbot Placeholder
st.subheader("💬 Group Chatbot")
st.info("Chat functionality will be available soon for student group interactions.")
