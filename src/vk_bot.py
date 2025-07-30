from vkbottle.bot import Bot, Message
from config import settings
from text_filter import ProfanityFilter
from llm_models import GigaChatImpl
from llm_service import ask_llm, kb
from parsers import FAQParser, ProgramsParser


bot = Bot(settings.vk_token)
gigachat = GigaChatImpl(settings.model_llm)
faq_parser = FAQParser(url="https://tilda-embed.tech-mail.ru/redmine_issue_13800")
progs_parser = ProgramsParser(
    url="https://store.tildaapi.com/api/getproductslist/?storepartuid=357127554781&recid=754421136&c=1752668309883&sort%5Bcreated%5D=desc&size=100",
    dir="src/parsed_data/"
    )
text_filter = ProfanityFilter("ban.txt")


@bot.on.message(text="!update")
async def update_kb(message: Message):
    progs_parser.parse_programs()
    progs_parser.save_raw_data("data_pretty.json")
    progs_parser.save_parsed_data("data_parsed.json")

    kb.update_knowledge_base(
        divs_data=faq_parser.extract_text_blocks(),
        faq_data=faq_parser.extract_faq(),
        json_file_path=progs_parser.dir + "data_parsed.json"
    )

@bot.on.message()
async def greet_handler(message: Message):
    if(text_filter.contains_profanity(message.text)):
        print(message.text)
        await message.reply("☠️Хватит ругаться!☠️")
    else:
        print("работаем...")
        await message.reply(await ask_llm(gigachat, message.text))




