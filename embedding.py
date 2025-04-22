from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def store_memo_in_vector_store(doc_id: str, title: str, content: str, user_id: str, last_modified: str):
    # Split content into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(content)

    documents = [
        Document(
            page_content=chunk,
            metadata={
                "doc_id": doc_id,
                "title": title,
                "last_modified": last_modified
            }
        )
        for chunk in chunks
    ]

    # Each user has their own collection
    collection_name = f"memos_{user_id}"
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=OpenAIEmbeddings(),
        persist_directory="./chroma"
    )

    vectorstore.add_documents(documents)
    vectorstore.persist()
# Placeholder for embedding logic with OpenAI
