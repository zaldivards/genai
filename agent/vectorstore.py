from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

vectorstore = Chroma(
    collection_name="docs",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./chroma_db",
)


def ingest(content: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=30, chunk_overlap=5)
    texts = text_splitter.split_text(content)
    docs = [Document(page_content=t) for t in texts]
    vectorstore.add_documents(docs)
