from sqlalchemy.orm import Session
from typing import Type, Generic, TypeVar, List

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
        try:
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return True
        except Exception:
            self.db.rollback()
    
    def bulk_create(self, items: List[T]):
        try:
            self.db.bulk_save_objects(items)
            self.db.commit()
            return True
        except Exception as e:
            print(str(e))
            self.db.rollback()
            return False
    
    def update(self, item: T):
        try:
            self.db.commit()
            self.db.refresh(item)
            return True
        except Exception as e:
            self.db.rollback()
            return False
        
    
    def bulk_update(self, items: List[T]):
        try:
            self.db.bulk_update_mappings(T, [item.to_dict() for item in items])
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False
    
    def delete(self, item: T):
        try:
            self.db.delete(item)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False