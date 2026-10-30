from aiogram import Bot, Dispatcher, types, F
from fastapi import FastAPI, Request

TOKEN = "8986625298:AAFC9UWMeKqHZEnwoloXJM1Agmp2GOiSch8"
bot = Bot(token=TOKEN)
dp = Dispatcher()

app = FastAPI()

@dp.message(F.text & (F.text == "/start"))
async def start_handler(message: types.Message):
    await message.answer("Салом! Менга расм ёки ҳужжат юборинг, мен унинг админка учун тайёр веб-ҳаволасини чиқариб бераман.")

@dp.message(F.photo | F.document)
async def get_file_url(message: types.Message):
    if message.photo:
        file_id = message.photo[-1].file_id
    else:
        file_id = message.document.file_id
        
    try:
        # Telegram API орқали файлнинг йўлини (file_path) оламиз
        file = await bot.get_file(file_id)
        file_path = file.file_path
        
        # Тўғридан-тўғри веб-ҳаволани яшаймиз
        direct_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
        
        await message.answer(
            f"✅ РАСМНИНГ ВЕБ ҲАВОЛАСИ:\n\n<code>{direct_url}</code>", 
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}")

@app.post("/")
async def webhook(request: Request):
    try:
        data = await request.json()
        update = types.Update.model_validate(data, context={"bot": bot})
        await dp.feed_update(bot, update)
    except Exception as e:
        print(f"Xatolik: {e}")
    return {"ok": True}

@app.get("/")
async def index():
    return {"status": "Bot is running!"}
