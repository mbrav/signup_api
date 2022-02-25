import random
import string

from sqlalchemy.orm import Session

from app import db, models, schemas
from app.api import auth_service
from app.models import to_snake_case


async def create_superuser(
    username: str,
    password: str,
    session: Session = db.Session
) -> None:
    """
    Tables should be created with Alembic migrations
    But if you don't want to use migrations, create
    the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)
    """
    db_session = session()
    user = db_session.query(models.User).count() != 0
    if not user:
        hashed_password = auth_service.hash_password(password)
        user_in = schemas.UserCreate(
            username=username,
            password=hashed_password,
            is_superuser=True)
        new_user = models.User(**user_in.dict())
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)


def random_lower_string(num: int = 20) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=num))


def random_numbers(num: int = 20) -> str:
    return ''.join(random.choices(string.digits, k=num))


def random_id_string(num: int = 20) -> str:
    return ''.join(random.choices(string.ascii_letters, k=num))


def random_email() -> str:
    return f'{random_lower_string(10)}@{random_lower_string(5)}.com'


def random_phone(num: int = 20) -> str:
    return '+' + random_numbers(11)
