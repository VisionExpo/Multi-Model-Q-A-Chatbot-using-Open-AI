import streamlit as st
import os
import time
from typing import List, Dict
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

from dotenv import load_dotenv

load_dotenv()

# Validate environment variables
groq_api_key = os.getenv('GROQ_API_KEY')
openai_key = os.getenv('OPENAI_API_KEY')

if not all([groq_api_key, openai_key]):
    raise ValueError("Missing required environment variables. Please check .env file")

llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

SYSTEM_PROMPT = f"""
You are an expert document analyst. Answer questions based only on the provided context.
Follow these rules:
1. Provide accurate, concise responses
2. Cite sources using page numbers when available
3. If unsure, state that information isn't available in the documents
4. Maintain a professional, technical tone
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT.strip()),
    ("user", """\
<context>
{context}
</context>

Question: {input}""")
])

def load_and_process_documents() -> List:
    """Load and split PDF documents from research_papers directory."""
    loader = PyPDFDirectoryLoader("research_papers", glob="**/*.pdf")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return text_splitter.split_documents(docs[:50])

def create_vector_embeddings():
    """Initialize or retrieve cached vector embeddings."""
    if "vectors" not in st.session_state:
        st.session_state.embeddings = OpenAIEmbeddings()
        st.session_state.final_docs = load_and_process_documents()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_docs = st.session_state.text_splitter.split_documents(st.session_state.docs[:50])
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_docs, st.session_state.embeddings)

st.title("RAG Document Q&A with GROQ API and Llama3")

user_prompt = st.text_input("Enter your question here", placeholder="What is the main topic of the document?")

col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Initialize Vector Database"):
        with st.spinner("Processing documents..."):
            create_vector_embeddings()
            st.success("Vector database ready!")
with col2:
    if st.button("🧹 Clear Cache", help="Reset all cached resources"):
        st.session_state.clear()
        st.rerun()

import time

if user_prompt:
    if "vectors" not in st.session_state:
        st.warning("Please initialize vector database first!")
        st.stop()
        
    try:
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = st.session_state.vectors.as_retriever(search_kwargs={"k": 3})
        retriever_chain = create_retrieval_chain(retriever, document_chain)
        
        with st.spinner("Analyzing documents..."):
            start = time.perf_counter()
            response = retriever_chain.invoke({"input": user_prompt})
            response_time = time.perf_counter() - start
            
        st.caption(f"Response generated in {response_time:.2f} seconds")

    st.write(response['answer'])

    ## with streamlit expander

    with st.expander("🔍 Source Documents"):
        st.subheader("Most Relevant Contexts")
        for i, doc in enumerate(response['context'], 1):
            page_num = doc.metadata.get('page', 'N/A')
            source = doc.metadata.get('source', 'Unknown')
            st.markdown(f"**Document {i}** (Page {page_num}, {os.path.basename(source)})")
            st.caption(doc.page_content)
            st.divider()
