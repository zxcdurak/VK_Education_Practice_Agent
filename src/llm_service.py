from knowledge_base import KnowledgeBase
from llm_models import AbstractChat


kb = KnowledgeBase("vkeducateproj_kb", "src/db")


async def ask_llm(chat_client: AbstractChat, query: str):
    return chat_client.ask(" ".join(kb.search(query)) + "\n" + query)  
