from app import db, models, schemas
from app.api import auth_service


def create_superuser(username: str,
                     password: str,
                     session=db.get_db,
                     schema=schemas.UserCreate) -> None:
    """
    Tables should be created with Alembic migrations
    But if you don't want to use migrations, create
    the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)
    """
    db = session()
    user = db.query(models.User).count() != 0
    if not user:
        hashed_password = auth_service.hash_password(password)
        user_in = schema(
            username=username,
            password=hashed_password,
            is_superuser=True)
        new_user = models.User(**user_in.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
