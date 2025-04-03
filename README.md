# Langchain
Langchain Tutorials

# Setup Instructions (for mac)
1. Create a python virtual environment <br>
<mark>python3 -m venv venv</mark>

2. Activate the virtual env<br>
<mark>source venv/bin/activate</mark>

3. Install the dependencies from requirements.txt <br>
<mark>pip3 install -r requirements.txt</mark>

# Run the python code
python3 chat.py

# About Chat App
This Python-based app uses OpenAI APIs to connect to the configured Snowflake instance. It uses chaining to convert - <br>
English Text -> Snowflake SQL -> Execute SQL -> Return results <br>
Currently the app is console-driven. However it can be easily extended to have a UI built in Streamlit by adding relevant dependencies to the requirements.txt file





