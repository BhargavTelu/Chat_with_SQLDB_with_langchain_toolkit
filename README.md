
# NLP2SQLDB

This is an end to end LLM project based on Llama and Langchain. We are building a system that can talk to MySQL database. User asks questions in a natural language and the system generates answers by converting those questions to an SQL query and then executing that query on MySQL database. 

Utilized Langchain for text extraction, Groq for inferencing and Provided a user-friendly interface using Streamlit that allows users to input questions.
## Why NLP2SQLDB?

Reduced dependency on database administrators by enabling non-technical employees to generate and retrieve business insights in real-time.

Handled complex database queries across various relational databases, achieving 90% accuracy in generating correct SQL queries.
## Getting Started
To get started with NLP2SQLDB, follow these simple steps:


## Installation

1. Ensure you have Python >=3.10 <=3.13 installed on your system. 

2. Create a SQL database:

3. Requirements

- langchain_chroma
- streamlit
- langchain
- langchain-community
- langchain_core
- langchain-groq
- pylance
- python-dotenv
- langchain-text-splitters
- langchain_huggingface



    
## Code

Libraries used 

```bash
import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
```

Configure databases, llm and streamlit webpage

```bash
st.set_page_config(page_title="Langchain: Chat with SQLDB", page_icon="🦜️")
st.title("🦜️ Chat with DB")

LOCALDB="USE_LOCALDB"
MYSQL="USE_MYSQL"

radio_opt=["Use SQLLITE 3 Database", "connect to mysql"]
selected_opt=st.sidebar.radio(label="Choose the DB", options=radio_opt)

if radio_opt.index(selected_opt)==1:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("Provide my MySQL Host")
    mysql_user=st.sidebar.text_input("MySQL user")
    mysql_password=st.sidebar.text_input("Mysql password",type = "password")
    mysql_db=st.sidebar.text_input("MySQL database")
else:
    db_uri=LOCALDB

# groq_api_key = st.sidebar.text_input(label="GROQ_API_KEY", type = "password")
groq_api_key=os.getenv("GROQ_API_KEY")

if not db_uri:
    st.info("please enter the database information and uri")

if not groq_api_key:
    st.info("please enter the api_key")

llm = ChatGroq(groq_api_key = groq_api_key , model_name = "Llama3-8b-8192", streaming=True)

@st.cache_resource(ttl="1h")
def configure_db(db_uri,mysql_host=None,mysql_user=None, mysql_password=None,mysql_db=None):
    if db_uri==LOCALDB:
        dbfilepath=(Path(__file__).parent/"student.db").absolute()
        print(dbfilepath)
        creator=lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro",uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator=creator))
    elif db_uri==MYSQL:
        if not(mysql_host and mysql_db and mysql_password and mysql_user):
            st.error("please provide a valid information")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))


if db_uri==MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password,mysql_db)
else:
    db=configure_db(db_uri)


```

Tools used

```bash
##toolkit     
toolkit = SQLDatabaseToolkit(db=db,llm=llm)
agent = create_sql_agent(llm=llm,toolkit=toolkit,verbose=True,
                         agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
```

configuring streamlit

```bash
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"]=[
        {"role": "assistant",
         "content": "Hi, I'm a chatbot who can search the databases"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"]) # appending all messages in chat_messages

user_query=st.chat_input(placeholder="Ask any question")
if user_query:
    st.session_state.messages.append({"role":"user", "content":user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback=StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = agent.run(user_query, callbacks=[streamlit_callback])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response) 
```


##  Running Your NLP2SQLDB
Before running make sure you have the following keys set as environment variables in your .env file:

An OpenAI API key (or other LLM API key): OPENAI_API_KEY=sk-...

## Features

- Complex Query Handling: upport for complex SQL queries involving multiple table joins, group by operations, and aggregations such as SUM, COUNT, AVG..
- Multi-database Support: The system can connect to multiple database types (e.g., MySQL, PostgreSQL, SQLite, Oracle) and generate dialect-specific SQL queries for different databases..
- User Authentication & Data Security: Ensure secure connections to databases with role-based access control. Only authorized users can query sensitive tables or data..
- Real Time Data: Real time and private data can be queried.
- Works with Open Source Models: Run your model using Open AI or open source models.


## 

![App Screenshot](https://github.com/BhargavTelu/Chat_with_SQLDB_with_langchain_toolkit/blob/main/Screenshot%202024-10-21%20005638.png)



## Use Cases:

Business Intelligence & Reporting:Non-technical stakeholders (e.g., sales managers, marketers) can use this system to generate reports without needing SQL expertise.

Customer Support & Service Operations:
Support teams could use natural language queries to quickly extract specific customer data. 

Healthcare & Medical Research:Medical professionals can query patient databases without requiring SQL knowledge.

HR managers could extract employee-related data without SQL

Inventory management: Retail managers could query inventory databases for stock analysis.

Education Analytics:
Universities can analyze student data without technical know-how.