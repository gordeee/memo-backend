from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

def ask_about_memos(question: str, user_id: str):
    # Load user-specific vector store
    collection = f"memos_{user_id}"
    vectorstore = Chroma(
        collection_name=collection,
        embedding_function=OpenAIEmbeddings(),
        persist_directory="./chroma"
    )

    llm = OpenAI(model="gpt-4", temperature=0.3)

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True
    )

    result = chain({"query": question})
    sources = result.get("source_documents", [])

    return {
        "answer": result["result"],
        "sources": [doc.metadata.get("doc_id") for doc in sources],
        "timestamps": {
            doc.metadata.get("doc_id"): doc.metadata.get("last_modified")
            for doc in sources if doc.metadata.get("last_modified")
        }
    }
