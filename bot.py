import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from google import genai
from aiohttp import web

# Render port talab qilgani uchun veb-server
async def handle(request):
    return web.Response(text="Bot ishlamoqda!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 10000)))
    await site.start()

# Tokenlar
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
client = genai.Client(api_key=GEMINI_API_KEY)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("👋 Assalomu alaykum! Menga istalgan savol yozing, sun'iy intellekt yordamida javob beraman.")

@dp.message()
async def chat_handler(message: types.Message):
    await asyncio.sleep(1)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=message.text,
        )
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")

async def main():
    await start_web_server()
    print("Bot va veb server ishga tushdi...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())