from langchain.text_splitter import RecursiveCharacterTextSplitter
from Parsers.parserINFO import divs, FAQ_qa
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import orjson


class KnowledgeBase:
    def __init__(self, collection_name: str = None, persist_directory: str = None):
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        self._init_components()

    def _init_components(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=100
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_db = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

        self.retriever = self.vector_db.as_retriever(
            search_kwargs={"k": 5}
        )

    def load_documents(self, divs_data: str = None, faq_data: str = None, json_file_path: str = None):
        docs = []

        if divs_data is not None:
            docs.append(divs_data)

        if faq_data is not None:
            docs.append(faq_data)

        if json_file_path:
            try:
                with open(json_file_path, "rb") as f:
                    data = orjson.loads(f.read())
                    docs.append(orjson.dumps(data).decode('utf-8'))
            except FileNotFoundError:
                print(f"Файл {json_file_path} не найден")
            except orjson.JSONDecodeError as e:
                print(f"Ошибка при чтении JSON файла: {e}")

        return docs

    def update_knowledge_base(self, divs_data: str = None, faq_data: str = None, json_file_path: str = None):
        docs = self.load_documents(divs_data, faq_data, json_file_path)

        if not docs:
            print("Нет документов для добавления")
            return

        chunks = [
            chunk for doc in docs for chunk in self.splitter.split_text(doc)]

        if chunks:
            self.vector_db.add_texts(chunks)
            print(f"Добавлено {len(chunks)} чанков в базу знаний")
        else:
            print("Не удалось создать чанки из документов")

    def search(self, query: str) -> list[str]:
        parts = self.retriever.invoke(query)
        return [p.page_content for p in parts]


KB = KnowledgeBase("gigachats_kb", "../db")
