from scraper import scrape_website
from file_handler import extract_data_from_file

def main():
    print("Welcome to the Chatbot Project!")
    print("1. Scrape a website")
    print("2. Process a document (PDF, TXT, DOCX)")
    choice = input("Choose an option (1/2): ")

    if choice == '1':
        url = input("Enter the website URL: ")
        data = scrape_website(url)
        with open("data/output.txt", "w", encoding="utf-8") as file:
            file.write(data)
        print(f"Data has been saved to data/output.txt")
    elif choice == '2':
        file_path = input("Enter the document path: ")
        data = extract_data_from_file(file_path)
        with open("data/output.txt", "w", encoding="utf-8") as file:
            file.write(data)
        print(f"Data has been saved to data/output.txt")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
