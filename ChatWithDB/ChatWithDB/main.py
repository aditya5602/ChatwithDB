import openai
import sqlite3


openai.api_key = "sk-proj-IjPyzDtIihJRTN3uuwJuT3BlbkFJi2L0sOH72KqtFCmYUIfA"

# Connect to SQLite 
conn = sqlite3.connect('D:\Vkaps Internship\ChatWDB\chinook.db')
cursor = conn.cursor()

#  execute SQL queries
def execute_sql_query(query):
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        return f"An error occurred: {e}"

#  interact with the language model
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
    

# Main loop for the chatbot
def main():
    print("Enter your question. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        # Check if the input contains SQL-related keywords
        sql_keywords = ['select', 'from', 'where', 'order by', 'group by', 'join']
        if any(keyword in user_input.lower() for keyword in sql_keywords):
            # If the input is an SQL-related query, directly query the database
            response_text = execute_sql_query(user_input)
        else:
            # If the input is not an SQL-related query, interact with the language model
            response_text = chat_with_language_model(user_input)
        
        print(f"Bot: {response_text}")

if __name__ =="__main__":
    main()

# Close the database connection when done
conn.close()
