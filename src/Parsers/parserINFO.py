import requests
from bs4 import BeautifulSoup

URL_api = "https://tilda-embed.tech-mail.ru/redmine_issue_13800"

res = requests.get(URL_api, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})

soup = BeautifulSoup(res.content, "html.parser")

divs = "\n".join([i.text.replace("\u2028", " ") for i in soup.select('.tn-atom')])
FAQ_q = soup.select(".t668__header")
FAQ_a = soup.select(".t668__content")
FAQ_qa = "".join([f"{FAQ_q[i].text.strip()}:{FAQ_a[i].text}" for i in range(len(FAQ_q))])

# print(divs)
# for i in range(len(FAQ_q)):
#     print(FAQ_q[i], FAQ_a[i], sep="\n")
#     print()