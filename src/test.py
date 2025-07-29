import requests
from bs4 import BeautifulSoup


def web_search_answer(query: str) -> str:
    # Делаем простой запрос и возвращаем первые параграф
    r = requests.get('https://api.allorigins.win/raw?url=' + requests.utils.quote('https://duckduckgo.com/html/?q='+query))
    soup = BeautifulSoup(r.text, 'html.parser')
    
    p = soup.find_all(class_='result__snippet')[:5]
    return p if p else "Я не нашёл информации в интернете."


with open('data_parsed.json', 'r', encoding="utf-8") as file:
    content = file.read()
    char_count = len(content)
    print(f"Количество символов в файле: {char_count}")

# print(*[i.text for i in web_search_answer("Что такое блокчейн")], sep="\n\n")

# from KB import take_parts, retriever, vector_db

# print(take_parts("Что такое VK educate"))
from time import time
from knowledge_base import kb
start = time()

print(("Что такое VK educate?"))
print(time() - start)