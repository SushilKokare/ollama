from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Import all your models here so Alembic knows about them
from app.models import user
