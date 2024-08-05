from typing import Optional
from sqlalchemy.orm import Session
from models.komtrax_model import Komtrax
from repositories.generic_repository import GenericRepository

class KomtraxRepository(GenericRepository[Komtrax]):
    def __init__(self, db: Session):
        super().__init__(db, Komtrax)

    def find_by_serial_number(self, serial_number: str) -> Optional[Komtrax]:
        return self.db.query(Komtrax).filter(Komtrax.serial_number == serial_number).first()
