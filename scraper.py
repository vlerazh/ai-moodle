from typing import List, Set
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json

# Utility to check if a URL is a file
def _url_is_file(url: str) -> bool:
    for extension in [".jpg", ".jpeg", ".png", ".webp", ".pdf", ".txt"]:
        if url.endswith(extension):
            return True
    return False


# Extract internal links from a page
def _find_internal_links(
    current_url: str,
    html: str,
    base_domain: str,
    visited_links: Set[str],
    exclude_links: Set[str],
    queue: List[str],
    max_links: int,
) -> Set[str]:
    internal_links = set()
    soup = BeautifulSoup(html, "html.parser")

    for link in soup.find_all("a", href=True):
        if link["href"] in ["http://", "https://"]:
            continue

        absolute_link = urljoin(current_url, link["href"])

        if base_domain != urlparse(absolute_link).netloc:
            continue

        if (
            absolute_link not in visited_links
            and absolute_link not in exclude_links
            and absolute_link not in queue
            and not _url_is_file(absolute_link)
        ):
            absolute_link = absolute_link.replace(" ", "%20")  # Handle spaces
            queue.append(absolute_link)
            internal_links.add(absolute_link)

        if len(internal_links) == max_links:
            break

    return internal_links


# Fetch a URL and return HTML content using Playwright
async def _fetch_url(url: str, playwright: async_playwright) -> str:
    try:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        )  # Set the user agent in the context
        page = await context.new_page()

        await page.goto(url)
        html = await page.content()
        await browser.close()
        return html
    except Exception as ex:
        print(f"Error fetching URL: {url}. Exception: {ex}")
        return ""


# Crawl and extract links recursively using Playwright and store the data
async def crawl_links(
    url: str,
    exclude_links: Set[str],
    max_links: int = 30,
    output_file="data/output.json",
) -> List[str]:
    visited_links: Set[str] = set()
    links_to_return: List[str] = []
    scraped_data = {}

    base_domain = urlparse(url).netloc
    queue = [url]

    async with async_playwright() as playwright:
        while queue and len(scraped_data) < max_links:
            current_url = queue.pop(0)

            if current_url in visited_links and _url_is_file(current_url):
                continue

            visited_links.add(current_url)
            print(f"Fetching HTML for URL: {current_url}")

            html = await _fetch_url(current_url, playwright)
            if not html:
                continue

            soup = BeautifulSoup(html, "html.parser")
            page_content = soup.get_text(separator=" ").strip()

            # Store the content of the page
            scraped_data[current_url] = page_content

            # Find internal links and recursively follow them
            internal_links = _find_internal_links(
                current_url=current_url,
                html=html,
                base_domain=base_domain,
                visited_links=visited_links,
                exclude_links=exclude_links,
                queue=queue,
                max_links=max_links,
            )

            # Add the internal links to the queue
            queue.extend(internal_links)

            if len(scraped_data) >= max_links:
                break

    # Save the scraped data into a JSON file
    with open(output_file, "w") as f:
        json.dump(scraped_data, f, indent=4)

    print(f"Scraped {len(scraped_data)} URLs and saved them in {output_file}")
    return list(scraped_data.keys())  # Return the list of URLs scraped