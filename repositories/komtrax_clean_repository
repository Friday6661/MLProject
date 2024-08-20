from typing import Optional
from sqlalchemy.orm import Session
from models.komtrax_clean_model import KomtraxClean
from repositories.generic_repository import GenericRepository

class KomtraxRepository(GenericRepository[KomtraxClean]):
    def __init__(self, db: Session):
        super().__init__(db, KomtraxClean)

    def find_by_serial_number(self, serial_number: str) -> Optional[KomtraxClean]:
        return self.db.query(KomtraxClean).filter(KomtraxClean.serial_number == serial_number).first()
