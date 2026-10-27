from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types, F

TOKEN = "8986625298:AAFC9UWMeKqHZEnwoloXJM1Agmp2GOiSch8"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.photo | F.document)
async def get_photo_id(message: types.Message):
    try:
        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.document:
            file_id = message.document.file_id
        else:
            return
        
        await message.answer(f"✅ Rasmning file_id:\n\n<code>{file_id}</code>", parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xatolik: {e}")

@dp.message()
async def start_handler(message: types.Message):
    await message.answer("Assalomu alaykum! Menga rasm yuboring, men uning file_id sini chiqarib beraman.")

app = FastAPI()

@app.post("/api/webhook")
async def webhook(request: Request):
    json_data = await request.json()
    update = types.Update.model_validate(json_data, context={"bot": bot})
    async with bot:
        await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "Bot ishlamoqda"}
