import requests
import orjson
from bs4 import BeautifulSoup
from pathlib import Path


class ProgramsParser:
    def __init__(self, url: str, dir: str):
        self.url = url
        self.dir = Path(dir)
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.data_progs = []

        self.dir.mkdir(exist_ok=True, parents=True)

    def fetch_data(self) -> dict:
        """Получает JSON-данные с API."""
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        return orjson.loads(response.content)

    def clean_program_text(self, text):
        soup = BeautifulSoup(text, "html.parser")
        cleaned_text = soup.get_text(separator=" ", strip=True)
        for old, new in [
            ("Желаем удачи! Нажмите «Выбрать проект», чтобы зарегистрироваться и получить доступ к подробному описанию.", ""),
            ("Желаем успехов! Нажмите «Выбрать проект», чтобы зарегистрироваться и получить доступ к подробному описанию.", "")
        ]:
            cleaned_text = cleaned_text.replace(old, new)
        return cleaned_text

    def parse_programs(self) -> list[dict]:
        """Обрабатывает список программ и возвращает список словарей."""
        raw_data = self.fetch_data()
        products = raw_data["products"]
        total = raw_data["total"]

        print(f"Found {len(products)} out of {total} programs")

        self.data_progs = []
        for i, prog in enumerate(products):
            print(f"{i+1}. {prog['title']}")

            cleaned_text = self.clean_program_text(prog["text"])

            program_data = {
                "title": prog["title"],
                "short_description": prog["descr"].replace("&nbsp;", " "),
                "description": cleaned_text,
                "direction": prog["characteristics"][0]["value"] if len(prog["characteristics"]) > 0 else "",
                "duration": prog["characteristics"][1]["value"] if len(prog["characteristics"]) > 1 else "",
                "status": prog["characteristics"][2]["value"] if len(prog["characteristics"]) > 2 else "",
            }
            self.data_progs.append(program_data)

        return self.data_progs

    def save_raw_data(self, filename: str = "data_pretty.json"):
        """Сохраняет исходные данные с API в формате pretty JSON."""
        raw_data = self.fetch_data()
        filepath = self.dir / filename  # Склеиваем путь через /
        with filepath.open("wb") as f:
            f.write(orjson.dumps(raw_data, option=orjson.OPT_INDENT_2))
        print(f"Raw data saved to {filepath}")

    def save_parsed_data(self, filename: str = "data_parsed.json"):
        """Сохраняет обработанные данные о программах."""
        filepath = self.dir / filename
        with filepath.open("wb") as f:
            f.write(orjson.dumps(self.data_progs, option=orjson.OPT_INDENT_2))
        print(f"Parsed programs saved to {filepath}")


progs_parser = ProgramsParser(
    url="https://store.tildaapi.com/api/getproductslist/?storepartuid=357127554781&recid=754421136&c=1752668309883&sort%5Bcreated%5D=desc&size=100",
    dir="src/parsed_data/"
    )

progs_parser.parse_programs()
progs_parser.save_raw_data("data_pretty.json")
progs_parser.save_parsed_data("data_parsed.json")
