
import pandas as pd 
import random
from faker import Faker


faker = Faker()


num_books = 50


book_ids = [f"B{str(i).zfill(3)}" for i in range(
    1, num_books + 1)]
titles = [faker.sentence(nb_words=3)
          for _ in range(num_books)]
authors = [faker.name() for _ in range(num_books)]
years = [random.randint(2000, 2023) for _ in range(num_books)]
categories = random.choices(
    ["Technology", "Science", "Fiction", "History", "Mathematics"], k=num_books
)
descriptions = [faker.text(max_nb_chars=100)
                for _ in range(num_books)]

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


file_name = "library_books.csv"
df.to_csv(file_name, index=False)


print(f"Dataset created successfully! Saved as '{file_name}'.")
