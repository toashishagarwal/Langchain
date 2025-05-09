# Langchain
Langchain Tutorials

# Setup Instructions (for mac)
1. Create a python virtual environment <br>
<mark>python3 -m venv venv</mark>

2. Activate the virtual env<br>
<mark>source venv/bin/activate</mark>

3. Install the dependencies from requirements.txt <br>
<mark>pip3 install -r requirements.txt</mark>


# 1. Chat App
This Python-based app uses OpenAI APIs to connect to the configured Snowflake instance. It uses chaining to convert - <br>
English Text -> Snowflake SQL -> Execute SQL -> Return results <br>
Currently the app is console-driven. However it can be easily extended to have a UI built in Streamlit by adding relevant dependencies to the requirements.txt file

## Run the python code
python3 chat.py

# 2. AI Agent
In addition to Prompt Chaining and Routing, Langchain supports creation of AI agents using Parallel execution of subtasks. Implementing parallelization involves support for async execution or multi-threading. Today's agentic frameworks support async operations. In Langchain, it is supported via the LangChain Expression Language (LCEL), where you can define lists of runnables or dictionaries.
This example demonstrates creation of a simple LangChain chain that takes a user query and simultaneously performs two independent "tasks" (simulated by simple chains or functions) before combining their results.

## Run the python code
python3 agent.py




