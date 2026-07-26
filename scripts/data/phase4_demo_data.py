# ruff: noqa: E501
"""
Phase 4 synthetic demo data generator for Project Berunda.

Generates realistic demo data for Phase 4 features:
  - Investigation notes for FIRs
  - Case assignments
  - Supervisor reviews
  - Related case suggestions
  - Report requests
  - Vehicle links
  - Evidence with metadata
  - Background jobs

All data is clearly marked SYNTHETIC and generated with deterministic
seeds for reproducibility. Idempotent — safe to run multiple times.

Usage:
    python scripts/data/phase4_demo_data.py
    python scripts/data/phase4_demo_data.py --seed 42 --dry-run
    python scripts/data/phase4_demo_data.py --seed 42 --force
    python scripts/data/phase4_demo_data.py --seed 42 --db-url sqlite+aiosqlite:///./berunda.db
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import logging
import os
import random
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# Ensure src module is importable
_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.models import (
    Base,
    BackgroundJob,
    CaseAssignment,
    CaseMaster,
    Employee,
    EvidenceMaster,
    InvestigationNote,
    RelatedCaseSuggestion,
    ReportRequest,
    SupervisorReview,
    User,
    VehicleLink,
)

LOG = logging.getLogger("berunda.phase4")

DB_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./berunda.db")
CONFIG_PATH = Path(__file__).resolve().parent / "synthetic_config.json"

NOTE_TYPES = [
    "witness_statement",
    "scene_inspection",
    "forensic_result",
    "suspect_interview",
    "progress_update",
    "legal_reference",
    "arrest_note",
    "charge_sheet_note",
    "victim_update",
    "general",
]

REPORT_TYPES = [
    ("weekly_crime_summary", "Weekly crime summary"),
    ("officer_performance", "Officer performance metrics"),
    ("case_status_distribution", "Case status distribution"),
    ("clearance_rate", "Clearance rate analysis"),
    ("hotspot_analysis", "Crime hotspot analysis"),
    ("anomaly_alert_report", "Anomaly alert report"),
    ("entity_resolution", "Entity resolution progress"),
    ("investigation_quality", "Investigation quality audit"),
    ("district_comparison", "District-wise comparison"),
    ("monthly_trend", "Monthly crime trends"),
]

REVIEW_TYPES = [
    "periodic",
    "quality_assurance",
    "supervisory",
    "legal_compliance",
    "progress_assessment",
]

JOB_TYPES = [
    "entity_resolution",
    "hotspot_detection",
    "crime_forecast",
    "report_generation",
    "data_export",
    "anomaly_detection",
    "mo_analysis",
    "bulk_import",
    "data_validation",
    "cache_warmup",
]

NOTE_TEMPLATES = {
    "witness_statement": [
        "Recorded statement of {witness_name}, who stated that on the date of incident they saw {observation}. Statement recorded in the presence of panchas.",
        "Witness {witness_name} was examined under Section 180 BNS. They stated that they heard loud noises from {location} around {time} and saw {observation}.",
        "Supplementary statement of {witness_name} recorded. They provided additional details about {observation} which corroborates the existing evidence.",
    ],
    "scene_inspection": [
        "Scene of crime inspected in the presence of panchas. Noticed {observation} at the location. Photographs taken and site plan prepared.",
        "Detailed crime scene inspection conducted at {location}. Recovered {observation} from the spot. Samples collected for forensics.",
        "Second visit to crime scene conducted along with FSL team. {observation} found which was missed during the initial inspection.",
    ],
    "forensic_result": [
        "FSL report received. {observation} confirmed from the samples sent for analysis. Report attached to case diary.",
        "DNA analysis results received. {observation} matches the suspect's profile with 99.99% probability.",
        "Digital forensics report completed. {observation} extracted from the seized electronic devices.",
    ],
    "suspect_interview": [
        "Suspect {suspect_name} was interviewed at the police station. They admitted to {observation} but claimed it was under duress.",
        "Interrogation of {suspect_name} conducted. They provided information about {observation} which led to recovery of stolen property.",
        "Accused {suspect_name} was confronted with the evidence. They broke down and confessed to {observation}.",
    ],
    "progress_update": [
        "Investigation progress review: {observation}. Next steps planned including recording of remaining witnesses.",
        "Case diary submitted for period {start_date} to {end_date}. Investigation is progressing satisfactorily with {observation}.",
        "Weekly progress: {observation}. Notice under Section 175 BNSS issued to remaining witnesses.",
    ],
    "legal_reference": [
        "Relevant legal provisions discussed with the IO. {observation} as per the Supreme Court judgment in Criminal Appeal No. {appeal_no}.",
        "Legal opinion sought from the Public Prosecutor. They opined that {observation}.",
        "Bail application of accused opposed on grounds of {observation}.",
    ],
    "arrest_note": [
        "Accused arrested at {location} after receiving reliable information. {observation} recovered from their possession.",
        "Arrest of {suspect_name} effected under warrant. They were produced before the Hon'ble Court and remanded to judicial custody.",
        "Surrender of accused recorded. {observation} as per the court orders.",
    ],
    "charge_sheet_note": [
        "Charge sheet filed before the Hon'ble Court on {cs_date} under sections {sections}. {observation}.",
        "Final report submitted. After thorough investigation, it is concluded that {observation}.",
        "Supplementary charge sheet filed. {observation} based on newly discovered evidence.",
    ],
    "victim_update": [
        "Victim was informed about the progress of the investigation. {observation}.",
        "Victim compensation application filed. {observation} as per the Victim Compensation Scheme.",
        "Statement of victim recorded under Section 183 BNSS. {observation}.",
    ],
    "general": [
        "Case diary entry: {observation}. Further investigation is in progress.",
        "Received call from the control room regarding {observation}. Action taken as per procedure.",
        "Cross-verification of alibi completed. {observation}.",
    ],
}

EVIDENCE_DESCRIPTIONS = [
    "Blood-stained {item} recovered from the scene of crime and sent for forensic analysis",
    "{item} seized from the possession of the accused under a seizure memo",
    "{item} found near the location of incident and photographed",
    "{item} recovered during the course of investigation from {location}",
    "{item} handed over by the complainant for forensic examination",
    "{item} collected from the hospital where the victim was treated",
    "{item} extracted from the digital devices seized during investigation",
    "{item} discovered during the scene inspection and properly bagged and labeled",
]

REGISTRATION_NUMBERS = [
    "KA-01-MQ-1234",
    "KA-02-AB-5678",
    "KA-03-CD-9012",
    "KA-05-EF-3456",
    "KA-09-GH-7890",
    "KA-19-IJ-2345",
    "KA-25-KL-6789",
    "KA-27-MN-0123",
    "KA-35-OP-4567",
    "KA-01-QR-8901",
    "KA-05-ST-2345",
    "KA-03-UV-6789",
    "KA-09-WX-0123",
    "KA-19-YZ-4567",
    "KA-25-AB-8901",
    "KA-27-BC-2345",
    "KA-01-CD-6789",
    "KA-02-DE-0123",
    "KA-03-EF-4567",
    "KA-05-FG-8901",
]

VEHICLE_MODELS = [
    "Maruti Swift", "Honda Activa", "Hero Splendor", "Toyota Innova",
    "Bajaj Pulsar", "Honda City", "TVS Apache", "Royal Enfield Bullet",
    "Hyundai i10", "Bajaj RE Auto", "Mahindra Scorpio", "Tata Winger",
    "Yamaha FZ", "Suzuki Access", "Honda Shine", "Tata Indica",
]

COLLECTION_LOCATIONS = [
    "Crime scene - main building", "Near the entrance gate", "From the accused residence",
    "Hospital casualty ward", "Forensic lab chain-of-custody", "Seized from vehicle",
    "Recovered from pawn shop", "Digital evidence lab", "Police station strong room",
    "Scene of occurrence - roadside",
]


def deterministic_uuid(seed: int, label: str, index: int) -> uuid.UUID:
    """Generate a deterministic UUID from seed + label + index."""
    raw = f"berunda-phase4-{seed}-{label}-{index}"
    digest = hashlib.sha256(raw.encode()).hexdigest()
    return uuid.UUID(hex=digest[:32])


def format_id(seed: int, prefix: str, index: int) -> str:
    """Generate a deterministic string ID (for ReportID, JobID)."""
    raw = f"berunda-phase4-{seed}-{prefix}-{index}"
    digest = hashlib.md5(raw.encode()).hexdigest()[:12]
    return f"{prefix}-{digest}"


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


async def delete_existing_phase4_data(session: AsyncSession) -> dict[str, int]:
    """Delete all existing Phase 4 demo data. Returns counts of deleted rows."""
    targets = [
        ("InvestigationNote", InvestigationNote),
        ("CaseAssignment", CaseAssignment),
        ("SupervisorReview", SupervisorReview),
        ("RelatedCaseSuggestion", RelatedCaseSuggestion),
        ("ReportRequest", ReportRequest),
        ("VehicleLink", VehicleLink),
        ("EvidenceMaster", EvidenceMaster),
        ("BackgroundJob", BackgroundJob),
    ]
    counts = {}
    for name, model in targets:
        result = await session.execute(delete(model))
        counts[name] = result.rowcount
    await session.commit()
    return counts


def get_synthetic_note_content(
    note_type: str, case_id: int, rng: random.Random, config: dict
) -> str:
    """Generate realistic but clearly synthetic investigation note content."""
    templates = NOTE_TEMPLATES.get(note_type, NOTE_TEMPLATES["general"])

    person_names = config["person_names"]
    districts = config["districts"]
    locations = config["mo_slots"]["location"]
    time_periods = config["mo_slots"]["time_period"]

    witness_name = (
        rng.choice(person_names["male_first"] + person_names["female_first"])
        + " "
        + rng.choice(person_names["last_names"])
    )
    suspect_name = (
        rng.choice(person_names["male_first"]) + " " + rng.choice(person_names["last_names"])
    )
    location = rng.choice(locations)
    time = rng.choice(time_periods)

    template = rng.choice(templates)

    observations = [
        f"footprints matching the suspect's shoe size near the point of entry",
        f"fingerprints lifted from the {rng.choice(['window sill', 'door handle', 'glass piece', 'metal safe', 'wooden cabinet'])}",
        f"a broken lock and scattered documents indicating a search for valuables",
        f"the victim's {rng.choice(['mobile phone', 'watch', 'bag', 'purse', 'documents'])} was found abandoned nearby",
        f"partial vehicle tire marks consistent with a {rng.choice(['motorcycle', 'car', 'SUV'])}",
        f"discarded {rng.choice(['cigarette butts', 'matchbox', 'cloth piece', 'empty bottle', 'gloves'])} near the scene",
        f"CCTV footage showing an unknown person fleeing towards the {rng.choice(['north', 'south', 'east', 'west'])}",
        f"call detail records showing communication between the accused and the victim prior to the incident",
        f"financial transactions indicating motive related to {rng.choice(['property dispute', 'loan recovery', 'business rivalry', 'family settlement'])}",
        f"recovery of {rng.choice(['gold ornaments', 'cash amount', 'incriminating documents', 'electronic devices'])} from the accused",
    ]
    observation = rng.choice(observations)
    districts_list = [d["name"] for d in districts]

    return (
        f"SYNTHETIC INVESTIGATION NOTE — NOT REAL DATA\n"
        f"[NoteType: {note_type} | CaseMasterID: {case_id} | Seed context for reproducibility]\n\n"
        f"{template.format(
            witness_name=witness_name,
            suspect_name=suspect_name,
            location=location,
            time=time,
            observation=observation,
            start_date='2026-01-01',
            end_date='2026-01-15',
            appeal_no=str(rng.randint(1000, 9999)),
            cs_date='2026-03-15',
            sections='303, 305 BNS',
        )}\n\n"
        f"--- END OF SYNTHETIC NOTE ---"
    )


def get_synthetic_evidence_data(
    case_id: int, rng: random.Random, config: dict
) -> list[dict]:
    """Generate synthetic evidence records for a case."""
    evidence_types = config["evidence_types"]
    district_name = rng.choice(config["districts"])["name"]

    count = rng.randint(1, 3)
    records = []
    for i in range(count):
        ev_type = rng.choice(evidence_types)
        subtype = rng.choice(ev_type["subtypes"])
        item = subtype.lower()
        location = rng.choice(COLLECTION_LOCATIONS)
        file_formats = ["jpg", "pdf", "mp4", "docx", "txt", "png", "xlsx", "zip"]
        file_type = rng.choice(file_formats)

        description = rng.choice(EVIDENCE_DESCRIPTIONS).format(item=item, location=location)

        records.append(
            {
                "EvidenceID": None,
                "CaseMasterID": case_id,
                "EvidenceType": ev_type["name"],
                "Description": f"SYNTHETIC — {description}",
                "StoragePath": f"evidence/{case_id}/{rng.choice(['photos', 'documents', 'forensics', 'digital'])}/{deterministic_uuid(42, 'evpath', 999)}.{file_type}",
                "CollectedAt": datetime.now() - timedelta(days=rng.randint(1, 90)),
                "CollectedBy": rng.choice(config["person_names"]["male_first"])
                + " "
                + rng.choice(config["person_names"]["last_names"]),
                "Source": rng.choice(
                    ["scene_inspection", "witness", "forensic_lab", "accused_recovery", "cctv"]
                ),
                "Location": location,
                "Checksum": hashlib.sha256(
                    f"synth-evidence-{case_id}-{i}".encode()
                ).hexdigest()[:64],
                "FileType": file_type,
                "FileSize": rng.randint(10000, 50000000),
                "Status": rng.choices(
                    ["registered", "collected", "analyzed", "produced_in_court", "returned"],
                    weights=[20, 30, 25, 20, 5],
                    k=1,
                )[0],
                "Sensitivity": rng.choices(
                    ["normal", "sensitive", "confidential"], weights=[70, 20, 10], k=1
                )[0],
            }
        )
    return records


def get_synthetic_note_type(rng: random.Random) -> str:
    return rng.choices(
        NOTE_TYPES,
        weights=[15, 10, 10, 12, 18, 8, 10, 8, 5, 4],
        k=1,
    )[0]


async def generate_phase4_demo_data(
    session: AsyncSession, seed: int = 42, force: bool = False, dry_run: bool = False
) -> dict[str, int]:
    """
    Generate synthetic Phase 4 demo data.

    Returns a dict with counts of entities that would be / were created.
    """
    rng = random.Random(seed)
    config = load_config()
    stats: dict[str, int] = {}
    stats["seed"] = seed
    stats["dry_run"] = dry_run

    if force and not dry_run:
        deleted = await delete_existing_phase4_data(session)
        for k, v in deleted.items():
            LOG.info("Deleted %d existing %s records", v, k)

    # ── Load existing records ──────────────────────────────────────────────
    case_result = await session.execute(
        select(CaseMaster).order_by(CaseMaster.CaseMasterID)
    )
    cases = list(case_result.scalars().all())
    LOG.info("Found %d existing CaseMaster records in database", len(cases))
    stats["cases_found"] = len(cases)

    user_result = await session.execute(select(User).order_by(User.UserID))
    users = list(user_result.scalars().all())
    LOG.info("Found %d existing User records", len(users))
    stats["users_found"] = len(users)

    emp_result = await session.execute(select(Employee).order_by(Employee.EmployeeID))
    employees = list(emp_result.scalars().all())
    LOG.info("Found %d existing Employee records", len(employees))

    if not cases or not users:
        LOG.error("No CaseMaster or User records found. Seed the database first.")
        return {"error": "No CaseMaster or User records found"}

    # Deterministic allocations
    case_ids = [c.CaseMasterID for c in cases]
    user_ids = [u.UserID for u in users]
    emp_ids = [e.EmployeeID for e in employees]

    investigator_emps = [e for e in employees if e.DesignationID == 2] or employees
    supervisor_emps = [e for e in employees if e.DesignationID == 1] or employees

    LOG.info("Employees: %d total, %d investigators, %d supervisors",
             len(employees), len(investigator_emps), len(supervisor_emps))

    # ── 1. Investigation Notes ─────────────────────────────────────────────
    note_count = 0
    notes_to_add = []
    for idx, cm_id in enumerate(case_ids):
        notes_per_case = rng.randint(1, 4)
        for n_idx in range(notes_per_case):
            note_count += 1
            note_type = get_synthetic_note_type(rng)
            content = get_synthetic_note_content(note_type, cm_id, rng, config)
            author_id = rng.choice(user_ids)
            created_at = datetime.now() - timedelta(
                days=rng.randint(1, 120), hours=rng.randint(0, 23)
            )
            visibility = rng.choices(
                ["station", "district", "confidential"],
                weights=[60, 30, 10],
                k=1,
            )[0]

            note = InvestigationNote(
                CaseMasterID=cm_id,
                AuthorID=author_id,
                NoteType=note_type,
                Content=content,
                IsAmendment=False,
                OriginalNoteID=None,
                Visibility=visibility,
                CreatedAt=created_at,
                UpdatedAt=created_at,
            )
            if not dry_run:
                session.add(note)
            notes_to_add.append(
                {
                    "CaseMasterID": cm_id,
                    "AuthorID": author_id,
                    "NoteType": note_type,
                    "Visibility": visibility,
                }
            )
    stats["investigation_notes"] = note_count
    LOG.info("  Investigation notes: %d", note_count)

    # ── 2. Case Assignments ────────────────────────────────────────────────
    assignment_count = 0
    assignments_to_add = []
    # Assign each case to an officer
    for idx, cm_id in enumerate(case_ids):
        assignment_count += 1
        # Rotate through investigators deterministically
        investigator = investigator_emps[idx % len(investigator_emps)]
        assignor = rng.choice(user_ids)
        created_at = datetime.now() - timedelta(
            days=rng.randint(1, 120), hours=rng.randint(0, 23)
        )

        status = rng.choices(
            ["active", "completed", "reassigned"],
            weights=[60, 30, 10],
            k=1,
        )[0]
        ended_at = (
            created_at + timedelta(days=rng.randint(30, 90)) if status != "active" else None
        )

        reasons = [
            "Primary IO assigned based on jurisdiction",
            "Experienced officer assigned for complex investigation",
            "Reassigned due to workload balancing",
            "Specialized investigator for cyber crime cases",
            "DSP directive - priority case",
            "Transfer of original IO - reassigned",
            "Additional IO appointed for multi-district case",
            "Junior officer attached for training purposes",
        ]
        reason = rng.choice(reasons)

        assignment = CaseAssignment(
            CaseMasterID=cm_id,
            AssignedOfficerID=investigator.EmployeeID,
            AssignedByUserID=assignor,
            AssignmentReason=reason,
            Status=status,
            AssignedAt=created_at,
            EndedAt=ended_at,
        )
        if not dry_run:
            session.add(assignment)
        assignments_to_add.append(
            {
                "CaseMasterID": cm_id,
                "AssignedOfficerID": investigator.EmployeeID,
                "Status": status,
            }
        )
    stats["case_assignments"] = assignment_count
    LOG.info("  Case assignments: %d", assignment_count)

    # ── 3. Supervisor Reviews ──────────────────────────────────────────────
    review_count = 0
    reviews_to_add = []
    # ~70% of cases get supervisor reviews, some get multiple
    for cm_id in case_ids:
        if rng.random() > 0.70:
            continue
        review_count += 1
        supervisor = rng.choice(supervisor_emps) if supervisor_emps else rng.choice(employees)
        supervisor_user = rng.choice(user_ids)

        review_type = rng.choice(REVIEW_TYPES)
        status = rng.choices(
            ["pending", "acknowledged", "resolved", "escalated"],
            weights=[15, 30, 45, 10],
            k=1,
        )[0]

        review_comments = [
            f"Review of investigation progress: {'Satisfactory' if status != 'escalated' else 'Needs improvement'}. "
            f"IO directed to expedite witness examination and collect remaining forensic reports.",
            f"Case reviewed as part of {'quality assurance' if review_type == 'quality_assurance' else 'routine'} process. "
            f"Observation: {'All procedures followed correctly' if status != 'escalated' else 'Some gaps identified in evidence collection'}. "
            f"Review type: {review_type}.",
            f"Periodic review of case #{cm_id}. Investigation is {'on track' if status != 'escalated' else 'behind schedule'}. "
            f"Recommended actions: {'File charge sheet within 15 days' if rng.random() > 0.5 else 'Record remaining witness statements urgently'}.",
        ]

        actions = [
            "Complete forensic analysis",
            "Record remaining witness statements",
            "File charge sheet within 15 days",
            "Issue notice to witnesses under Section 175 BNSS",
            "Coordinate with FSL for expedited reports",
            "Trace and arrest absconding accused",
            "Collect call detail records from telecom provider",
            "Submit CCTV footage analysis report",
            "Update case diary with recent findings",
            "Recommend closure based on B report",
        ]

        reviewed_at = datetime.now() - timedelta(
            days=rng.randint(1, 60), hours=rng.randint(0, 23)
        )

        review = SupervisorReview(
            CaseMasterID=cm_id,
            SupervisorID=supervisor_user,
            ReviewType=review_type,
            Status=status,
            Comments=rng.choice(review_comments),
            ActionRequested=rng.choice(actions),
            ReviewedAt=reviewed_at,
        )
        if not dry_run:
            session.add(review)
        reviews_to_add.append(
            {
                "CaseMasterID": cm_id,
                "SupervisorID": supervisor_user,
                "ReviewType": review_type,
                "Status": status,
            }
        )
    stats["supervisor_reviews"] = review_count
    LOG.info("  Supervisor reviews: %d", review_count)

    # ── 4. Related Case Suggestions ────────────────────────────────────────
    suggestion_count = 0
    suggestions_to_add = []
    signal_templates = [
        "shared_vehicle:{}",
        "same_accused:{}",
        "similar_mo:{}",
        "overlapping_witness:{}",
        "same_location:{}",
        "phone_contact:{}",
        "same_complainant:{}",
        "shared_evidence:{}",
        "temporal_proximity:{}",
        "same_crime_head:{}",
    ]

    if len(case_ids) >= 3:
        # Create meaningful suggestions based on similarity patterns
        for i in range(min(len(case_ids), len(case_ids))):
            source_id = case_ids[i]
            # Pick a different case as candidate
            candidates_pool = [c for c in case_ids if c != source_id]
            if not candidates_pool:
                continue
            num_suggestions = rng.randint(1, min(3, len(candidates_pool)))
            pool = rng.sample(candidates_pool, num_suggestions)

            for candidate_id in pool:
                suggestion_count += 1
                confidence = round(rng.uniform(0.55, 0.98), 4)
                num_signals = rng.randint(1, 4)
                signals_used = rng.sample(signal_templates, num_signals)
                signal_text = "; ".join(
                    [s.format(deterministic_uuid(seed, "sig", 999)) for s in signals_used]
                )

                explanation_patterns = [
                    f"Both cases involve similar modus operandi (confidence: {confidence}). "
                    f"The accused in case #{source_id} has been linked to case #{candidate_id} "
                    f"through shared MO patterns and witness accounts.",
                    f"Vehicle registration {rng.choice(REGISTRATION_NUMBERS)} appears in both cases "
                    f"(confidence: {confidence}). Suggesting possible link between the incidents.",
                    f"Common accused name pattern detected across cases (confidence: {confidence}). "
                    f"Entity resolution pipeline suggests a single perpetrator.",
                    f"Temporal and spatial proximity (confidence: {confidence}). Cases occurred "
                    f"within {rng.randint(1, 5)} km and {rng.randint(1, 14)} days of each other.",
                    f"Shared phone contact detected in call records (confidence: {confidence}). "
                    f"A common phone number was in contact with complainants in both cases.",
                ]

                review_status = rng.choices(
                    ["suggested", "under_review", "confirmed", "rejected"],
                    weights=[50, 25, 15, 10],
                    k=1,
                )[0]

                suggestion = RelatedCaseSuggestion(
                    SourceFIRID=source_id,
                    CandidateFIRID=candidate_id,
                    ConfidenceScore=confidence,
                    SupportingSignals=signal_text,
                    Explanation=rng.choice(explanation_patterns),
                    ModelVersion="hybrid-v2.1",
                    ReviewStatus=review_status,
                    ReviewedByUserID=rng.choice(user_ids) if review_status in ("confirmed", "rejected") else None,
                    ReviewReason=(
                        "Confirmed by supervising officer" if review_status == "confirmed"
                        else "Insufficient evidence to link" if review_status == "rejected"
                        else None
                    ),
                    ReviewedAt=(
                        datetime.now() - timedelta(days=rng.randint(1, 30))
                        if review_status in ("confirmed", "rejected")
                        else None
                    ),
                )
                if not dry_run:
                    session.add(suggestion)
                suggestions_to_add.append(
                    {
                        "SourceFIRID": source_id,
                        "CandidateFIRID": candidate_id,
                        "ConfidenceScore": confidence,
                        "ReviewStatus": review_status,
                    }
                )
    stats["related_case_suggestions"] = suggestion_count
    LOG.info("  Related case suggestions: %d", suggestion_count)

    # ── 5. Report Requests ─────────────────────────────────────────────────
    report_count = 0
    reports_to_add = []
    for idx, (report_type, report_desc) in enumerate(REPORT_TYPES):
        report_count += 1
        requester_id = rng.choice(user_ids)
        report_id = format_id(seed, "RPT", idx + 1)

        status = rng.choices(
            ["requested", "processing", "completed", "failed"],
            weights=[15, 10, 70, 5],
            k=1,
        )[0]
        file_format = rng.choice(["pdf", "csv", "xlsx", "json"])

        parameters = {
            "district_ids": rng.sample(range(1, 32), rng.randint(1, 5)),
            "date_from": (datetime.now() - timedelta(days=90)).isoformat(),
            "date_to": datetime.now().isoformat(),
            "include_charts": True,
            "group_by": rng.choice(["district", "crime_head", "station", "month"]),
            "filters": {
                "case_status": rng.choice(["all", "active", "closed"]),
                "crime_type": rng.choice(["all", "property", "violent", "economic"]),
            },
        }

        error_message = (
            "Report generation failed: data not available for requested period" if status == "failed" else None
        )

        report = ReportRequest(
            ReportID=report_id,
            RequestedByUserID=requester_id,
            ReportType=report_type,
            Parameters=json.dumps(parameters, ensure_ascii=False),
            Status=status,
            FileFormat=file_format,
            ErrorMessage=error_message,
            CompletedAt=(
                datetime.now() - timedelta(hours=rng.randint(1, 48))
                if status == "completed"
                else None
            ),
            ExpiresAt=(
                datetime.now() + timedelta(days=30)
                if status == "completed"
                else None
            ),
            StorageObjectRef=f"reports/{report_id}.{file_format}" if status == "completed" else None,
        )
        if not dry_run:
            session.add(report)
        reports_to_add.append(
            {
                "ReportID": report_id,
                "ReportType": report_type,
                "Status": status,
            }
        )
    stats["report_requests"] = report_count
    LOG.info("  Report requests: %d", report_count)

    # ── 6. Vehicle Links ───────────────────────────────────────────────────
    vehicle_count = 0
    vehicles_to_add = []
    linked_cases = set()
    existing_vehicles = set()

    # Check for existing vehicle links
    existing_vl_result = await session.execute(select(VehicleLink))
    for vl in existing_vl_result.scalars().all():
        existing_vehicles.add(vl.VehicleNumber)

    # Create vehicle links for ~30% of cases
    for cm_id in case_ids:
        if rng.random() > 0.30:
            continue
        vehicle_count += 1
        reg_no = rng.choice(REGISTRATION_NUMBERS)
        if reg_no not in existing_vehicles:
            existing_vehicles.add(reg_no)

        model = rng.choice(VEHICLE_MODELS)
        vtype = "Motorcycle" if any(m in model for m in ["Splendor", "Activa", "Apache", "Pulsar", "FZ", "Bullet", "Shine", "Access"]) else \
                "Car" if any(m in model for m in ["Swift", "i10", "City", "Indica", "Innova", "Scorpio", "Creta", "Alto"]) else \
                "Auto-Rickshaw" if "Auto" in model else \
                "SUV" if any(m in model for m in ["Scorpio", "Fortuner", "Safari"]) else \
                "Van"
        confidence = round(rng.uniform(0.65, 0.99), 4)
        source = rng.choices(
            ["witness", "cctv", "ner", "manual", "forensic"],
            weights=[30, 25, 15, 20, 10],
            k=1,
        )[0]

        vehicle_link = VehicleLink(
            VehicleNumber=reg_no,
            CaseMasterID=cm_id,
            Confidence=confidence,
            Source=source,
        )
        if not dry_run:
            session.add(vehicle_link)
        vehicles_to_add.append(
            {
                "VehicleNumber": reg_no,
                "CaseMasterID": cm_id,
                "Confidence": confidence,
                "Source": source,
            }
        )
        linked_cases.add(cm_id)

    # Create a shared vehicle pattern (same vehicle across 2-3 cases)
    if len(case_ids) >= 3:
        shared_reg = rng.choice(REGISTRATION_NUMBERS)
        shared_cases = rng.sample(case_ids, min(3, len(case_ids)))
        for scm_id in shared_cases:
            vehicle_count += 1
            vehicle_link = VehicleLink(
                VehicleNumber=shared_reg,
                CaseMasterID=scm_id,
                Confidence=round(rng.uniform(0.85, 0.99), 4),
                Source="ner",
            )
            if not dry_run:
                session.add(vehicle_link)
            vehicles_to_add.append(
                {
                    "VehicleNumber": shared_reg,
                    "CaseMasterID": scm_id,
                    "Confidence": 0.95,
                    "Source": "ner",
                }
            )
    stats["vehicle_links"] = vehicle_count
    LOG.info("  Vehicle links: %d", vehicle_count)

    # ── 7. Evidence Master Records ─────────────────────────────────────────
    evidence_count = 0
    evidence_to_add = []
    for cm_id in case_ids:
        if rng.random() > 0.45:
            continue
        ev_records = get_synthetic_evidence_data(cm_id, rng, config)
        for ev_data in ev_records:
            evidence_count += 1
            evidence = EvidenceMaster(
                CaseMasterID=ev_data["CaseMasterID"],
                EvidenceType=ev_data["EvidenceType"],
                Description=ev_data["Description"],
                StoragePath=ev_data["StoragePath"],
                CollectedAt=ev_data["CollectedAt"],
                CollectedBy=ev_data["CollectedBy"],
                Source=ev_data["Source"],
                Location=ev_data["Location"],
                Checksum=ev_data["Checksum"],
                FileType=ev_data["FileType"],
                FileSize=ev_data["FileSize"],
                Status=ev_data["Status"],
                Sensitivity=ev_data["Sensitivity"],
            )
            if not dry_run:
                session.add(evidence)
            evidence_to_add.append(
                {
                    "CaseMasterID": cm_id,
                    "EvidenceType": ev_data["EvidenceType"],
                    "Status": ev_data["Status"],
                }
            )
    stats["evidence_records"] = evidence_count
    LOG.info("  Evidence records: %d", evidence_count)

    # ── 8. Background Jobs ─────────────────────────────────────────────────
    job_count = 0
    jobs_to_add = []
    for idx, job_type in enumerate(JOB_TYPES):
        job_count += 1
        requester_id = rng.choice(user_ids) if rng.random() > 0.2 else None
        job_id = format_id(seed, "JOB", idx + 1)
        id_key = hashlib.md5(
            f"berunda-phase4-{seed}-job-{job_type}".encode()
        ).hexdigest()[:32]

        status = rng.choices(
            ["queued", "running", "completed", "failed", "cancelled"],
            weights=[10, 5, 70, 10, 5],
            k=1,
        )[0]

        payload_template = {
            "entity_resolution": {
                "algorithm": "hybrid-ensemble-v2",
                "threshold": 0.75,
                "batch_size": 100,
                "entity_types": ["accused", "complainant", "victim"],
            },
            "hotspot_detection": {
                "algorithm": "dbscan",
                "eps_km": 2.0,
                "min_samples": 5,
                "districts": rng.sample(range(1, 32), rng.randint(1, 5)),
            },
            "crime_forecast": {
                "model": "timeseries-lstm-v3",
                "forecast_days": 30,
                "confidence_interval": 0.95,
                "crime_heads": rng.sample(range(1, 21), rng.randint(3, 8)),
            },
            "report_generation": {
                "report_template": rng.choice([r[0] for r in REPORT_TYPES]),
                "format": "pdf",
                "schedule": "once",
            },
            "data_export": {
                "tables": rng.sample(
                    ["src_CaseMaster", "int_PersonEntity", "int_VehicleLink", "src_EvidenceMaster"],
                    rng.randint(1, 3),
                ),
                "format": rng.choice(["csv", "json", "parquet"]),
                "date_range": {"from": "2024-01-01", "to": "2026-12-31"},
            },
            "anomaly_detection": {
                "method": "zscore",
                "z_threshold": 2.0,
                "window_days": 30,
                "district_ids": rng.sample(range(1, 32), rng.randint(2, 8)),
            },
            "mo_analysis": {
                "embedding_model": "all-MiniLM-L6-v2",
                "cluster_method": "kmeans",
                "n_clusters": rng.randint(3, 8),
            },
            "bulk_import": {
                "source": rng.choice(["csv_upload", "api_batch", "legacy_migration"]),
                "record_count": rng.randint(500, 5000),
                "entity_type": rng.choice(["cases", "persons", "evidence"]),
            },
            "data_validation": {
                "checks": ["schema", "nulls", "duplicates", "foreign_keys"],
                "scope": rng.choice(["all_tables", "src_schema", "int_schema"]),
            },
            "cache_warmup": {
                "cache_keys": [
                    "hotspot:summary",
                    "dashboard:stats",
                    "crime:trends",
                    "entity:counts",
                ],
                "priority": rng.choice(["high", "medium", "low"]),
            },
        }

        payload = payload_template.get(job_type, {"task": job_type, "params": {"seed": seed}})

        error_message = (
            "Job failed: timeout exceeded" if status == "failed"
            else "Job cancelled by user" if status == "cancelled"
            else None
        )

        created_at = datetime.now() - timedelta(
            days=rng.randint(0, 30), hours=rng.randint(0, 23)
        )
        started_at = (
            created_at + timedelta(minutes=rng.randint(1, 30))
            if status in ("running", "completed", "failed")
            else None
        )
        completed_at = (
            started_at + timedelta(minutes=rng.randint(5, 120))
            if status == "completed"
            else None
        )

        attempt_count = 0
        if status == "completed":
            attempt_count = 1
        elif status == "failed":
            attempt_count = rng.randint(1, 3)

        job = BackgroundJob(
            JobID=job_id,
            JobType=job_type,
            Payload=json.dumps(payload, ensure_ascii=False),
            IdempotencyKey=id_key,
            RequestedByUserID=requester_id,
            Status=status,
            AttemptCount=attempt_count,
            MaxAttempts=3,
            ResultRef=(
                f"results/{job_id}/output_{completed_at.strftime('%Y%m%d_%H%M%S')}.json"
                if status == "completed"
                else None
            ),
            ErrorMessage=error_message,
            CreatedAt=created_at,
            StartedAt=started_at,
            CompletedAt=completed_at,
        )
        if not dry_run:
            session.add(job)
        jobs_to_add.append(
            {
                "JobID": job_id,
                "JobType": job_type,
                "Status": status,
            }
        )
    stats["background_jobs"] = job_count
    LOG.info("  Background jobs: %d", job_count)

    # ── Commit ─────────────────────────────────────────────────────────────
    if not dry_run:
        await session.commit()
        LOG.info("All Phase 4 data committed to database.")
    else:
        LOG.info("DRY RUN — no data written.")

    return stats


async def main():
    parser = argparse.ArgumentParser(
        description="Generate Phase 4 synthetic demo data for Berunda"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--dry-run", action="store_true", help="Log what would be created without writing")
    parser.add_argument("--force", action="store_true", help="Delete existing Phase 4 data first")
    parser.add_argument(
        "--db-url",
        default=DB_URL,
        help="Async database URL (default: from DATABASE_URL or sqlite+aiosqlite:///./berunda.db)",
    )
    parser.add_argument("--verbose", action="store_true", help="Detailed logging")
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )

    # Suppress noisy SQLAlchemy logs
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    LOG.info("Phase 4 demo data generator starting...")
    LOG.info("  Seed: %d", args.seed)
    LOG.info("  Dry run: %s", args.dry_run)
    LOG.info("  Force: %s", args.force)
    LOG.info("  DB URL: %s", args.db_url)

    engine = create_async_engine(args.db_url, echo=False)
    async_session_local = sessionmaker(engine, class_=AsyncSession)

    async with async_session_local() as session:
        stats = await generate_phase4_demo_data(
            session, seed=args.seed, force=args.force, dry_run=args.dry_run
        )

    await engine.dispose()

    LOG.info("=" * 60)
    LOG.info("Phase 4 Demo Data Generation Summary")
    LOG.info("=" * 60)

    entity_names = {
        "investigation_notes": "Investigation Notes",
        "case_assignments": "Case Assignments",
        "supervisor_reviews": "Supervisor Reviews",
        "related_case_suggestions": "Related Case Suggestions",
        "report_requests": "Report Requests",
        "vehicle_links": "Vehicle Links",
        "evidence_records": "Evidence Records",
        "background_jobs": "Background Jobs",
    }

    total = 0
    for key, label in entity_names.items():
        count = stats.get(key, 0)
        LOG.info("  %s: %s", label.ljust(30), count)
        total += count

    LOG.info("  %s", "-" * 40)
    LOG.info("  %s: %s", "TOTAL ENTITIES".ljust(30), total)
    LOG.info("  Mode: %s", "DRY RUN (no data written)" if args.dry_run else "LIVE (data committed)")
    LOG.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
