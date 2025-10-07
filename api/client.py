import requests
import streamlit as st

# def get_openai_response(input_text):
#     response=requests.post("http://localhost:8000/essay/invoke",
#     json={'input':{'topic':input_text}})

#     return response.json()['output']['content']

def get_ollama_response(input_text):
    try:
        payload = {
        "input": {"topic": input_text},
        "config": {},
        "kwargs": {}
        }

        response = requests.post(
            "http://127.0.0.1:8000/essay/invoke",
            json={'input': {'topic': input_text}}
        )
        response.raise_for_status()  # Raise error if HTTP status is not 2xx
        data = response.json()
        return data.get('output', 'No output returned')
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except ValueError:
        return "Error: Invalid JSON response"
    
##Streamlit framework

st.title('Langchani with Ollama')
input_text=st.text_input("Write essay on")

if input_text:
    st.write(get_ollama_response(input_text))