import streamlit as st
import openai
import sqlite3

# Set your OpenAI API key
openai.api_key = "sk-proj-IjPyzDtIihJRTN3uuwJuT3BlbkFJi2L0sOH72KqtFCmYUIfA"

# Connect to your SQLite database
conn = sqlite3.connect('D:\Vkaps Internship\ChatWDB\chinook.db')
cursor = conn.cursor()

# Function to execute SQL queries
def execute_sql_query(query):
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        return f"An error occurred: {e}"

# Function to interact with the language model
def chat_with_language_model(user_input):
    try:
        # Use GPT-3 to generate a response based on user input
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )

        # Extract the generated response
        generated_text = response.choices[0].message['content']
        return generated_text
    except Exception as e:
        return f"An error occurred: {e}"

# Main function for the chatbot
def main():
    st.title("Chat with your SQL Dataset ")
    st.write("Type your queries or messages in the box below.")

    user_input = st.text_input("You:")
    
    if st.button("Send"):
        if user_input.strip() == '':
            st.warning("Please enter a message.")
        else:
            # Check if the input contains SQL-related keywords
            sql_keywords = ['select', 'from', 'where', 'order by', 'group by', 'join']
            if any(keyword in user_input.lower() for keyword in sql_keywords):
                # If the input is an SQL-related query, directly query the database
                response_text = execute_sql_query(user_input)
                st.write(f"Bot: {response_text}")
            else:
                # If the input is not an SQL-related query, interact with the language model
                response_text = chat_with_language_model(user_input)
                st.write(f"Bot: {response_text}")

if __name__=="__main__":
    main()

conn.close()

