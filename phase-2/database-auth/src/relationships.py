from sqlalchemy.orm import relationship

from .models import (
    CaseMaster, InvOccuranceTime, ComplainantDetails,
    Victim, Accused, ActSectionAssociation, User,
    District, Unit,
)

# CaseMaster -> InvOccuranceTime (one-to-one)
CaseMaster.occurrence_time = relationship(
    "InvOccuranceTime", uselist=False,
    back_populates="case_master", passive_deletes=True
)
InvOccuranceTime.case_master = relationship(
    "CaseMaster", back_populates="occurrence_time"
)

# CaseMaster -> ComplainantDetails (one-to-many)
CaseMaster.complainants = relationship(
    "ComplainantDetails", back_populates="case_master", passive_deletes=True
)
ComplainantDetails.case_master = relationship(
    "CaseMaster", back_populates="complainants"
)

# CaseMaster -> Victim (one-to-many)
CaseMaster.victims = relationship(
    "Victim", back_populates="case_master", passive_deletes=True
)
Victim.case_master = relationship(
    "CaseMaster", back_populates="victims"
)

# CaseMaster -> Accused (one-to-many)
CaseMaster.accused = relationship(
    "Accused", back_populates="case_master", passive_deletes=True
)
Accused.case_master = relationship(
    "CaseMaster", back_populates="accused"
)

# CaseMaster -> ActSectionAssociation (one-to-many)
CaseMaster.act_sections = relationship(
    "ActSectionAssociation", back_populates="case_master", passive_deletes=True
)
ActSectionAssociation.case_master = relationship(
    "CaseMaster", back_populates="act_sections"
)

# User -> District (many-to-one)
User.district = relationship("District", back_populates="users")
District.users = relationship("User", back_populates="district")

# Unit -> District (many-to-one)
Unit.district = relationship("District", back_populates="units")
District.units = relationship("Unit", back_populates="district")

# CaseMaster -> Unit (PoliceStation)
CaseMaster.police_station = relationship(
    "Unit", back_populates="cases", foreign_keys=[CaseMaster.PoliceStationID]
)
Unit.cases = relationship(
    "CaseMaster", back_populates="police_station",
    foreign_keys=[CaseMaster.PoliceStationID]
)

# CaseMaster -> GravityOffence
CaseMaster.gravity_offence = relationship("GravityOffence", back_populates="cases")
GravityOffence.cases = relationship("CaseMaster", back_populates="gravity_offence")

# CaseMaster -> CrimeHead (major head)
CaseMaster.crime_major_head = relationship(
    "CrimeHead", back_populates="cases"
)
CrimeHead.cases = relationship(
    "CaseMaster", back_populates="crime_major_head"
)
