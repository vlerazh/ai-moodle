# app.py

import os
import asyncio
import json
import time
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from scraper import crawl_links
from chat_app import run_chatbot  # Import the chatbot function

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Ensure the data directory exists
if not os.path.exists("data"):
    os.makedirs("data")

# Caching the file upload to avoid redundant uploads
@st.cache_resource
def upload_file(file_path):
    with open(file_path, 'rb') as f:
        return client.files.create(
            file=f,
            purpose="assistants"
        )

# Caching the assistant creation to prevent multiple instances
@st.cache_resource
def create_assistant(file_id):
    return client.beta.assistants.create(
        name="UBT assistant",
        instructions=(
            "You are a helpful assistant that answers questions solely based on the content of the provided 'output.txt' file. "
            "Do not use or refer to any external information or sources outside of this file. "
            "Respond in the same language as the user's input; always respond in Albanian. "
            "Do not include filenames, page numbers, or external references. "
            "If the user asks for information not contained within 'output.txt', inform them that you cannot answer that question. "
            "Maintain the flow of conversation by referencing previous interactions when relevant."
        ),
        model="gpt-3.5-turbo",  # Use a faster model if appropriate
        tools=[{"type": "code_interpreter"}],
        tool_resources={
            "code_interpreter": {
                "file_ids": [file_id]
            }
        }
    )

# Asynchronous function to handle scraping
async def run_scraping(url, exclude_links, max_links, output_file, text_output_file, scraped_urls_placeholder):
    scraped_links = await crawl_links(url, exclude_links, max_links, output_file)
    
    # Convert JSON data to plain text
    try:
        with open(output_file, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        with open(text_output_file, "w", encoding="utf-8") as text_file:
            for link, content in data.items():
                text_file.write(f"Content:\n{content}\n")
                text_file.write("=" * 80 + "\n")  # Add a separator for readability

        # Display the scraped URLs
        scraped_urls = list(data.keys())
        scraped_urls_placeholder.text_area("Scraped URLs:", value="\n".join(scraped_urls), height=300)
    except Exception as e:
        st.error(f"Error converting JSON to text: {e}")

# Sidebar is no longer needed for navigation, so we remove it
# Implement tabs in the main area
st.title("UBT Tool")

# Create tabs
tab_scraping, tab_chatbot = st.tabs(["🕸️ Scraping", "💬 Chatbot"])

with tab_scraping:
    st.header("Web Scraping Tool")
    
    with st.form(key="scraping_form"):
        url = st.text_input("Enter the URL to scrape:", value="https://www.ubt-uni.net/sq/ubt/")
        max_links = st.number_input("Maximum number of links to scrape:", min_value=10, max_value=1000, value=150, step=10)
        submit_button = st.form_submit_button("Start Scraping")
    
    if submit_button:
        if not url:
            st.error("Please enter a valid URL.")
        else:
            # Define file paths
            output_file = "data/output.json"
            text_output_file = "data/output.txt"
            exclude_links = set()
            
            # Create data directory if it doesn't exist
            if not os.path.exists("data"):
                os.makedirs("data")
            
            # Display progress and status
            with st.spinner("Scraping in progress..."):
                # Start scraping synchronously
                try:
                    asyncio.run(run_scraping(
                        url=url,
                        exclude_links=exclude_links,
                        max_links=max_links,
                        output_file=output_file,
                        text_output_file=text_output_file,
                        scraped_urls_placeholder=st.empty()  # Pass a new empty container
                    ))
                    
                    # Upload the scraped file to OpenAI
                    my_file = upload_file(output_file)
                    
                    # Create the assistant
                    if "my_assistant" not in st.session_state:
                        st.session_state["my_assistant"] = create_assistant(my_file.id)
                    st.success("Scraping and assistant setup completed successfully!")
                except Exception as e:
                    st.error(f"An error occurred during scraping: {e}")

with tab_chatbot:
    st.header("Chat with UBT Assistant")
    
    # Ensure that the assistant is set up
    if "my_assistant" not in st.session_state:
        st.warning("Please complete the scraping process first.")
    else:
        my_assistant = st.session_state["my_assistant"]
        
        # Run the chatbot from chat_app.py
        run_chatbot(my_assistant, client)