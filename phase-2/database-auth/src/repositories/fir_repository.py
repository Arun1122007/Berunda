from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session as SASession, joinedload

from ..models import (
    CaseMaster, InvOccuranceTime, ComplainantDetails,
    Victim, Accused, Unit, District,
)
from .base import Repository


class FirRepository(Repository[CaseMaster]):

    def __init__(self, db: SASession):
        self.db = db

    def _eager_query(self):
        return self.db.query(CaseMaster).options(
            joinedload(CaseMaster.occurrence_time),
            joinedload(CaseMaster.complainants),
            joinedload(CaseMaster.victims),
            joinedload(CaseMaster.accused),
            joinedload(CaseMaster.police_station),
            joinedload(CaseMaster.gravity_offence),
            joinedload(CaseMaster.crime_major_head),
        )

    def get_by_id(self, entity_id: int) -> Optional[CaseMaster]:
        return self._eager_query().filter(CaseMaster.CaseMasterID == entity_id).first()

    def list(
        self,
        offset: int = 0,
        limit: int = 100,
        **filters: Any,
    ) -> List[CaseMaster]:
        q = self._eager_query()

        if "district_id" in filters and filters["district_id"] is not None:
            q = q.join(CaseMaster.police_station).filter(
                Unit.DistrictID == filters["district_id"]
            )

        if "police_station_id" in filters and filters["police_station_id"] is not None:
            q = q.filter(CaseMaster.PoliceStationID == filters["police_station_id"])

        if "case_status_id" in filters and filters["case_status_id"] is not None:
            q = q.filter(CaseMaster.CaseStatusID == filters["case_status_id"])

        if "crime_no" in filters and filters["crime_no"] is not None:
            q = q.filter(CaseMaster.CrimeNo == filters["crime_no"])

        return q.offset(offset).limit(limit).all()

    def create(self, data: Dict[str, Any]) -> CaseMaster:
        case = CaseMaster(**data)
        self.db.add(case)
        self.db.flush()
        return case

    def update(self, entity_id: int, data: Dict[str, Any]) -> Optional[CaseMaster]:
        case = self.db.query(CaseMaster).filter(CaseMaster.CaseMasterID == entity_id).first()
        if not case:
            return None
        for key, value in data.items():
            if hasattr(case, key):
                setattr(case, key, value)
        self.db.flush()
        return case

    def delete(self, entity_id: int) -> bool:
        case = self.db.query(CaseMaster).filter(CaseMaster.CaseMasterID == entity_id).first()
        if not case:
            return False
        self.db.delete(case)
        self.db.flush()
        return True

    def count(self, **filters: Any) -> int:
        q = self.db.query(CaseMaster)
        if "district_id" in filters and filters["district_id"] is not None:
            q = q.join(CaseMaster.police_station).filter(
                Unit.DistrictID == filters["district_id"]
            )
        if "case_status_id" in filters and filters["case_status_id"] is not None:
            q = q.filter(CaseMaster.CaseStatusID == filters["case_status_id"])
        return q.count()
