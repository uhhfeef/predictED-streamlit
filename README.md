# predictED
## Overview
predictED is a Gen AI-powered data analysis application designed for EdTech founders. It allows users to perform SQL queries, generate visualizations, and receive AI-driven insights from student data to enhance educational outcomes. The application is built using Python and Streamlit, leveraging various libraries for data manipulation and visualization.
## Features
- Interactive SQL Queries: Users can input SQL queries to analyze student data.
- Data Visualization: Generate visualizations based on the queried data.
- AI-Driven Insights: Utilize OpenAI's language model to provide insights and answer user queries.
- User-Friendly Interface: Built with Streamlit for an intuitive user experience.
## Technologies Used
- Python: The primary programming language.
- Streamlit: For building the web application interface.
- LangChain: For integrating language models and tools.
- OpenAI: For AI-driven insights and responses.
- Matplotlib: For data visualization.
- SQLAlchemy: For database interactions.
- dotenv: For managing environment variables.
## Installation
1. Clone the Repository
2. Create a Virtual Environment
3. Install Dependencies
4. Set Up Environment Variables
   - Create a .env file in the root directory and add the following:
## Usage
- Run the Application
- Access the Application
   - Open your web browser and go to http://localhost:8501.
## Code Structure
- src/
  - app/
    - main.py: The main application file that initializes the Streamlit app and handles user interactions.
    - streamlit_config.py: Contains the configuration settings for the Streamlit app.
    - db_agent.py: Contains functions to create a database agent for handling SQL queries.
    - file_management.py: Provides tools for file management operations.
  - config/
    - config.py: Loads environment variables and contains configuration settings.
  - requirements.txt: Lists all the dependencies required for the project.

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (git checkout -b feature/YourFeature).
3. Make your changes and commit them (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/YourFeature).
5. Open a pull request.
