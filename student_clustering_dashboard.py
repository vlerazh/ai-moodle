import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from enum import Enum

# Enum for Group Names
class GroupNames(Enum):
    LITERATURE = "Literature Enthusiasts"
    TECH = "Tech Savvy Explorers"
    LEADERS = "Future Leaders"
    PHILOSOPHERS = "Philosophers & Thinkers"
    SCIENCE = "Science Seekers"

# Map Cluster IDs to GroupNames Enum
cluster_to_group = {
    0: GroupNames.LITERATURE,
    1: GroupNames.TECH,
    2: GroupNames.LEADERS,
    3: GroupNames.PHILOSOPHERS,
    4: GroupNames.SCIENCE
}

# Singleton Pattern for KMeans Model
class KMeansModel:
    _instance = None

    @staticmethod
    def get_instance():
        if KMeansModel._instance is None:
            KMeansModel()
        return KMeansModel._instance

    def __init__(self):
        if KMeansModel._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.model = KMeans(n_clusters=5, random_state=42)
            KMeansModel._instance = self

# Data Loader with Exception Handling
class DataLoader:
    @staticmethod
    def load_csv(path):
        try:
            return pd.read_csv(path)
        except FileNotFoundError:
            st.error(f"File not found: {path}")
            return pd.DataFrame()

# Data Preprocessing
class DataPreprocessor:
    def __init__(self, student_df, book_df):
        self.student_df = student_df
        self.book_df = book_df
        self.degree_encoder = LabelEncoder()
        self.faculty_encoder = LabelEncoder()
        self.status_encoder = LabelEncoder()

    def preprocess(self):
        self.student_df['Full Name'] = self.student_df['First Name'] + " " + self.student_df['Last Name']
        
        # Create a dictionary to map Book IDs to Book Names
        book_id_to_name = dict(zip(self.book_df['Book ID'], self.book_df['Name']))
        
        # Generate a Books Reading column with book names
        self.student_df['Books Reading'] = self.student_df['E-Library Book ID'].apply(
            lambda x: ', '.join([book_id_to_name.get(book_id.strip(), 'Unknown') for book_id in str(x).split(',')])
        )
        
        # Encode degree, faculty, and status
        self.student_df['Degree'] = self.degree_encoder.fit_transform(self.student_df['Degree'])
        self.student_df['Faculty'] = self.faculty_encoder.fit_transform(self.student_df['Faculty'])
        self.student_df['Status'] = self.status_encoder.fit_transform(self.student_df['Status'])
        
        return self.student_df

# Clustering
class StudentClusterer:
    def __init__(self, student_df, book_df):
        self.student_df = student_df
        self.book_df = book_df
        self.kmeans = KMeansModel.get_instance().model

    def cluster(self):
        # Use Degree, Faculty, Status, and Books Reading as features
        X = self.student_df[['Degree', 'Faculty', 'Status']]
        
        # Convert the Books Reading column into a numerical representation using CountVectorizer
        vectorizer = CountVectorizer()
        books_features = vectorizer.fit_transform(self.student_df['Books Reading'].fillna('')).toarray()
        
        # Combine the books' features with Degree, Faculty, and Status
        X = self.student_df[['Degree', 'Faculty', 'Status']].join(pd.DataFrame(books_features))

        # Ensure all column names are strings
        X.columns = X.columns.astype(str)

        # Perform KMeans clustering
        self.student_df['Cluster'] = self.kmeans.fit_predict(X)
        
        return self.student_df

# Streamlit Dashboard
class ClusteringDashboard:
    def __init__(self, student_df, degree_encoder, faculty_encoder):
        self.student_df = student_df
        self.degree_encoder = degree_encoder
        self.faculty_encoder = faculty_encoder

    def run(self):
        st.set_page_config(page_title="Student Group Clustering Dashboard", layout="wide")
        st.title("\U0001F4DA Student Group Clustering Dashboard")
        st.sidebar.header("\U0001F50D Search Student")
        selected_student_name = st.sidebar.selectbox("Select a student:", self.student_df['Full Name'].values)
        selected_student = self.student_df[self.student_df['Full Name'] == selected_student_name].iloc[0]

        st.subheader(f"\U0001F9D1‍\U0001F393 Student Profile: {selected_student['Full Name']}")
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.markdown(f"**\U0001F393 Degree Program:** {self.degree_encoder.inverse_transform([selected_student['Degree']])[0]}")
            st.markdown(f"**\U0001F3E2 Faculty:** {self.faculty_encoder.inverse_transform([selected_student['Faculty']])[0]}")

        with col2:
            st.markdown(f"**\U0001F4D6 Books Reading:** {selected_student['Books Reading']}")
            st.markdown(f"**\U0001F4CA Group:** {cluster_to_group[selected_student['Cluster']].value}")

        with col3:
            st.markdown(f"**\U0001F4C5 Enrollment Date:** {selected_student['Enrollment Date']}")
            st.markdown(f"**\U0001F516 Status:** {'Active' if selected_student['Status'] == 1 else 'Inactive'}")

        st.subheader("\U0001F4CA Cluster Overview")
        for cluster_id, group in self.student_df.groupby('Cluster'):
            with st.expander(f"{cluster_to_group[cluster_id].value} ({len(group)} Students)"):
                group['Degree'] = group['Degree'].apply(lambda x: self.degree_encoder.inverse_transform([x])[0])
                group['Faculty'] = group['Faculty'].apply(lambda x: self.faculty_encoder.inverse_transform([x])[0])
                st.dataframe(group[['Full Name', 'Faculty', 'Degree', 'Books Reading']].reset_index(drop=True))

        st.subheader("\U0001F4AC Group Chatbot")
        st.info("Chat functionality will be available soon for student group interactions.")

# Main Execution
def main():
    student_df = DataLoader.load_csv('data/mock_student_dataset.csv')
    book_df = DataLoader.load_csv('data/mock_e_library_dataset.csv')
    preprocessor = DataPreprocessor(student_df, book_df)
    processed_df = preprocessor.preprocess()
    clusterer = StudentClusterer(processed_df, book_df)
    clustered_df = clusterer.cluster()
    dashboard = ClusteringDashboard(clustered_df, preprocessor.degree_encoder, preprocessor.faculty_encoder)
    dashboard.run()

if __name__ == "__main__":
    main()
