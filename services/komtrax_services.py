from models.komtrax_model import Komtrax
from repositories.komtrax_repository import KomtraxRepository
from models.dto.komtrax_request import KomtraxRequest
from sqlalchemy.orm import Session

class KomtraxService:
    def __init__(self, db: Session):
        self.repo = KomtraxRepository(db)

    def read_all_komtrax_service(self):
        return self.repo.get_all()

    def read_komtrax_by_id_service(self, komtrax_id: int):
        return self.repo.get_by_id(komtrax_id)

    def create_komtrax_service(self, komtrax_request: KomtraxRequest):
        komtrax = Komtrax(
            smr = komtrax_request.smr,
            working_hour = komtrax_request.working_hour,
            actual_working_hour = komtrax_request.actual_working_hour
        )
        return self.repo.create(komtrax)

    def delete_komtrax_service(self, komtrax_id: int):
        komtrax = self.repo.get_by_id(komtrax_id)
        if komtrax is None:
            return None
        self.repo.delete(komtrax)
        return komtrax

    def update_komtrax_service(self, komtrax_id: int, komtrax_request: KomtraxRequest):
        komtrax = self.repo.get_by_id(komtrax_id)
        if komtrax is None:
            return None
        komtrax.smr = komtrax_request.smr
        komtrax.working_hour = komtrax_request.working_hour
        komtrax.actual_working_hour = komtrax_request.actual_working_hour
        return self.repo.update(komtrax)