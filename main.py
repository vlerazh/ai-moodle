import asyncio
from scraper import crawl_links

async def main():
    url = "https://www.ubt-uni.net/sq/ubt/"
    exclude_links = set() 
    max_links = 150  # Scrape 150 links
    output_file = "data/output.json"  # Store output in this file

    print("Starting the web scraping process...")

    # Scrape the links and store data in the specified output file
    scraped_links = await crawl_links(url, exclude_links, max_links, output_file)
    
    print(f"Scraped {len(scraped_links)} links:")
    for link in scraped_links:
        print(link)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
