import asyncio
from scraper import crawl_links

async def main():
    url = "https://www.ubt-uni.net/sq/ubt/"
    exclude_links = set() 
    max_links = 150 

    print("Starting the web scraping process...")

    scraped_links = await crawl_links(url, exclude_links, max_links)
    
    print(f"Scraped {len(scraped_links)} links:")
    for link in scraped_links:
        print(link)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
