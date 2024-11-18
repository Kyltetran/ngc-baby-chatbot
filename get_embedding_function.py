# from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
import os

# from dotenv import load_dotenv
# load_dotenv()

import getpass
import os

if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

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


