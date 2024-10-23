import os
from langchain_community.agent_toolkits.file_management.toolkit import FileManagementToolkit

def get_file_management_tools():
    working_directory = os.getcwd()
    return FileManagementToolkit(
        root_dir=str(working_directory),
        selected_tools=["read_file", "write_file", "list_directory"],
    ).get_tools()
