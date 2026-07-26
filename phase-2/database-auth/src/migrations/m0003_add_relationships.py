"""Migration 003: Add foreign key constraints between related tables."""

from sqlalchemy import MetaData

FK_STATEMENTS = """
ALTER TABLE src_CaseMaster ADD CONSTRAINT fk_cm_ps FOREIGN KEY (PoliceStationID) REFERENCES src_Unit(UnitID);
ALTER TABLE src_Inv_OccuranceTime ADD CONSTRAINT fk_iot_cm FOREIGN KEY (CaseMasterID) REFERENCES src_CaseMaster(CaseMasterID);
ALTER TABLE src_ComplainantDetails ADD CONSTRAINT fk_cd_cm FOREIGN KEY (CaseMasterID) REFERENCES src_CaseMaster(CaseMasterID);
ALTER TABLE src_Victim ADD CONSTRAINT fk_v_cm FOREIGN KEY (CaseMasterID) REFERENCES src_CaseMaster(CaseMasterID);
ALTER TABLE src_Accused ADD CONSTRAINT fk_a_cm FOREIGN KEY (CaseMasterID) REFERENCES src_CaseMaster(CaseMasterID);
ALTER TABLE src_ActSectionAssociation ADD CONSTRAINT fk_asa_cm FOREIGN KEY (CaseMasterID) REFERENCES src_CaseMaster(CaseMasterID);
ALTER TABLE src_Unit ADD CONSTRAINT fk_u_d FOREIGN KEY (DistrictID) REFERENCES src_District(DistrictID);
ALTER TABLE auth_User ADD CONSTRAINT fk_au_d FOREIGN KEY (DistrictID) REFERENCES src_District(DistrictID);
ALTER TABLE auth_Session ADD CONSTRAINT fk_as_u FOREIGN KEY (UserID) REFERENCES auth_User(UserID);
ALTER TABLE src_CaseMaster ADD CONSTRAINT fk_cm_go FOREIGN KEY (GravityOffenceID) REFERENCES src_GravityOffence(GravityOffenceID);
ALTER TABLE src_CaseMaster ADD CONSTRAINT fk_cm_ch FOREIGN KEY (CrimeMajorHeadID) REFERENCES src_CrimeHead(CrimeHeadID);
ALTER TABLE src_CaseMaster ADD CONSTRAINT fk_cm_csm FOREIGN KEY (CaseStatusID) REFERENCES src_CaseStatusMaster(CaseStatusID);
"""


def upgrade(engine):
    for statement in FK_STATEMENTS.strip().split("\n"):
        stmt = statement.strip()
        if stmt:
            engine.execute(stmt)


def downgrade(engine):
    meta = MetaData()
    meta.reflect(bind=engine)
    fk_names = [
        "fk_cm_ps", "fk_iot_cm", "fk_cd_cm", "fk_v_cm", "fk_a_cm",
        "fk_asa_cm", "fk_u_d", "fk_au_d", "fk_as_u",
        "fk_cm_go", "fk_cm_ch", "fk_cm_csm",
    ]
    for name in fk_names:
        try:
            engine.execute(f"ALTER TABLE ... DROP CONSTRAINT {name}")
        except Exception:
            pass
