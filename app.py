# app.py

import os
import asyncio
import json
import streamlit as st
from config import client
from scraper import crawl_links
from chat_app import run_chatbot  

os.makedirs("data", exist_ok=True)

# Caching the file upload to avoid redundant uploads
@st.cache_resource
def upload_file(file_path):
    with open(file_path, 'rb') as f:
        return client.files.create(
            file=f,
            purpose="assistants"
        )

# Caching the assistant 
@st.cache_resource
def create_assistant(file_id):
    return client.beta.assistants.create(
        name="UBT assistant",
        instructions=(
            "You are a helpful assistant. You answer questions solely based on the content of the provided 'output.txt' file. "
            "Do not use or refer to any external information or sources outside of this file. "
            "Respond in the same language as the user's input; always respond in Albanian. "
            "Do not include filenames, page numbers, or external references. "
            "If the user asks for information not contained within 'output.txt', inform them that you cannot answer that question. "
            "Maintain the flow of conversation by referencing previous interactions when relevant."
            "Do not explicitly mention that you are using the 'output.txt' file for your responses."
        ),
        model="gpt-4o-mini", 
        tools=[{"type": "code_interpreter"}],
        tool_resources={
            "code_interpreter": {
                "file_ids": [file_id]
            }
        }
    )

async def run_scraping(url, exclude_links, max_links, output_file, text_output_file, scraped_urls_placeholder):
    scraped_links = await crawl_links(url, exclude_links, max_links, output_file)
    
    try:
        with open(output_file, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        with open(text_output_file, "w", encoding="utf-8") as text_file:
            for link, content in data.items():
                text_file.write(f"Content:\n{content}\n")
                text_file.write("=" * 80 + "\n")  

        scraped_urls = list(data.keys())
        scraped_urls_placeholder.text_area("Scraped URLs:", value="\n".join(scraped_urls), height=300)
    except Exception as e:
        st.error(f"Error converting JSON to text: {e}")

st.title("UBT Tool")

tab_scraping, tab_chatbot = st.tabs(["🕸️ Scraping", "💬 Chatbot"])

# Scraping Tab
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
            output_file = "data/output.json"
            text_output_file = "data/output.txt"
            exclude_links = set()
            
            # Display progress and status
            with st.spinner("Scraping in progress..."):
                try:
                    asyncio.run(run_scraping(
                        url=url,
                        exclude_links=exclude_links,
                        max_links=max_links,
                        output_file=output_file,
                        text_output_file=text_output_file,
                        scraped_urls_placeholder=st.empty() 
                    ))
                    
                    my_file = upload_file(output_file)
                    
                    if "my_assistant" not in st.session_state:
                        st.session_state["my_assistant"] = create_assistant(my_file.id)
                    st.success("Scraping and assistant setup completed successfully!")
                except Exception as e:
                    st.error(f"An error occurred during scraping: {e}")

# Chatbot Tab
with tab_chatbot:
    st.header("Chat with UBT Assistant")
    
    if "my_assistant" not in st.session_state:
        st.warning("Please complete the scraping process first.")
    else:
        my_assistant = st.session_state["my_assistant"]
        
        run_chatbot(my_assistant, client)