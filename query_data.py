import argparse
# from langchain.vectorstores.chroma import Chroma
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
# from langchain_ollama.llms import OllamaLLM
# from langchain_anthropic import AnthropicLLM
# from langchain_core.prompts import PromptTemplate
# from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Trả lời theo ngôn ngữ giống thông tin dưới đây:

{context}

---

Hãy trả lời câu hỏi dựa vào thông tin trên: {question}, trích dẫn đúng thông tin từ dữ liệu trong câu trả lời (bao gồm tên tác giả, ngày xuất bản, số báo). Nếu không tìm được thông tin trong dữ liệu trên, ghi: "Thông tin không bao gồm, vui lòng thử lại". Nếu tìm được thông tin, hãy trả lời theo giọng văn của một cây viết nữ của báo Nữ giới chung ở năm 1918.
"""

import os
from getpass import getpass

# if "ANTHROPIC_API_KEY" not in os.environ:
#     os.environ["ANTHROPIC_API_KEY"] = getpass()

# headers = {
#     "Content-Type": "application/json",
#     "x-api-key": "ANTHROPIC_API_KEY" # Changed the Authorization header to x-api-key and removed the Bearer prefix.
# }
# print(os.environ["ANTHROPIC_API_KEY"])

# Set the API key if not already set
if "OPEN_API_KEY" not in os.environ:
    os.environ["OPEN_API_KEY"] = getpass("Enter your Open API Key: ")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ['OPEN_API_KEY']}"
}
print(os.environ["OPEN_API_KEY"])


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    # Prepare the context text from the search results
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    # Run the model
    model = ChatOpenAI(model="gpt-4o")
    response_text = model.invoke(prompt).content

    # Format the sources to show content instead of metadata
    formatted_sources = [f"{doc.metadata.get('id', 'Unknown Source')}: {doc.page_content}" for doc, _score in results]

    # Combine response with formatted sources
    formatted_response = f"Response: {response_text}\nSources:\n" + "\n\n".join(formatted_sources)
    print(formatted_response)
    return response_text


from flask import Flask, jsonify, request, render_template, session

app = Flask(__name__)
app.secret_key = '123456'

@app.route('/')
def index():
    session.clear()  # Clear the session when starting a new conversation
    return render_template('index.html')

if __name__ == "__main__":
    main()
