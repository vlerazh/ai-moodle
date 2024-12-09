import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    """
    Scrape text content from a webpage and clean it.
    :param url: URL of the website to scrape.
    :return: Cleaned and meaningful text content of the webpage.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator=" ")
            cleaned_text = " ".join(text.split())
            return cleaned_text
        else:
            return f"Failed to scrape {url}, status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
