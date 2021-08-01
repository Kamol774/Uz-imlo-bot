import logging
from aiogram import Bot, Dispatcher, executor, types
from checkword import checkWord
from transliterate import to_cyrillic
from settings.local_settings import TELEGRAM_TOKEN

API_TOKEN = TELEGRAM_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm Uz-imlo-bot!\nYou can write any word to check whether it is true or not")

@dp.message_handler()
async def checkImlo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    msg = message.text
    javob = lambda msg: to_cyrillic(msg) if msg.isascii() else to_cyrillic(msg)
    message.text = javob(msg)

    if len(message.text)>1:
        message.text = message.text.split()
        for word in message.text:
            result = checkWord(word)
            if result['available']:
                response = f"✅{word.capitalize()}"
            else:
                response = f"❌{word.capitalize()}\n"
                for text in result['matches']:
                    response += f"✅{text.capitalize()}\n"
            await message.answer(response)
    else:
        word = message.text
        result = checkWord(word)
        if result['available']:
            response = f"✅{word.capitalize()}"
        else:
            response = f"❌{word.capitalize()}\n"
            for text in result['matches']:
                response += f"✅{text.capitalize()}\n"
        await message.answer(response)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)