from typing import Type, TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

T = TypeVar("T")  # Model type

class CRUDRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        """
        Generic CRUD repository for any SQLAlchemy model.
        :param model: SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[T]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: Dict[str, Any]) -> T:
        obj = self.model(**obj_in)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: T, obj_in: Dict[str, Any]) -> T:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: T) -> T:
        """
        Delete a model instance.
        :param db_obj: The SQLAlchemy model instance to delete
        """
        db.delete(db_obj)
        db.commit()
        return db_obj

    
    def get_by_field(self, db: Session, field_name: str, value: Any) -> Optional[T]:
            """
            Get a single record by any column.
            """
            return db.query(self.model).filter(getattr(self.model, field_name) == value).first()
