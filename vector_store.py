from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

def get_user_vectorstore(user_id: str):
    return Chroma(
        collection_name=f"memos_{user_id}",
        embedding_function=OpenAIEmbeddings(),
        persist_directory="./chroma"
    )
# Placeholder for vector store setup and retrieval
