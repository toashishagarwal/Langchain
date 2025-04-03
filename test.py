from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

chatModel = ChatOpenAI(model="gpt-4", temperature=0.6)
result = chatModel.invoke("write a 5 line poem on Life & its beauty")

print(result.content)
