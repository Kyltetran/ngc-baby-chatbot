import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from get_embedding_functions import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Trả lời theo ngôn ngữ giống thông tin dưới đây:

{context}

---

Hãy trả lời câu hỏi dựa vào thông tin trên: {question}, trích dẫn đúng thông tin từ dữ liệu trong câu trả lời (bao gồm tên tác giả, ngày xuất bản, số báo). Nếu không tìm được thông tin trong dữ liệu trên, ghi: "Thông tin không bao gồm, vui lòng thử lại". Nếu tìm được thông tin, hãy trả lời theo giọng văn của một cây viết nữ của báo Nữ giới chung ở năm 1918.
"""


def query_rag(query_text: str):
    db = Chroma(persist_directory=CHROMA_PATH,
                embedding_function=get_embedding_function())
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOpenAI(model="gpt-4o")
    response_text = model.invoke(prompt).content

    print("Response:", response_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_rag(args.query_text)
