import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Multi-Model-Q-A-Chatbot"


## Prompt Template

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant that answers questions based on the provided context. Please provide concise and accurate answers."),
        ("user", "Question: {question}")
    ]
)


def generate_response(question,api_key,llm,temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm, api_key=api_key, temperature=temperature, max_tokens=max_tokens)
    output_parser = StrOutputParser()
    chain= prompt | llm | output_parser
    answer = chain.invoke({"question": question})
    return answer

## Title of the app
st.title("Multi-Model Q&A Chatbot")

## Sidebar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

## Dropdown for model selection
llm = st.sidebar.selectbox(
    "Select Language Model",
    options=["gpt-3.5-turbo", "gpt-4o", "gpt-4", "gpt-4-1106-preview"])

## Adjust response parameters
temparature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 300, 150)


## Main Interface for user input
st.write("## Ask a Question")
user_input = st.text_input("You: ")

if user_input:
    response = generate_response(user_input,api_key,llm,temparature, max_tokens)
    st.write("### AI Assistant:")
    st.write(response)
else:
    st.write("Please enter a question to get started.")