import streamlit as st
import requests

API_URL = "http://localhost:3000/api/v1/prediction/cbe8d440-54ad-4a04-ae30-7a9086550d38"

def query(payload):
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        st.write("HTTP Error:", errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        st.write("Error Connecting:", errc)
        return None
    except requests.exceptions.Timeout as errt:
        st.write("Timeout Error:", errt)
        return None
    except requests.exceptions.RequestException as err:
        st.write("Something went wrong. Please try again.", err)
        return None
    
    try:
        return response.json()
    except Exception as e:
        st.write("Error parsing response:", e)
        return None

st.title('API Chatbot')

# List to hold the conversation history
conversation = []

# User input
user_input = st.text_input("Enter your message:")
submit_button = st.button('Submit')

if submit_button:
    # Add user input to conversation history
    conversation.append({'role': 'user', 'content': user_input})
    
    # Query the API
    response = query({'history': conversation, 'question': user_input})
    
    if response is not None:
        # Add bot response to conversation history
        conversation.append({'role': 'bot', 'content': response})
    else:
        conversation.append({'role': 'bot', 'content': 'Sorry, I am unable to process your request at the moment.'})
    
    # Display the conversation history
    for message in conversation:
        if message['role'] == 'user':
            st.write(f"User: {message['content']}")
        else:  # message['role'] == 'bot'
            st.write(f"AI Bot: {message['content']}")
