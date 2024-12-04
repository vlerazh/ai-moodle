# Import libraries
import pandas as pd
import random
from faker import Faker

# Initialize Faker for realistic mock data
faker = Faker()

# The number of books defined
num_books = 50  

# Generate data for each column
book_ids = [f"B{str(i).zfill(3)}" for i in range(
    1, num_books + 1)]  # Unique IDs like B001, B002
titles = [faker.sentence(nb_words=3)
          for _ in range(num_books)]  # Random book titles
authors = [faker.name() for _ in range(num_books)]  # Random author names
years = [random.randint(2000, 2023) for _ in range(num_books)]  # Random years
categories = random.choices(
    ["Technology", "Science", "Fiction", "History", "Mathematics"], k=num_books
)  # Random categories
descriptions = [faker.text(max_nb_chars=100)
                for _ in range(num_books)]  # Random summaries

# Combine the data into a DataFrame
data = {
    "Book ID": book_ids,
    "Title": titles,
    "Author": authors,
    "Publication Year": years,
    "Category": categories,
    "Short Description": descriptions,
}
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
file_name = "library_books.csv"
df.to_csv(file_name, index=False)

# Print confirmation
print(f"Dataset created successfully! Saved as '{file_name}'.")
