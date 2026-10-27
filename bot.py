import os
from aiogram import Bot, Dispatcher, types, F
from fastapi import FastAPI, Request

TOKEN = "8986625298:AAFC9UWMeKqHZEnwoloXJM1Agmp2GOiSch8"
bot = Bot(token=TOKEN)
dp = Dispatcher()

app = FastAPI()

@dp.message(F.photo | F.document)
async def get_file_id(message: types.Message):
    if message.photo:
        file_id = message.photo[-1].file_id
        await message.answer(f"✅ РАСМНИНГ FILE_ID СИ:\n\n<code>{file_id}</code>", parse_mode="HTML")
    elif message.document:
        file_id = message.document.file_id
        await message.answer(f"✅ ФАЙЛНИНГ FILE_ID СИ:\n\n<code>{file_id}</code>", parse_mode="HTML")

@dp.message()
async def start_handler(message: types.Message):
    await message.answer("Салом! Менга расм юборинг, мен uning file_id sini chiqarib beraman.")

@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}
