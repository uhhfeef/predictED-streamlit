import streamlit as st

def setup_streamlit():
    st.set_page_config(page_title="predictED", page_icon="🧑‍🎓")
    st.header(' Welcome to predictED, your copilot for EdTech data insights.')
    
    st.markdown('''
    A Gen AI-powered data analysis app for edtech founders. Perform SQL queries, generate visualizations, and receive AI-driven insights from student data to enhance educational outcomes. Ideal for identifying trends and making informed decisions.

    Example questions:
    - What percentage of students completed their courses?
    - How many students have dropped out from each course this year?
    - Can you show a bar chart of the average performance score by course ID?
    ''')
