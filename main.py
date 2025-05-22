from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import argparse
import os
from getpass import getpass
from flask import Flask, jsonify, request, render_template, session
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
# from get_embedding_function import get_embedding_function
import json

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Trả lời theo ngôn ngữ giống thông tin dưới đây:

{context}

---

Hãy nêu quan điểm dựa vào thông tin trên: {question}, trích dẫn đúng thông tin từ dữ liệu trong câu trả lời (bao gồm tên tác giả, ngày xuất bản, số báo). Nếu không tìm được thông tin trong dữ liệu trên, ghi: "Thông tin không bao gồm, vui lòng thử lại". Nếu tìm được thông tin, hãy trả lời theo giọng văn của một cây viết nữ của báo Nữ giới chung ở năm 1918.
"""


# Load environment variables from .env
load_dotenv()

# Get the API key from the environment
OPEN_API_KEY = os.getenv("OPEN_API_KEY")

if not OPEN_API_KEY:
    raise ValueError("OPEN_API_KEY is not set in the environment.")
print("API Key loaded successfully.")

app = Flask(__name__)
app.secret_key = '123456'


def get_embedding_function():
    # embeddings = OllamaEmbeddings(
    #     model="llama3.2",
    # )
    # # embeddings = OllamaEmbeddings(model="nomic-embed-text")0
    # return embeddings

    # Get the API key from the environment
    OPEN_API_KEY = os.getenv("OPEN_API_KEY")

    if not OPEN_API_KEY:
        raise ValueError("OPEN_API_KEY is not set in the environment.")
    print("API Key loaded successfully.")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        # openai_api_key=api_key
    )
    # embeddings = OllamaEmbeddings(model="nomic-embed-text")0
    return embeddings


# Define the route for the frontend
@app.route('/')
def index():
    session.clear()  # Clear the session when starting a new conversation
    return render_template('index.html')

# Define the API endpoint to handle queries


@app.route('/api/query', methods=['POST'])
def api_query():
    data = request.json
    query_text = data.get('query_text', '')
    print("Received query:", query_text)

    # Prepare the DB
    db = Chroma(persist_directory=CHROMA_PATH,
                embedding_function=get_embedding_function())
    print("Database initialized")

    # Search the DB
    results = db.similarity_search_with_score(query_text, k=5)
    print("Search results:", results)

    # Prepare the prompt and context
    context_text = "\n\n---\n\n".join(
        [doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Run the model
    model = ChatOpenAI(model="gpt-4o")
    response_text = model.invoke(prompt).content

    # Extract sources
    # formatted_sources = [f"{doc.metadata.get('id', 'Unknown Source')}: {doc.page_content}" for doc, _score in results]

    # Combine response with formatted sources
    # sources = f"Response: {response_text}\nSources:\n" + "\n\n".join(formatted_sources)

    # Extract sources with full metadata
    # sources = [
    #     {
    #         "metadata": doc.metadata,
    #         "content": doc.page_content
    #     } for doc, _score in results
    # ]

    # sources = [doc.metadata.get("id", None) for doc, _score in results]
    response = {
        "response": response_text,
        # "sources": sources
    }
    return jsonify(response)


if __name__ == "__main__":
    # Get the PORT from the environment (default to 5000 if not set)
    port = int(os.environ.get("PORT", 6000))
    # Run the app on all available IPs (0.0.0.0) and the specified port
    app.run(host="0.0.0.0", port=port, debug=True)

# if __name__ == "__main__":
#     app.run(debug=True)
