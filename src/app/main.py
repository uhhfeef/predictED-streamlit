import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
import matplotlib.pyplot as plt
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents import AgentExecutor
from langsmith.wrappers import wrap_openai
from langchain_community.utilities import SQLDatabase
import openai

# Import configurations
from config.config import OPENAI_API_KEY, DB_URI
from src.app.streamlit_config import setup_streamlit
from src.db_agent import create_db_agent
from src.file_management import get_file_management_tools

# Load environment variables
load_dotenv()

# Set up Streamlit
setup_streamlit()

# Sidebar for taking OpenAI input
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=OPENAI_API_KEY)
if not openai_api_key:
    st.info("Enter an OpenAI API Key to continue")
    st.stop()

# Auto-trace LLM calls in-context
client = wrap_openai(openai.Client(api_key=openai_api_key))

# Set up database
db = SQLDatabase.from_uri(DB_URI)

# Set up LLM
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")

# Create tools
tools = get_file_management_tools()
tools.append(PythonREPLTool())
tools.extend(SQLDatabaseToolkit(db=db, llm=llm).get_tools())

# Create agent
agent = create_db_agent(llm, tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, max_iterations=25, verbose=True)

# Streamlit UI
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="Ask me anything!")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)
    
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke({"input": user_query})
        
        print('-------------\n', response)
        print(type(response))
        
        if "data.png" in str(response):
            image_path = os.path.join(os.getcwd(), 'data.png')
            st.image(image_path)
        else:
            st.session_state.messages.append({"role": "assistant", "content": response['output']})
            st.write(response['output'])
