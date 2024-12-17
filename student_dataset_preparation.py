import pandas as pd
from faker import Faker
import random


fake = Faker()

# Function to generate a logical description based on book title and category
def generate_description(book_title, category):
    descriptions = {
        'Computer Science': {
            'Machine Learning Techniques': 'This book covers the foundational concepts of machine learning, including supervised and unsupervised learning, model evaluation, and practical applications in real-world scenarios.',
            'Data Structures': 'An essential guide to data structures in computer science, including arrays, linked lists, trees, and graphs, with practical implementation examples.',
            'Algorithms': 'A comprehensive introduction to algorithms, discussing different types including searching, sorting, and graph algorithms with algorithmic complexity analysis.',
        },
        'Mathematics': {
            'Calculus': 'An exploration of key concepts in calculus such as limits, derivatives, and integrals, with applications in engineering and physics.',
            'Linear Algebra': 'This book provides a thorough understanding of linear algebra concepts, including matrix operations, vector spaces, and eigenvalues/eigenvectors.',
        },
        'Physics': {
            'Quantum Physics': 'A detailed introduction to quantum mechanics, including wave-particle duality, quantum states, and principles governing atomic and subatomic particles.',
            'Thermodynamics': 'An overview of the laws of thermodynamics, discussing heat transfer, energy conservation, and the behavior of gases.',
        },
        'Literature': {
            'Modern Literature': 'An examination of contemporary literature, discussing major themes, authors, and movements that define modern storytelling.',
            'Poetry': 'An anthology of significant poetic works, analyzing various forms, styles, and the emotional impact of poetry on society.',
        },
        'Biology': {
            'Molecular Biology': 'A deep dive into the molecular foundations of biological processes, exploring DNA, RNA, and protein synthesis among other topics.',
            'Genetics': 'An introduction to the principles of genetics, including heredity, gene expression, and genetic variability in populations.',
        }
    }
    
    # Return a description based on category and title or a default message if not found
    return descriptions.get(category, {}).get(book_title, fake.text(max_nb_chars=100)) 


class ELibraryBook:
    def __init__(self, book_id, category):
        self.book_id = f'B{book_id:03}'
        self.category = category
        
        # Book titles corresponding to each category
        book_titles = {
            'Computer Science': ['Machine Learning Techniques', 'Data Structures', 'Algorithms'],
            'Mathematics': ['Calculus', 'Linear Algebra'],
            'Physics': ['Quantum Physics', 'Thermodynamics'],
            'Literature': ['Modern Literature', 'Poetry'],
            'Biology': ['Molecular Biology', 'Genetics']
        }
        
        # Randomly pick a book title based on category
        self.name = random.choice(book_titles[self.category])
        
        # Generate the book description based on category and name
        self.description = generate_description(self.name, self.category)


class Faculty:
    def __init__(self, name):
        self.name = name
        self.departments = {}

    def add_department(self, department_name, degree_class):
        self.departments[department_name] = degree_class


class Degree:
    def __init__(self, degree_name, faculty, department):
        self.degree_name = degree_name
        self.faculty = faculty
        self.department = department
        self.faculty.add_department(department, self)

    def get_subjects(self):
        raise NotImplementedError("Each degree must implement its own subjects.")


class BScComputerScience(Degree):
    def __init__(self, faculty):
        super().__init__('BSc in Computer Science', faculty, 'Computer Science')

    def get_subjects(self):
        return ['Python Programming', 'Data Structures', 'Algorithms', 'Operating Systems', 'Database Systems']


class BScMathematics(Degree):
    def __init__(self, faculty):
        super().__init__('BSc in Mathematics', faculty, 'Mathematics')

    def get_subjects(self):
        return ['Calculus', 'Linear Algebra', 'Probability and Statistics', 'Discrete Mathematics']


class BScPhysics(Degree):
    def __init__(self, faculty):
        super().__init__('BSc in Physics', faculty, 'Physics')

    def get_subjects(self):
        return ['Mechanics', 'Quantum Physics', 'Thermodynamics', 'Electromagnetism']


