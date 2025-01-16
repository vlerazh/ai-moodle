import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def load_and_visualize(file_name):
    df = pd.read_csv(file_name)

    if 'Cluster Name' not in df.columns:
        st.write("Kolona 'Cluster Name' nuk është e pranishme në file.")
        return

    st.write(f"Ky është dataset-i nga file: {file_name}")

    st.write("Të dhënat e plotë të studentëve:")

    st.dataframe(df, use_container_width=True)

    st.write("Shpërndarja e grupeve të parashikuara:")

    fig, ax = plt.subplots(figsize=(14, 8))

    sns.countplot(x='Cluster Name', data=df, palette='viridis', ax=ax)

    ax.set_title('Shpërndarja e Grupeve të Parashikuara', fontsize=16)
    ax.set_xlabel('Emri i Grupit', fontsize=14)
    ax.set_ylabel('Numri i Studentëve', fontsize=14)

    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_wrap(True)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45,
                       ha="right", rotation_mode="anchor")
    st.pyplot(fig)

    st.write("Numri i studentëve në secilin grup:")
    student_counts = df['Cluster Name'].value_counts()
    st.write(student_counts)


st.title("Visualizimi i Student Clustering")
file_option = st.selectbox(
    "Zgjidh një file CSV për të vizualizuar:",
    ("student_clustering_supervised.csv",
     "student_clustering_unsupervised_with_names.csv")
)

if file_option == "student_clustering_supervised.csv":
    load_and_visualize("data/student_clustering_supervised.csv")
else:
    load_and_visualize("data/student_clustering_unsupervised_with_names.csv")
