from sqlalchemy.orm import Session
from typing import Type, Generic, TypeVar, List, Optional
from database import Base, Base1
from sqlalchemy.orm import Query

T = TypeVar('T')

class GenericRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model
    
    def get_all(self):
        return self.db.query(self.model).all()
    
    def get_by_id(self, id:int):
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def create(self, item: T):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def update(self, item: T):
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def delete(self, item: T):
        self.db.delete(item)
        self.db.commit()