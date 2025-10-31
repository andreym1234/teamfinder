from telegram import Update
from telegram.ext import CallbackContext
from src.bot.run import start  # Импортируем функцию start

def test_bot_start():
    update = Update(update_id=1, message=None)  # Мокируем сообщение от пользователя
    context = CallbackContext(None)

    # Проверяем, что функция start правильно добавляет пользователя в БД
    start(update, context)
    
    db = SessionLocal()
    user = db.query(User).filter(User.telegramID == 123456).first()  # Тестируем пользователя с id 123456
    assert user is not None
    db.close()
