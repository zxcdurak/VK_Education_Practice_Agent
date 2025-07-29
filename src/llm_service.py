from knowledge_base import kb
from llm_models import AbstractChat


async def ask_llm(chat_client: AbstractChat, query: str):
    return chat_client.ask(" ".join(kb.search(query)) + "\n" + query)  
