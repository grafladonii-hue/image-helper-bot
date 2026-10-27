import os
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types, F

TOKEN = "8986625298:AAFC9UWMeKqHZEnwoloXJM1Agmp2GOiSch8"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.photo)
async def get_photo_id(message: types.Message):
    photo = message.photo[-1]
    await message.answer(f"✅ Rasmning file_id:\n\n<code>{photo.file_id}</code>", parse_mode="HTML")

@dp.message()
async def start_handler(message: types.Message):
    await message.answer("Assalomu alaykum! Menga rasm yuboring, men uning file_id sini chiqarib beraman.")

app = FastAPI()

@app.post("/api/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = types.Update.model_validate(data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "Image ID bot ishlamoqda"}