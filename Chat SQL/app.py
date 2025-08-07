import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🚀")
st.title("LangChain: Chat with SQL DB 🚀")

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL" 

radio_opt = ["Use SQLLite 3 Database- Student.db", "Connect to you SQL Database"]

selected_opt = st.sidebar.radio(label="Choose the DB which you want chat", options=radio_opt)

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("MySQL Host")
    mysql_user = st.sidebar.text_input("MySQL User")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database")
else:
    db_uri=LOCALDB


api_key = st.sidebar.text_input(label="GROQ API Key", type="password")

if not db_uri:
    st.info("Please enter the database information and uri")
if not api_key:
    st.info("Please add the api key")

## LLM model
llm = ChatGroq(groq_api_key=api_key, model_name= "Llama3-8b-8192", streaming = True)

st.cache_resource(ttl= "2h")
def configure_db(db_uri, mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
    if db_uri==LOCALDB:
        dbfilepath=(Path(__file__).parent/"student.db").absolute()
        print(dbfilepath)
        creater = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creater=creater))
    elif db_uri==MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
    
if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)


## Toolkit
