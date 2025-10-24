from flask import Flask, jsonify, request, render_template, session
# from flask_cors import CORS
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from get_embedding_function import get_embedding_function
import os


app = Flask(__name__)
# CORS(app)
app.secret_key = '123456'

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Trả lời theo ngôn ngữ giống thông tin dưới đây:

{context}

---

Hãy nêu quan điểm dựa vào thông tin trên: {question}, trích dẫn đúng thông tin từ dữ liệu trong câu trả lời (bao gồm tên tác giả, ngày xuất bản, số báo). Nếu không tìm được thông tin trong dữ liệu trên, ghi: "Thông tin không bao gồm, vui lòng thử lại". Nếu tìm được thông tin, hãy trả lời theo giọng văn của một cây viết nữ của báo Nữ giới chung ở năm 1918.
"""


@app.route('/')
def index():
    session.clear()
    return render_template('index.html')


@app.route('/api/query', methods=['POST'])
def api_query():
    data = request.json
    query_text = data.get('query_text', '')
    print("Received query:", query_text)

    db = Chroma(persist_directory=CHROMA_PATH,
                embedding_function=get_embedding_function())
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOpenAI(model="gpt-4o")
    response_text = model.invoke(prompt).content

    return jsonify({"response": response_text})


# check server health
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Server is running fine!",
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# if __name__ == "__main__":
#     app.run()
