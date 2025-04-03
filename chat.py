from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

# Get Snowflake connection parameters from environment variables
snowflake_user = os.getenv("SNOWFLAKE_USER")
snowflake_password = os.getenv("SNOWFLAKE_PASSWORD")
snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT")
snowflake_database = os.getenv("SNOWFLAKE_DATABASE")
snowflake_schema = os.getenv("SNOWFLAKE_SCHEMA")
snowflake_warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
snowflake_role = os.getenv("SNOWFLAKE_ROLE")

# Snowflake connection details
snowflake_uri = f"snowflake://{snowflake_user}:{snowflake_password}@{snowflake_account}/{snowflake_database}/{snowflake_schema}?warehouse={snowflake_warehouse}&role={snowflake_role}"

# Connect to the Snowflake database
db = SQLDatabase.from_uri(snowflake_uri)

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

# Get table info for context
table_info = db.get_table_info()

# Create custom SQL generation prompt specifically for Snowflake
sql_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert SQL translator that converts user questions into Snowflake SQL queries.
    
The query will be executed against a Snowflake database with the following schema:
{table_info}

Important guidelines:
- Always use Snowflake SQL syntax
- Include appropriate joins when working with multiple tables
- Use appropriate date and time functions for Snowflake
- Always return columns with clear names (use aliases when necessary)
- Return just the SQL query without explanation or markdown
"""),
    ("human", "{question}")
])

# Create the SQL generation chain
sql_generation_chain = (
    sql_prompt
    | llm
    | StrOutputParser()
)

# Create a prompt for generating natural language responses from SQL results
response_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant that translates SQL query results into natural language.
Given the following:
1. User question: {question}
2. SQL query: {query}
3. SQL response: {response}

Provide a natural language response that answers the user's question based on the SQL results.
Make your answer conversational and easy to understand.
If the SQL result is empty, explain that there are no results matching their criteria.
Do not mention SQL in your response unless the user specifically asks about it."""),
    ("human", "Please answer the question based on the SQL results.")
])

# Function to execute SQL and handle errors
def get_sql_response(query):
    """Execute SQL query and return results"""
    try:
        result = db.run(query)
        return result
    except Exception as e:
        return f"Error executing query: {str(e)}"

# Main function to process user queries
def process_user_query(question):
    # Generate SQL query
    query = sql_generation_chain.invoke({
        "question": question,
        "table_info": table_info
    })
    
    # Execute query
    sql_response = get_sql_response(query)
    
    # Generate natural language response
    final_response = llm.invoke(
        response_prompt.format(
            question=question,
            query=query,
            response=sql_response
        )
    ).content
    
    return {
        "question": question,
        "sql_query": query,
        "sql_response": sql_response,
        "final_response": final_response
    }

# Simple CLI for testing
if __name__ == "__main__":
    print("********************************************************")
    print("Welcome to the Snowflake Query Assistant!")
    print("Ask questions about your data...")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYour question: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye! Have a nice day !!!")
            break
        
        result = process_user_query(user_input)
        print("\nSQL Query:")
        print(result["sql_query"])
        print("\nResponse:")
        print(result["final_response"])
