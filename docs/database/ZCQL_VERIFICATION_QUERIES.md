# ZCQL Verification Queries

This document contains Zoho Catalyst Query Language (ZCQL) queries designed to verify the correct migration and relationships of the FIR Data Store Schema.

## 1. Case with Station, District, and Employee
Verifies that a `CaseMaster` record properly joins to its `Unit` (Police Station), the station's `District`, and the Investigating Officer (`Employee`).

```sql
SELECT CaseMaster.CrimeNo, Unit.UnitName, District.DistrictName, Employee.EmployeeName
FROM CaseMaster
LEFT JOIN Unit ON CaseMaster.PoliceStationRef = Unit.ROWID
LEFT JOIN District ON Unit.DistrictRef = District.ROWID
LEFT JOIN Employee ON CaseMaster.PolicePersonRef = Employee.ROWID
WHERE CaseMaster.CaseNo = '12345';
```

## 2. Case with Victims and Accused
Verifies 1:N relationships between FIRs and associated individuals.

**Victims:**
```sql
SELECT CaseMaster.CrimeNo, Victim.Name, Victim.Age
FROM CaseMaster
JOIN Victim ON CaseMaster.ROWID = Victim.CaseMasterRef
WHERE CaseMaster.CrimeNo = 'FIR-001-2023';
```

**Accused:**
```sql
SELECT CaseMaster.CrimeNo, Accused.Name, Accused.Age
FROM CaseMaster
JOIN Accused ON CaseMaster.ROWID = Accused.CaseMasterRef
WHERE CaseMaster.CrimeNo = 'FIR-001-2023';
```

## 3. Case with Act and Sections
Verifies the `ActSectionAssociation` junction table joining `CaseMaster` with `Act` and `Section`.

```sql
SELECT CaseMaster.CrimeNo, Act.ActName, Section.SectionName
FROM ActSectionAssociation
JOIN CaseMaster ON ActSectionAssociation.CaseMasterRef = CaseMaster.ROWID
JOIN Act ON ActSectionAssociation.ActRef = Act.ROWID
JOIN Section ON ActSectionAssociation.SectionRef = Section.ROWID
WHERE CaseMaster.CrimeNo = 'FIR-001-2023';
```

## 4. Arrest with Accused and Investigating Officer
Verifies the `ArrestSurrenderAccused` junction table and link to `Employee`.

```sql
SELECT ArrestSurrender.DateOfArrest, Accused.Name, Employee.EmployeeName, ArrestSurrenderAccused.IsPrimaryAccused
FROM ArrestSurrenderAccused
JOIN ArrestSurrender ON ArrestSurrenderAccused.ArrestSurrenderRef = ArrestSurrender.ROWID
JOIN Accused ON ArrestSurrenderAccused.AccusedRef = Accused.ROWID
JOIN Employee ON ArrestSurrender.PolicePersonRef = Employee.ROWID;
```

## 5. Chargesheet with Case and Employee
Verifies that `ChargesheetDetails` correctly points to the `CaseMaster` and the filing `Employee`.

```sql
SELECT ChargesheetDetails.ChargesheetDate, CaseMaster.CrimeNo, Employee.EmployeeName
FROM ChargesheetDetails
JOIN CaseMaster ON ChargesheetDetails.CaseMasterRef = CaseMaster.ROWID
JOIN Employee ON ChargesheetDetails.PolicePersonRef = Employee.ROWID;
```

## 6. Crime-head and Sub-head Joins
Verifies that cases properly map to major and minor crime categories.

```sql
SELECT CaseMaster.CrimeNo, CrimeHead.HeadName, CrimeSubHead.SubHeadName
FROM CaseMaster
JOIN CrimeHead ON CaseMaster.CrimeMajorHeadRef = CrimeHead.ROWID
JOIN CrimeSubHead ON CaseMaster.CrimeMinorHeadRef = CrimeSubHead.ROWID;
```

## 7. Orphan Record Detection Queries
Queries designed to catch integrity violations (e.g., if a cascade or restrict constraint failed during a bug).

**Find Victims without a Case:**
```sql
SELECT Victim.ROWID, Victim.Name 
FROM Victim
LEFT JOIN CaseMaster ON Victim.CaseMasterRef = CaseMaster.ROWID
WHERE CaseMaster.ROWID IS NULL;
```

**Find Occurrence Times without a Case:**
```sql
SELECT Inv_OccurrenceTime.ROWID 
FROM Inv_OccurrenceTime
LEFT JOIN CaseMaster ON Inv_OccurrenceTime.CaseMasterRef = CaseMaster.ROWID
WHERE CaseMaster.ROWID IS NULL;
```

**Find Arrest-Accused junction records missing an Accused:**
```sql
SELECT ArrestSurrenderAccused.ROWID 
FROM ArrestSurrenderAccused
LEFT JOIN Accused ON ArrestSurrenderAccused.AccusedRef = Accused.ROWID
WHERE Accused.ROWID IS NULL;
```
