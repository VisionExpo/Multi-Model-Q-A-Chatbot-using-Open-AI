from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

## Langsmith Tracing
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "ollama-chatbot"

## Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please answer the user's questions."),
        ("user", "Question:{question}"),
    ]
)

def generate_response(question, engine, temperature, max_tokens):
    llm = OllamaLLM(model=engine, temperature=temperature, num_predict=max_tokens)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"question": question})
    return answer

## Title of the app
st.title("Multi-Model Q&A Chatbot")

## Sidebar for settings
st.sidebar.title("Settings")

## Dropdown for model selection
llm = st.sidebar.selectbox(
    "Select Language Model",
    options=["gemma:2b", "deepseek-r1:7b"])

## Adjust response parameters
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 300, 150)


## Main Interface for user input
st.write("## Ask a Question")
user_input = st.text_input("You: ")
if user_input:
    response = generate_response(user_input, llm, temperature, max_tokens)
    st.write("### AI Assistant:")
    st.write(response)
else:
    st.write("Please enter a question to get started.")