class MScLiterature(Degree):
    def __init__(self, faculty):
        super().__init__('MSc in Literature', faculty, 'Literature')

    def get_subjects(self):
        return ['Shakespearean Drama', 'Modern Literature', 'Poetry', 'Philosophy', 'Literary Theory']


class MScBiology(Degree):
    def __init__(self, faculty):
        super().__init__('MSc in Biology', faculty, 'Biology')

    def get_subjects(self):
        return ['Molecular Biology', 'Genetics', 'Ecology', 'Microbiology']


class Student:
    def __init__(self, student_id, degree):
        self.student_id = f'S{student_id:03}'
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.age = random.randint(18, 30)
        self.gender = random.choice(['Male', 'Female'])
        self.status = random.choice(['Active', 'Inactive'])
        self.enrollment_date = fake.date_between(start_date='-3y', end_date='today')

        self.degree = degree
        self.faculty = degree.faculty
        self.department = degree.department
        self.subjects = degree.get_subjects()
        self.e_library_book_id = self.get_e_library_book_id()

    def get_e_library_book_id(self):
        # Map the degree department to a category and get a corresponding book
        category_map = {
            'Computer Science': 'Computer Science',
            'Mathematics': 'Mathematics',
            'Physics': 'Physics',
            'Literature': 'Literature',
            'Biology': 'Biology'
        }
        
        category = category_map[self.department]
        
        # Find a book ID corresponding to the category
        category_books = [book for book in books if book.category == category]
        if category_books:
            book_id = random.choice(category_books).book_id
            return book_id
        return None


# Parameters
number_of_students = 100  # Set the number of students to generate
number_of_books = 20       # Set the number of e-library books to generate

# Create faculties
faculty_of_science = Faculty("Faculty of Science")
faculty_of_arts = Faculty("Faculty of Arts")

# Generate degrees
degrees = [
    BScComputerScience(faculty_of_science),
    BScMathematics(faculty_of_science),
    BScPhysics(faculty_of_science),
    MScLiterature(faculty_of_arts),
    MScBiology(faculty_of_science)
]

# Generate e-library book dataset
book_data = {
    "Book ID": [],
    "Category": [],
    "Name": [],
    "Description": []
}

books = []  # Store books so that we can later map students to them

for book_id in range(1, number_of_books + 1):
    category = random.choice(['Computer Science', 'Mathematics', 'Physics', 'Literature', 'Biology'])
    book = ELibraryBook(book_id, category)
    books.append(book)
    book_data["Book ID"].append(book.book_id)
    book_data["Category"].append(book.category)
    book_data["Name"].append(book.name)
    book_data["Description"].append(book.description)

book_df = pd.DataFrame(book_data)

# Generate student dataset
student_data = {
    "Student ID": [],
    "First Name": [],
    "Last Name": [],
    "Age": [],
    "Gender": [],
    "Status": [],
    "Enrollment Date": [],
    "Degree": [],
    "Faculty": [],
    "Subjects": [],
    "E-Library Book ID": []
}

for student_id in range(1, number_of_students + 1):
    degree = random.choice(degrees)
    student = Student(student_id, degree)
    student_data["Student ID"].append(student.student_id)
    student_data["First Name"].append(student.first_name)
    student_data["Last Name"].append(student.last_name)
    student_data["Age"].append(student.age)
    student_data["Gender"].append(student.gender)
    student_data["Status"].append(student.status)
    student_data["Enrollment Date"].append(student.enrollment_date)
    student_data["Degree"].append(student.degree.degree_name)
    student_data["Faculty"].append(student.faculty.name)
    student_data["Subjects"].append(student.subjects)
    student_data["E-Library Book ID"].append(student.e_library_book_id)

# Create DataFrame for students
student_df = pd.DataFrame(student_data)

# Save to CSV files
student_df.to_csv('mock_student_dataset.csv', index=False)
book_df.to_csv('mock_e_library_dataset.csv', index=False)

print("Mock student and e-library datasets have been generated and saved to CSV files.")