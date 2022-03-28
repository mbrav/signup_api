import random
import string

from app import db, models, schemas
from app.api import auth_service


async def create_superuser(
    username: str,
    password: str,
) -> None:
    """
    Tables should be created with Alembic migrations
    But if you don't want to use migrations, create
    the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)
    """

    db_session = db.Session()
    user = await models.User.get(db_session, raise_404=False)

    if not user:
        hashed_password = auth_service.hash_password(password)
        user_in = schemas.UserCreate(
            username=username,
            password=hashed_password,
            is_admin=True)
        new_user = models.User(**user_in.dict())
        await new_user.save(db_session)


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
