from abc import ABC, abstractmethod
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from config import settings
from prompt_manager import manager


class AbstractChat(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def ask(self, question: str) -> str:
        pass


class GigaChatImpl(AbstractChat):
    def __init__(self, model: str):
        super().__init__()
        self.giga = GigaChat(
            credentials=settings.giga_auth_key,
            verify_ssl_certs=False,
            model=model
        )

    def ask(self, question: str) -> str:
        messages = [
            SystemMessage(
                content=manager.get_prompt("vk_agent")
            )]
        messages.append(HumanMessage(content=question))
        res = self.giga.invoke(messages)
        return res.content
