import asyncio
import json
from scraper import crawl_links

async def main():
    url = "https://www.ubt-uni.net/sq/ubt/"
    exclude_links = set()
    max_links = 150  # Scrape 150 links
    output_file = "data/output.json"  # Store output in this file
    text_output_file = "data/output.txt"  # Store plain text output here

    print("Starting the web scraping process...")

    # Scrape the links and store data in the specified output file
    scraped_links = await crawl_links(url, exclude_links, max_links, output_file)
    
    print(f"Scraped {len(scraped_links)} links:")
    for link in scraped_links:
        print(link)

    # Convert JSON data to plain text
    try:
        with open(output_file, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        with open(text_output_file, "w", encoding="utf-8") as text_file:
            for link, content in data.items():
                text_file.write(f"Content:\n{content}\n")
                text_file.write("=" * 80 + "\n")  # Add a separator for readability

        print(f"Data successfully written to {text_output_file}")

    except Exception as e:
        print(f"Error converting JSON to text: {e}")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
