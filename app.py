import os
from langchain.agents import *
import pandas as pd 
from langchain_experimental.agents.agent_toolkits import create_csv_agent
# from langchain_community.agent_toolkits.json.base import create_json_agent
from langchain_openai import ChatOpenAI



df = pd.read_csv('EdTech_Sample_Data.csv')

# llm = ChatOpenAI(temperature=0.1,model="gpt-3.5-turbo")
llm = ChatOpenAI(temperature=0.1,model="gpt-4-turbo")
agent_executer = create_csv_agent(llm, 'EdTech_Sample_Data.csv', verbose=True, allow_dangerous_code=True)

agent_executer.invoke("Can you tell me the trend in student performance over the last 2 years?")

