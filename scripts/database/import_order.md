# Catalyst Data Store Import Order

When seeding or migrating data into Zoho Catalyst Data Store, tables must be imported in strict parent-first order to satisfy foreign key constraints.

## Import Sequence

### Phase A: Independent Master Tables
These tables have no foreign keys and can be imported in any order or in parallel.
1. State
2. UnitType
3. Rank
4. Designation
5. CaseCategory
6. GravityOffence
7. CaseStatusMaster
8. CrimeHead
9. Act
10. OccupationMaster
11. ReligionMaster
12. CasteMaster
13. GenderMaster
14. BloodGroupMaster
15. NationalityMaster
16. ArrestSurrenderTypeMaster

### Phase B: Dependent Master Tables
These tables depend on Phase A tables.
17. District (requires State)
18. Unit (requires District, UnitType; Note: ParentUnitRef is self-referencing, so top-level units must be imported first, followed by child units in multiple passes or with ParentUnitRef set to NULL initially and updated later).
19. Court (requires District)
20. CrimeSubHead (requires CrimeHead)
21. Section (requires Act)
22. Employee (requires Rank, Designation, Unit)

### Phase C: Core Case Tables
These tables depend on Phase B tables.
23. CaseMaster (requires Employee, Unit, CaseCategory, GravityOffence, CrimeHead, CrimeSubHead, CaseStatusMaster, Court)
24. Inv_OccurrenceTime (requires CaseMaster)
25. ComplainantDetails (requires CaseMaster, GenderMaster, NationalityMaster, ReligionMaster, CasteMaster, OccupationMaster)
26. Victim (requires CaseMaster, GenderMaster, NationalityMaster, ReligionMaster, CasteMaster, OccupationMaster)
27. Accused (requires CaseMaster, GenderMaster, NationalityMaster, ReligionMaster, CasteMaster, OccupationMaster)
28. ArrestSurrender (requires CaseMaster, ArrestSurrenderTypeMaster, Employee)
29. ChargesheetDetails (requires CaseMaster, Employee)

### Phase D: Association / Junction Tables
These tables link previously imported records.
30. ActSectionAssociation (requires CaseMaster, Act, Section)
31. CrimeHeadActSection (requires CrimeSubHead, Act, Section)
32. ArrestSurrenderAccused (requires ArrestSurrender, Accused)

## ROWID Resolution Procedure

Catalyst relies on its auto-generated `ROWID` for foreign keys. When importing from an external source (where records have a business ID like `CaseMasterID = 100`):

1. **Import Parent Table:** Import the parent records into Catalyst. Catalyst generates new `ROWID`s.
2. **Fetch ROWIDs:** Query the parent table in Catalyst to retrieve the mapping between the original business ID and the new `ROWID`.
3. **Map Child Foreign Keys:** In the child dataset, replace the foreign key references (e.g., `StateID = 5`) with the corresponding Catalyst `ROWID`.
4. **Import Child Table:** Import the prepared child records.

## Rollback and Retry Procedure

If an import fails midway:
1. Identify the batch that failed via the Catalyst CLI output or Console logs.
2. Since dependent tables rely on the parent ROWIDs, deleting parent records will `CASCADE` or `RESTRICT` depending on the schema definition.
3. If partial insertion occurred, use ZCQL to delete the partially inserted records or run a script to purge the table.
4. Correct the data issue (e.g., missing parent record, data type mismatch).
5. Resume import for that specific table. Do not re-import successful parent tables unless wiping the entire environment.
