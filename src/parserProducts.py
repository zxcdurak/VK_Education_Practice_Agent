import requests
import orjson
import re


URL_api =   "https://store.tildaapi.com/api/getproductslist/?storepartuid=357127554781&recid=754421136&c=1752668309883&sort%5Bcreated%5D=desc&size=100"
res = requests.get(URL_api, headers={"User-Agent": "Mozilla/5.0"})

data_progs = []

input_data = orjson.loads(res.content)
print(len(input_data["products"]), input_data["total"])

for i, programm in enumerate(input_data["products"]):
    print(i+1, programm["title"])
    temp = dict()
    temp["title"] = programm["title"]
    temp["short_description"] = programm["descr"].replace("&nbsp;", " ")
    temp["description"] = (
        re.sub(re.compile("<.*?>"), '', programm["text"])
        .replace("Желаем удачи!Нажмите «Выбрать проект», чтобы зарегистрироваться и получить доступ к подробному описанию.", "")
        .replace("&nbsp;", " ")
        .replace("amp;", "")
        .replace("Желаем успехов!Нажмите «Выбрать проект», чтобы зарегистрироваться и получить доступ к подробному описанию.", "")
        )
    
    temp["direction"] = programm["characteristics"][0]["value"]
    temp["duration"] = programm["characteristics"][1]["value"]
    temp["status"] = programm["characteristics"][2]["value"]
    data_progs.append(temp)

with open("data_pretty.json", "wb") as f:
    f.write(orjson.dumps(orjson.loads(res.content), option=orjson.OPT_INDENT_2))

with open("data_parsed.json", "wb") as f:
    f.write(orjson.dumps((data_progs), option=orjson.OPT_INDENT_2))
