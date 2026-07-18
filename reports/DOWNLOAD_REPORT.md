# Download Report

> **Document ID:** BERUNDA-REP-DOWNLOAD-001 | **Version:** 1.0 | **Status:** PENDING
> **Classification:** INTERNAL | **Owner:** Berunda Team | **Source:** Acquisition agent
> **Generated:** 2026-07-18T04:30:00Z | **Last Verified:** 2026-07-18

---

## 1. Summary

| Metric | Value |
|--------|-------|
| Resources targeted | 92 |
| Auto-acquirable (AUTO-API / AUTO-DIRECT-DOWNLOAD / AUTO-GIT) | 39 |
| Requires human session (AUTO-BROWSER-WITH-USER-SESSION) | 4 |
| Requires manual intervention (SEMI-AUTOMATED / MANUAL-AUTHORIZED) | 13 |
| Future-restricted / do-not-acquire | 36 |
| **Successful downloads** | **0** |
| **Failed downloads** | **0** |
| **Pending downloads** | **56** |
| Total estimated size | ~1.15 GB |

---

## 2. Successful Downloads

*No successful downloads yet. This section will be populated by the acquisition agent.*

| RSRC ID | Resource | URL | Size | Checksum (SHA256) | Downloaded At |
|---------|----------|-----|------|-------------------|---------------|
| *(empty)* | | | | | |

---

## 3. Failed Downloads

*No failed downloads yet. Failures will be recorded here with error details.*

| RSRC ID | Resource | URL | Error | Attempted At | Retry Count |
|---------|----------|-----|-------|--------------|-------------|
| *(empty)* | | | | | |

---

## 4. Resources Requiring Manual Download

The following resources cannot be downloaded automatically and require human action:

| RSRC ID | Resource | Reason | Instructions |
|---------|----------|--------|--------------|
| RSRC-001 | Datathon ERD / DB Design Doc | MANUAL-AUTHORIZED | Already in hand â€” confirm PDF matches uploaded original |
| RSRC-002 | Police FIR Schema â€” table definitions | MANUAL-AUTHORIZED | Organizer-provided â€” confirm against ERD PDF |
| RSRC-003 | Challenge rules / timeline / judging | AUTO-BROWSER-WITH-USER-SESSION | Log into `hack2skill.com`, navigate to Resources tab, download rules PDF |
| RSRC-004 | Submission format requirements | AUTO-BROWSER-WITH-USER-SESSION | Same dashboard â€” note submission format, deadline, any templates |
| RSRC-005 | FAQ / support resources | AUTO-BROWSER-WITH-USER-SESSION | Same dashboard â€” check for updates |
| RSRC-006 | Catalyst credit code KSPH26 | AUTO-BROWSER-WITH-USER-SESSION | Visit `catalyst.zoho.com/promotions.html?cn=KSPH26` |
| RSRC-007 | Catalyst project provisioning guide | MANUAL-AUTHORIZED | Once credits redeemed, create project and document setup steps |
| RSRC-025 | Survey of India boundaries | MANUAL-AUTHORIZED | Visit `surveyofindia.gov.in` â€” verify licensing before download |
| RSRC-030 | IMD rainfall data | SEMI-AUTOMATED | Review `mausam.imd.gov.in` bulk access procedure |
| RSRC-031 | ECI election dates | SEMI-AUTOMATED | Visit `eci.gov.in`, locate Karnataka election schedule |
| RSRC-046 | Faker (en_IN) | SEMI-AUTOMATED | Run `pip install Faker` â€” verify en_IN locale support |
| RSRC-047 | indic-faker | SEMI-AUTOMATED | Source/repo unverified â€” confirm exact package before scripting |
| RSRC-024 | Bhuvan satellite imagery | SEMI-AUTOMATED | May need registration â€” verify at build time |

---

## 5. Batch Approval Table â€” P0 Items Requiring Auth

The following P0 items require explicit human approval before the agent can proceed:

