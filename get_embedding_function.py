# from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
import os

from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get the API key from the environment
OPEN_API_KEY = os.getenv("OPEN_API_KEY_2")

if not OPEN_API_KEY:
    raise ValueError("OPEN_API_KEY is not set in the environment.")
print("API Key loaded successfully.")

def get_embedding_function():
    # embeddings = OllamaEmbeddings(
    #     model="llama3.2",
    # )
    # # embeddings = OllamaEmbeddings(model="nomic-embed-text")0
    # return embeddings

    # Get the API key from environment variables
    # api_key = os.getenv("OPEN_API_KEY")
    # print("Loaded API Key:", os.getenv("OPEN_API_KEY"))
    # if not api_key:
    #     raise ValueError("OpenAI API key not found in environment variables.")

    embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            # openai_api_key=api_key
        )
        # embeddings = OllamaEmbeddings(model="nomic-embed-text")0
    return embeddings


