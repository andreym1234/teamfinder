# src/repositories/users.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models.user import User

def get_by_telegram_id(db: Session, telegram_id: int) -> User | None:
    return db.execute(select(User).where(User.telegram_id == telegram_id)).scalar_one_or_none()

def upsert_from_tg(db: Session, tg_user) -> User:
    """
    tg_user: telegram.User
    """
    user = get_by_telegram_id(db, tg_user.id)
    if user is None:
        user = User(telegram_id=tg_user.id)

    user.username = tg_user.username
    user.name = tg_user.first_name
    user.surname = tg_user.last_name
    user.language_code = getattr(tg_user, "language_code", None)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
