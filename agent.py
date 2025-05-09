import os
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# Set your API key - replace with your actual environment variable or key management
# Ensure you have set the appropriate environment variable (e.g., OPENAI_API_KEY, GOOGLE_API_KEY)
# Example (replace with your actual method for managing API keys):
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Initialize the language model
# Using a chat model, but any runnable that processes text can be used.
try:
   # Example for OpenAI
   llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
   print(f"Language model initialized: {llm.model_name}")
except Exception as e:
   print(f"Error initializing language model: {e}")
   print("Please ensure your API key is set correctly and the model name is valid.")
   llm = None # Set llm to None if initialization fails

# --- Define Independent Tasks (Simulated Workflows) ---
# These represent tasks that can be executed in parallel.
# In a real scenario, these might be calls to different APIs, tools, or separate chains.

# Task 1: Summarize the topic
summarize_prompt = ChatPromptTemplate.from_messages([
   ("system", "Summarize the following topic concisely:"),
   ("user", "{topic}")
])
summarize_chain = summarize_prompt | llm | StrOutputParser()

# Task 2: Generate related questions
questions_prompt = ChatPromptTemplate.from_messages([
   ("system", "Generate three interesting questions about the following topic:"),
   ("user", "{topic}")
])
questions_chain = questions_prompt | llm | StrOutputParser()

# Task 3: Identify key terms
terms_prompt = ChatPromptTemplate.from_messages([
   ("system", "Identify 5-10 key terms from the following topic, separated by commas:"),
   ("user", "{topic}")
])
terms_chain = terms_prompt | llm | StrOutputParser()

# --- Combine Tasks for Parallel Execution using RunnableParallel ---
parallel_tasks = RunnableParallel({
   "summary": summarize_chain,
   "questions": questions_chain,
   "key_terms": terms_chain
})

# --- Create a chain that combines the original input with parallel results ---
# This approach uses a dictionary that merges inputs and outputs correctly
def combine_inputs_and_parallel_results(inputs):
    # inputs here is just the topic string
    return {
        "topic": inputs,  # Keep the original topic
        # The rest will be filled by parallel_tasks
    }

# --- Define a Final Synthesis Step ---
synthesis_prompt = ChatPromptTemplate.from_messages([
   ("system", """Based on the following information about a topic:

   Summary: {summary}

   Related Questions: {questions}

   Key Terms: {key_terms}

   Synthesize a comprehensive answer that includes the summary, lists the related questions, and mentions the key terms."""),
   ("user", "Original topic: {topic}") # Include the original topic for context
])

# --- Build the Full Chain ---
# First, we run the parallel tasks
# Then, we combine the results with the original topic
# Finally, we use that combined data for synthesis
full_parallel_chain = (
    RunnableParallel({
        "topic": RunnablePassthrough(),  # Pass through the original topic
        "parallel_results": parallel_tasks  # Run all parallel tasks
    })
    .assign(  # Restructure the data for the synthesis prompt
        summary=lambda x: x["parallel_results"]["summary"],
        questions=lambda x: x["parallel_results"]["questions"],
        key_terms=lambda x: x["parallel_results"]["key_terms"]
    )
    | synthesis_prompt | llm | StrOutputParser()
)

# --- Run the Chain ---
async def run_parallel_example(topic: str):
   """Runs the parallel LangChain example with a given topic."""
   if not llm:
       print("LLM not initialized. Cannot run example.")
       return

   print(f"\n--- Running Parallel LangChain Example for Topic: '{topic}' ---")
   # Invoke the chain asynchronously
   try:
       response = await full_parallel_chain.ainvoke(topic)
       print("\n--- Final Response ---")
       print(response)
   except Exception as e:
       print(f"\nAn error occurred during chain execution: {e}")

# Run the example with a test topic
if __name__ == "__main__":
   test_topic = "Artificial Intelligence"
   # Run the asynchronous function
   asyncio.run(run_parallel_example(test_topic))

   test_topic_2 = "Renewable Energy"
   asyncio.run(run_parallel_example(test_topic_2))

   
