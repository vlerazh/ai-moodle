import streamlit as st
from openai import OpenAI
import json
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY")
)

# Load the scraped data from the JSON file
with open('data/output.json', 'r') as f:
    scraped_data = json.load(f)

# Function to get the best match from the scraped data
def get_best_match(user_input):
    best_match = None
    best_score = 0

    # Find the best matching content in the scraped data
    for url, content in scraped_data.items():
        score = content.lower().count(user_input.lower())
        if score > best_score:
            best_score = score
            best_match = content

    return best_match if best_match else "Sorry, I couldn't find an answer."

# Function to get a GPT-4 (or GPT-4-mini) response based on the user input and the scraped content
def get_gpt4_response(user_input):
    print('user_input',user_input)
    messages = [
        {"role": "user", "content": user_input},
        # {"role": "assistant", "content": context}
    ]
    
    try:
        # Using OpenAI's new chat API
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the mini version of GPT-4
            messages=messages,
            temperature=0.7,  # Adjust for more or less creativity in the response
            max_tokens=150,
        )
        
        # Extracting the response from the API
        response = completion.choices[0].message.content.strip()
        print('response',response)
        return response
    except Exception as e:
        print(f"Error generating GPT-4 response: {e}")
        return "Sorry, I couldn't process your request."

# Streamlit UI components
st.title("Chatbot with GPT-4 (or GPT-4-mini) and Scraped Data")

# User input text box
user_input = st.text_input("Ask a question:")

if user_input:
    # Get the best matching content from the scraped data
    best_match = get_best_match(user_input)
    
    # if best_match:
        # Get a GPT-4 (or GPT-4-mini) response based on the best matching content
    response = get_gpt4_response(user_input)
    st.write(f"Bot: {response}")
    # else:
    #     st.write("Bot: Sorry, I couldn't find relevant content to answer your question.")