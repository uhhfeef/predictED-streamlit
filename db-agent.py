import os
from dotenv import load_dotenv

load_dotenv()

#os.environ["HUGGINGFACEHUB_API_TOKEN"]
from langchain.agents import create_sql_agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from  langchain_experimental.tools.python.tool import PythonREPLTool
# from  langchain_experimental.python import PythonREPL
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.agents import AgentExecutor, create_structured_chat_agent

llm = OpenAI()
model = ChatOpenAI()
db = SQLDatabase.from_uri('sqlite:///edtech.db')
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

# agent_executor.run("how many student records are in the database?")
# agent_executor.run('what is the total number of tracks and the average length of tracks by genre?')

working_directory  = os.getcwd()
tools = FileManagementToolkit(
    root_dir=str(working_directory),
    selected_tools=["read_file", "write_file", "list_directory"],).get_tools()
tools.append(
    PythonREPLTool())
tools.extend(SQLDatabaseToolkit(db=db, llm=llm).get_tools())

context = toolkit.get_context()
print('-----------------\n', context)
print('-----------------\n', toolkit.get_tools())


# model = ChatOpenAI()
agent = initialize_agent(
    tools, model, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
# print(agent.agent)
# agent.run("Based on the data, what three strategic changes would you recommend for improving overall student success rates next year?")


