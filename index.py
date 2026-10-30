from aiogram import Bot, Dispatcher, types, F
from fastapi import FastAPI, Request
import aiohttp

TOKEN = "8986625298:AAFC9UWMeKqHZEnwoloXJM1Agmp2GOiSch8"
bot = Bot(token=TOKEN)
dp = Dispatcher()

app = FastAPI()

@dp.message(F.text & (F.text == "/start"))
async def start_handler(message: types.Message):
    await message.answer("Салом! Менга расм ёки ҳужжат юборинг, мен унинг file_id сини чиқариб бераман.")

@dp.message(F.photo | F.document)
async def get_file_id(message: types.Message):
    if message.photo:
        file_id = message.photo[-1].file_id
        await message.answer(f"✅ РАСМНИНГ FILE_ID СИ:\n\n<code>{file_id}</code>", parse_mode="HTML")
    elif message.document:
        file_id = message.document.file_id
        await message.answer(f"✅ ФАЙЛНИНГ FILE_ID СИ:\n\n<code>{file_id}</code>", parse_mode="HTML")

# --- МАНА BU YANGI FUNKSIYA QO'SHILDI ---
@app.get("/get-image-url/{file_id}")
async def get_image_url(file_id: str):
    async with aiohttp.ClientSession() as session:
        api_url = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}"
        async with session.get(api_url) as resp:
            res_json = await resp.json()
            if res_json.get("ok"):
                file_path = res_json["result"]["file_path"]
                download_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
                return {"url": download_url}
    return {"url": ""}

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
