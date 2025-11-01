# teamfinder/src/bot/run.py
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pydantic_settings import BaseSettings

from core.db import engine, AsyncSessionLocal, Base
from repositories.users import upsert_from_tg_profile

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    class Config:
        env_file = ".env"

settings = Settings()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("bot")

async def ensure_schema():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    async with AsyncSessionLocal() as session:
        user = await upsert_from_tg_profile(
            session,
            tg_id=u.id,
            username=u.username,
            first_name=u.first_name,
            last_name=u.last_name,
            lang=u.language_code,
        )
    await update.message.reply_text(f"Привет, {u.first_name}! Твой id в БД: {user.id}")

async def main():
    await ensure_schema()
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))
    log.info("Bot started.")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
