import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
import matplotlib.pyplot as plt
from langchain_community.agent_toolkits.file_management.toolkit import FileManagementToolkit
from  langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langsmith.wrappers import wrap_openai
from langsmith import traceable
from langchain_community.utilities import SQLDatabase, GoogleSerperAPIWrapper
import openai

# load_dotenv()

# app config
st.set_page_config(page_title="predictED", page_icon="🧑‍🎓")
st.header(' Welcome to predictED, your copilot for EdTech data insights.')

'''
A Gen AI-powered data analysis app for edtech founders. Perform SQL queries, generate visualizations, and receive AI-driven insights from student data to enhance educational outcomes. Ideal for identifying trends and making informed decisions.\n
\n
Example questions:\n
What is the average engagement score for Course ID 102 during the last month?\n
How many students have dropped out from each course this year?\n
Can you show a bar chart of the average performance score by course?\n
'''
# Sidebar for taking openai input
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Enter an OpenAI API Key to continue")
    st.stop()


# Auto-trace LLM calls in-context
client = wrap_openai(openai.Client(api_key=openai_api_key))

db = SQLDatabase.from_uri('sqlite:///edtech.db')

llm = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo')

# print(llm)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# ----------------------------------------------------
# Creating the tools
# ----------------------------------------------------

working_directory  = os.getcwd()
tools = FileManagementToolkit(
    root_dir=str(working_directory),
    selected_tools=["read_file", "write_file", "list_directory"],).get_tools()
tools.append(
    PythonREPLTool())
tools.extend(SQLDatabaseToolkit(db=db, llm=llm).get_tools())

# agent = initialize_agent(
#     tools, llm, agent= AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
# )

# ----------------------------------------------------
# Define the prompt
# ----------------------------------------------------

# Define the prompt 
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

# Creating the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", human),
    ]
)

agent = create_structured_chat_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# agent = initialize_agent(
#     tools, llm, agent= AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
# )

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="Ask me anything!")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query}) # Save the user query in the message history
    st.chat_message("user").write(user_query) # Display the user query in the chat
    
    with st.chat_message("assistant"): 
        st_cb = StreamlitCallbackHandler(st.container()) # Create a Streamlit callback handler
        # response = agent.run(user_query, callbacks = [st_cb]) # Response is the last statement in the agent's execution
        
        response = agent_executor.invoke({"input": user_query}) # Response is the last statement in the agent's execution
        
        print('-------------\n', response)
        print(type(response))
        # Adding extra logic for matplotlibs or text
        if "data.png" in response.values():  # If the response is a Matplotlib Figure
            # st.pyplot(response)
            image_path = os.path.join(working_directory, 'data.png')
            st.image(image_path)
            # st.session_state.messages.append({"role": "assistant", "content": response['output']})
            # st.write(response['output'])

        else:  # If the response is text
            st.session_state.messages.append({"role": "assistant", "content": response['output']})
            st.write(response['output'])




# def get_response(user_query, chat_history):

#     template = """
#     You are a helpful assistant. Answer the following questions considering the history of the conversation:

#     Chat history: {chat_history}

#     User question: {user_question}
#     """

#     prompt = ChatPromptTemplate.from_template(template)

#     llm = ChatOpenAI()
        
#     chain = prompt | llm | StrOutputParser()
    
#     return chain.invoke({
#         "chat_history": chat_history,
#         "user_question": user_query,
#     })
    
# # conversation
# for message in st.session_state.chat_history:
#     if isinstance(message, AIMessage):
#         with st.chat_message("AI"):
#             st.write(message.content)
#     elif isinstance(message, HumanMessage):
#         with st.chat_message("Human"):
#             st.write(message.content)

# # user input
# user_query = st.chat_input("Type your message here...")
# if user_query is not None and user_query != "":
#     st.session_state.chat_history.append(HumanMessage(content=user_query))

#     with st.chat_message("Human"):
#         st.markdown(user_query)

#     with st.chat_message("AI"):
#         response = get_response(user_query, st.session_state.chat_history)
#         st.write(response)

#     st.session_state.chat_history.append(AIMessage(content=response))