| RSRC ID | Resource | Auth Type | Approved? | Approved By | Date |
|---------|----------|-----------|-----------|-------------|------|
| RSRC-003 | Challenge rules (hack2skill) | User browser session | âŒ PENDING | â€” | â€” |
| RSRC-004 | Submission format (hack2skill) | User browser session | âŒ PENDING | â€” | â€” |
| RSRC-005 | FAQ / support (hack2skill) | User browser session | âŒ PENDING | â€” | â€” |
| RSRC-006 | Catalyst credits (catalyst.zoho.com) | User browser session | âŒ PENDING | â€” | â€” |
| RSRC-007 | Catalyst project provisioning | Manual setup | âŒ PENDING | â€” | â€” |

### Required User Actions

To unblock the P0 downloads, please complete the following steps:

**Step 1 â€” Log into Hack2Skill dashboard**
```
1. Open browser â†’ https://hack2skill.com
2. Log in with your registered credentials
3. Navigate to the Datathon 2026 Resources tab
4. Download and record:
   - Challenge rules & timeline
   - Submission format requirements (CRITICAL â€” confirm file format, deadline, any templates)
   - ERD / DB Design Document (confirm matches already-provided PDF)
   - Any provided sample data
5. Save downloaded files to `data/organizer/`
6. Run: `certutil -hashfile <file> SHA256` and record in `manifests/provenance.jsonl`
```

**Step 2 â€” Redeem Catalyst credits**
```
1. Open browser â†’ https://catalyst.zoho.com/promotions.html?cn=KSPH26
2. Log in with your Zoho account
3. Verify credits are visible in console
4. Create a new Catalyst project named "Berunda"
5. Document setup steps in `docs/devsecops/`
```

**Step 3 â€” Report back**
```
After completing steps 1-2, update `manifests/approval_register.csv` with:
- resource_id, approval_type, approved_by, approval_date

Then re-run: python scripts/acquisition/download_resources.py --no-dry-run --priority P0
```

---

## 6. Auto-Acquisition Pipeline (P0 + P1)

The following resources are auto-acquirable and will be downloaded by the agent on dry-run â†’ live approval:

| Run Order | RSRC IDs | Priority | Method | Est. Time |
|-----------|----------|----------|--------|-----------|
| 1 | RSRC-016, RSRC-017 | P0 | AUTO-DIRECT-DOWNLOAD | 2 min |
| 2 | RSRC-032 | P0 | AUTO-DIRECT-DOWNLOAD | 1 min |
| 3 | RSRC-009â€“015 | P1 | AUTO-DIRECT-DOWNLOAD | 5 min |
| 4 | RSRC-019 | P1 | AUTO-DIRECT-DOWNLOAD | 1 min |
| 5 | RSRC-022 | P1 | AUTO-API | 3 min |
| 6 | RSRC-023, RSRC-024 | P1 | AUTO-API / SEMI-AUTOMATED | 3 min |
| 7 | RSRC-029 | P1 | AUTO-API | 2 min |
| 8 | RSRC-033â€“035 | P1 | AUTO-DIRECT-DOWNLOAD | 2 min |
| 9 | RSRC-040, RSRC-041 | P1 | AUTO-GIT | 3 min |
| 10 | RSRC-046 | P1 | AUTO-DIRECT-DOWNLOAD (pip) | 1 min |

---

## 7. Post-Download Validation Trigger

After each batch download completes, the agent will automatically:

1. Move files from `quarantine/` â†’ `data/raw/` (or appropriate subdirectory)
2. Generate SHA256 checksum â†’ `manifests/provenance.jsonl`
3. Update `manifests/resource_manifest.csv` with status `downloaded`
4. Trigger validation: `python scripts/validation/validate_resources.py --no-dry-run`
5. Append log entry to `logs/acquisition.log`

---

*This report is auto-updated by `scripts/acquisition/download_resources.py` and `scripts/acquisition/download_resources.ps1`.*
