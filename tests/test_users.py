from src.db.session import SessionLocal
from src.models.user import User

def test_create_user():
    db = SessionLocal()
    new_user = User(telegramID=123456, name="John", username="john_doe")
    db.add(new_user)
    db.commit()

    # Проверка, что пользователь был добавлен
    user = db.query(User).filter(User.telegramID == 123456).first()
    assert user is not None
    assert user.name == "John"
    db.close()
