from vkbottle.bot import Bot, Message
from config import settings
from text_filter import text_filter as tf
from knowledge_base import kb
from llm_service import gigachat

bot = Bot(settings.vk_token)

@bot.on.message()
async def greet_handler(message: Message):
    if(tf.contains_profanity(message.text)):
        print(message.text)
        await message.reply("☠️Хватит ругаться!☠️")
    else:
        await message.reply(gigachat.ask(" ".join(kb.searh(message.text)) + "\n" + message.text))
