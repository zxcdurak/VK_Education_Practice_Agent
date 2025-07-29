from vkbottle.bot import Bot, Message
from config import settings
from text_filter import text_filter as tf
from llm_models import gigachat
from llm_service import ask_llm

bot = Bot(settings.vk_token)

@bot.on.message()
async def greet_handler(message: Message):
    if(tf.contains_profanity(message.text)):
        print(message.text)
        await message.reply("☠️Хватит ругаться!☠️")
    else:
        await message.reply(await ask_llm(gigachat, message.text))
