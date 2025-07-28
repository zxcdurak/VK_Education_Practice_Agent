from vkbottle.bot import Bot, Message
from config import settings
from check_message import contains_profanity
from KB import take_parts
from src.llmService import ask

bot = Bot(settings.vk_token)

@bot.on.message()
async def greet_handler(message: Message):
    if(contains_profanity(message.text)):
        print(message.text)
        await message.reply("☠️Хватит ругаться!☠️")
    else:
        await message.reply(ask(" ".join(take_parts(message.text)) + "\n" + message.text))

bot.run_forever()