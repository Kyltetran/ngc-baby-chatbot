import time
import argparse
import os
import shutil
import pandas as pd
from tqdm import tqdm
# from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain_community.vectorstores import Chroma
# from langchain_chroma import Chroma


CHROMA_PATH = "chroma"
DATA_PATH = "data"


def main():
    # Record the start time
    start_time = time.time()

    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true",
                        help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    print("📄 Loading documents...")
    documents = load_documents()

    print(f"📄 Loaded {len(documents)} documents.")
    print("✂️ Splitting documents into chunks...")
    chunks = split_documents(documents)

    print(f"✂️ Split documents into {len(chunks)} chunks.")
    print("📝 Adding chunks to Chroma database...")
    add_to_chroma(chunks)

    # Calculate and print the running time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"✅ Total running time: {elapsed_time:.2f} seconds")


def load_documents():
    """Read all CSV files in the directory and convert them into a list of Document objects."""
    documents = []

    for file_name in os.listdir(DATA_PATH):
        if file_name.endswith(".csv"):
            file_path = os.path.join(DATA_PATH, file_name)
            df = pd.read_csv(file_path, delimiter=';',
                             on_bad_lines='skip')  # Read CSV file
            for _, row in df.iterrows():
                # Create a Document for each row of the CSV
                # Convert row to a dictionary and then to a string
                content = str(row.to_dict())
                document = Document(page_content=content,
                                    metadata={"source": file_name})
                documents.append(document)

    return documents


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=150,
        length_function=len,
        is_separator_regex=False,
    )
    # Use tqdm to show progress during chunking
    chunks = []
    for doc in tqdm(documents, desc="Splitting documents", unit="doc"):
        chunks.extend(text_splitter.split_documents([doc]))
    return chunks


def add_to_chroma(chunks: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        for chunk in tqdm(new_chunks, desc="Adding documents", unit="chunk"):
            chunk_id = chunk.metadata["id"]
            db.add_documents([chunk], ids=[chunk_id])
        # db.persist()
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in tqdm(chunks, desc="Calculating chunk IDs", unit="chunk"):
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    main()
