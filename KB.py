from langchain.text_splitter import RecursiveCharacterTextSplitter
from parserINFO import divs, FAQ_qa

docs = []
def update_docs():
    docs.append(divs)
    docs.append(FAQ_qa)
    with open("data_parsed.json", encoding="utf-8") as f:
        s = f.read()
        docs.append(s)

update_docs()

splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
chunks = [chunk for doc in docs for chunk in splitter.split_text(doc)]

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = Chroma(collection_name="gigachats_kb", persist_directory="./db", embedding_function=embeddings)
# vector_db.add_texts(chunks)

retriever = vector_db.as_retriever(search_kwargs={"k": 5})  # получить топ‑5

def take_parts(ask: str) -> list[str]:
    docs = retriever.invoke(ask)
    return [d.page_content for d in docs]

# prompt = "\n\n".join([d.page_content for d in docs]) + "\n\nQUESTION: " + query

# print(prompt)