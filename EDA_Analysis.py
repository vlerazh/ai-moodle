import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

student_df = pd.read_csv('data/mock_student_dataset.csv')
book_df = pd.read_csv('data/mock_e_library_dataset.csv')

# --- 1. Basic Information & Structure ---
# Book DataFrame info
print("Book DataFrame Info:")
print(book_df.info())

# Student DataFrame info
print("\nStudent DataFrame Info:")
print(student_df.info())

# Preview the first few rows of both dataframes
print("\nFirst 5 rows of book_df:")
print(book_df.head())

print("\nFirst 5 rows of student_df:")
print(student_df.head())

# --- 2. Descriptive Statistics ---
# Descriptive statistics for numerical columns in student_df
print("\nStudent DataFrame Descriptive Statistics:")
print(student_df.describe())

# For 'Age' column in student_df, check its unique values and distribution
print("\nUnique values for Age column:")
print(student_df['Age'].value_counts())

# For 'Gender' distribution
print("\nGender Distribution:")
print(student_df['Gender'].value_counts())

# For 'Enrollment Date', check the min and max dates
print("\nEnrollment Date Range:")
print(student_df['Enrollment Date'].min(), " to ", student_df['Enrollment Date'].max())

# Descriptive statistics for book_df's 'Name' column
book_name_lengths = book_df['Name'].apply(len)
print("\nBook Name Lengths (Mean and Distribution):")
print(book_name_lengths.describe())

# Category distribution in book_df
print("\nCategory Distribution in Book DataFrame:")
print(book_df['Category'].value_counts())

# --- 3. Missing Values ---
# Check for missing values in both dataframes
print("\nMissing Values in Book DataFrame:")
print(book_df.isnull().sum())

print("\nMissing Values in Student DataFrame:")
print(student_df.isnull().sum())

# --- 4. Categorical Analysis ---

# Book Category Distribution
plt.figure(figsize=(10, 6))
sns.countplot(data=book_df, x='Category')
plt.title('Book Category Distribution')
plt.xticks(rotation=45)
plt.show()

# Gender Distribution in student_df
plt.figure(figsize=(6, 6))
sns.countplot(data=student_df, x='Gender')
plt.title('Gender Distribution')
plt.show()

# Degree Program Distribution
plt.figure(figsize=(10, 6))
sns.countplot(data=student_df, x='Degree')
plt.title('Degree Program Distribution')
plt.xticks(rotation=45)
plt.show()

# Faculty Distribution
plt.figure(figsize=(10, 6))
sns.countplot(data=student_df, x='Faculty')
plt.title('Faculty Distribution')
plt.xticks(rotation=45)
plt.show()

# --- 5. Age Distribution ---
# Age Distribution in student_df
plt.figure(figsize=(10, 6))
sns.histplot(student_df['Age'], kde=True, bins=20)
plt.title('Age Distribution of Students')
plt.show()

# --- 6. Relationships Between Columns ---
# Degree vs Faculty (to see how degrees are distributed across faculties)
plt.figure(figsize=(12, 6))
sns.countplot(data=student_df, x='Degree', hue='Faculty')
plt.title('Degree vs Faculty')
plt.xticks(rotation=45)
plt.show()

# Age vs Status (check distribution of Age by Status)
plt.figure(figsize=(10, 6))
sns.boxplot(data=student_df, x='Status', y='Age')
plt.title('Age Distribution by Student Status')
plt.show()

# --- 7. Text Analysis (for 'Description' in book_df) ---
# Generate a word cloud for all book descriptions
all_descriptions = " ".join(book_df['Description'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_descriptions)

plt.figure(figsize=(12, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud of Book Descriptions')
plt.axis('off')
plt.show()

# --- 8. Time-based Analysis (Enrollment Date) ---
# Convert Enrollment Date to datetime if not already
student_df['Enrollment Date'] = pd.to_datetime(student_df['Enrollment Date'])

# Plot a count of enrollments per year
plt.figure(figsize=(10, 6))
student_df['Enrollment Year'] = student_df['Enrollment Date'].dt.year
sns.countplot(data=student_df, x='Enrollment Year')
plt.title('Enrollment Distribution by Year')
plt.show()


