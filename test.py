from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
from langchain import hub
from langchain_community.chat_models import ChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.agent_toolkits.file_management.toolkit import FileManagementToolkit
import os 
from  langchain_experimental.tools.python.tool import PythonREPLTool
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import matplotlib.pyplot as plt


load_dotenv()

# Fetching the prompt from the hub
# prompt = hub.pull("hwchase17/structured-chat-agent")

# Define the prompt - TESTING
system = '''Respond to the human as helpfully and accurately as possible. You have access to the following tools:

{tools}

Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or {tool_names}

Provide only ONE action per $JSON_BLOB, as shown:

```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```

Follow this format:

Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}

Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation.
Use the repltool to create matplotlib charts if the user is asking for a graph, plot, pie chart, etc. If you're using python repl tool, Instead of using plt.show() in your REPL tool input, which attempts to display the plot in an interactive window (not suitable for non-interactive environments like servers or certain REPL setups), you should save the plot to a file and strictly call in "data.png". Even if the user says "show me the plot", you should still return "data.png" as the response. NEVER RUN plt.show() in the REPL tool input.

'''

human = '''{input}

{agent_scratchpad}

(reminder to respond in a JSON blob no matter what)'''

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", human),
    ]
)


db = SQLDatabase.from_uri("sqlite:///edtech.db")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# python_repl = PythonREPL()
# # You can create the tool to pass to an agent
# repl_tool = Tool(
#     name="python_repl",
#     description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
#     func=python_repl.run,
# ) # create the tool repl_tool

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

working_directory  = os.getcwd()
tools = FileManagementToolkit(
    root_dir=str(working_directory),
    selected_tools=["read_file", "write_file", "list_directory"],).get_tools()
tools.append(
    PythonREPLTool())
tools.extend(SQLDatabaseToolkit(db=db, llm=llm).get_tools())



agent = create_structured_chat_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# agent_executor.invoke({"input": "show me a graph of the top 3 students by performance score from edtech.db"})

# print(prompt)
# Locate the template part


# agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

# agent_executor.invoke(
#     "List the total number of entries?"
# )

res = {
    "input": "show me the graph for the top 3 students based on performance from edtech.db",
    "output": "data.png"
}

print(res["output"])