import requests
from bs4 import BeautifulSoup


class FAQParser:
    def __init__(self, url: str):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_content(self):
        """Получает содержимое страницы."""
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        return response.content

    def extract_text_blocks(self) -> str:
        """Извлекает текст из блоков .tn-atom."""
        content = self.fetch_content()
        soup = BeautifulSoup(content, "html.parser")
        divs = "\n".join(
            [i.text.replace("\u2028", " ") for i in soup.select('.tn-atom')]
        )
        return divs

    def extract_faq(self) -> str:
        """Извлекает пары вопрос-ответ из .t668__header и .t668__content."""
        content = self.fetch_content()
        soup = BeautifulSoup(content, "html.parser")
        FAQ_q = soup.select(".t668__header")
        FAQ_a = soup.select(".t668__content")
        faq_text = "".join([
            f"{FAQ_q[i].text.strip()}:{FAQ_a[i].text.strip()}\n"
            for i in range(min(len(FAQ_q), len(FAQ_a)))
        ])
        return faq_text
    

faq_parser = FAQParser(url="https://tilda-embed.tech-mail.ru/redmine_issue_13800")
