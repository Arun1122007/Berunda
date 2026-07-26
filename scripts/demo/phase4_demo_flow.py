"""
Phase 4 Hackathon Demo Flow Script.

Walks through the complete Phase 4 MVP workflow:
  officer login -> FIR ops -> investigation -> related cases
  -> supervisor login -> dashboard -> review -> report -> audit

Usage:
    python scripts/demo/phase4_demo_flow.py [--base-url http://localhost:9000]
    python scripts/demo/phase4_demo_flow.py --wait

Requires: httpx (pip install httpx)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

try:
    import httpx
except ImportError:
    httpx = None  # type: ignore[assignment]


# -- helpers -----------------------------------------------------------------

def print_step(step_num: int, description: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  STEP {step_num}: {description}")
    print(f"{'=' * 60}")


def print_ok(label: str, detail: str = "") -> None:
    pad = 45
    dots = "." * max(1, pad - len(label))
    print(f"    [OK] {label} {dots} {detail}" if detail else f"    [OK] {label}")


def print_skip(label: str, reason: str = "server unreachable") -> None:
    print(f"    [SKIP] {label} ({reason})")


def print_fail(label: str, detail: str = "") -> None:
    print(f"    [FAIL] {label} {detail}".strip())


def trunc(obj: dict | list | str, max_len: int = 120) -> str:
    s = json.dumps(obj, indent=2, default=str) if not isinstance(obj, str) else obj
    return s if len(s) <= max_len else s[:max_len] + "..."


# -- demo credentials -------------------------------------------------------

DEMO_OFFICER_EMAIL = "officer@berunda.gov"
DEMO_OFFICER_PASSWORD = "officer123"

DEMO_SUPERVISOR_EMAIL = "supervisor@berunda.gov"
DEMO_SUPERVISOR_PASSWORD = "supervisor123"

CASE_ID = 1


# -- API helpers -------------------------------------------------------------

def api_call(
    client: httpx.Client,
    method: str,
    path: str,
    label: str,
    *,
    json_body: dict | None = None,
    token: str | None = None,
    expected: int | range = 200,
) -> dict | list | None:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    url = f"{client.base_url}{path}"

    try:
        resp = client.request(method, url, json=json_body, headers=headers, timeout=10)
    except (httpx.ConnectError, httpx.TimeoutException) as exc:
        print_skip(label, str(exc))
        return None

    ok = resp.status_code == expected if isinstance(expected, int) else resp.status_code in expected

    if ok:
        try:
            data = resp.json()
        except Exception:
            data = resp.text
        print_ok(label, f"{resp.status_code} {trunc(data)}")
        return data
    else:
        detail = f"{resp.status_code} {trunc(resp.text)}"
        print_fail(label, detail)
        return None


def server_alive(client: httpx.Client) -> bool:
    try:
        r = client.get("/health", timeout=5)
        return r.status_code < 500
    except Exception:
        return False


def wait_for_server(client: httpx.Client, retries: int = 12, delay: float = 5.0) -> bool:
    for attempt in range(1, retries + 1):
        if server_alive(client):
            return True
        print(f"  [WAIT] Polling server (attempt {attempt}/{retries})...")
        time.sleep(delay)
    return False


# -- demo flow ---------------------------------------------------------------

def demo_flow(base_url: str, wait: bool) -> None:
    if httpx is None:
        print("ERROR: httpx is required. Install with: pip install httpx")
        sys.exit(1)

    client = httpx.Client(base_url=base_url)

    alive = server_alive(client)
    if wait and not alive:
        alive = wait_for_server(client)

    if not alive:
        print("  [WARN] Server not reachable. Running OFFLINE demo.\n")
        _run_offline_demo()
        return

    _run_live_demo(client)


def _run_live_demo(client: httpx.Client) -> None:
    tokens: dict[str, str] = {}

    # ---- STEP 1: Authenticate as officer -----------------------------------
    print_step(1, "Authenticate as Investigating Officer")
    officer_login = api_call(
        client, "POST", "/api/v1/auth/login",
        "Login officer",
        json_body={"email": DEMO_OFFICER_EMAIL, "password": DEMO_OFFICER_PASSWORD},
    )
    if officer_login and isinstance(officer_login, dict):
        officer_token = officer_login["token"]
        officer_user = officer_login.get("user", {})
        print_ok("Officer session", f"userId={officer_user.get('userId')} role={officer_user.get('role')}")
        tokens["officer"] = officer_token
    else:
        print("  [WARN] Officer login failed -- trying register+login fallback...")
        api_call(client, "POST", "/api/v1/auth/register", "Register officer",
                 json_body={"email": DEMO_OFFICER_EMAIL, "password": DEMO_OFFICER_PASSWORD,
                            "role": "officer", "district_id": 5},
                 expected=range(200, 410))
        officer_login = api_call(
            client, "POST", "/api/v1/auth/login",
            "Login officer (retry)",
            json_body={"email": DEMO_OFFICER_EMAIL, "password": DEMO_OFFICER_PASSWORD},
        )
        if officer_login and isinstance(officer_login, dict):
            officer_token = officer_login["token"]
            tokens["officer"] = officer_token
        else:
            print("  [WARN] Officer auth unavailable -- continuing without token")
            officer_token = ""

    # ---- STEP 2: List assigned FIRs ----------------------------------------
    print_step(2, "List Assigned FIRs")
    api_call(client, "GET", "/api/v1/fir?page=1&page_size=5", "List FIRs",
             token=tokens.get("officer"))

    # ---- STEP 3: Open FIR detail -------------------------------------------
    print_step(3, "Open FIR Detail")
    api_call(client, "GET", f"/api/v1/fir/{CASE_ID}", f"Get FIR #{CASE_ID}",
             token=tokens.get("officer"))

    # ---- STEP 4: Add investigation note ------------------------------------
    print_step(4, "Add Investigation Note")
    note_data = {
        "Content": "Visited crime scene at 10th Cross, MG Road. "
                   "Collected fingerprints from rear door. "
                   "Two eyewitnesses identified -- statements recorded.",
        "NoteType": "field_visit",
        "Visibility": "station",
    }
    api_call(client, "POST", f"/api/v1/fir/{CASE_ID}/notes", "Create note",
             json_body=note_data, token=tokens.get("officer"), expected=201)

    # ---- STEP 5: Link vehicle ----------------------------------------------
    print_step(5, "Link Vehicle to Case")
    api_call(client, "POST", f"/api/v1/fir/{CASE_ID}/evidence",
             "Upload vehicle evidence (KA-01-MQ-1234)",
             json_body={"description": "Suspect vehicle photo -- KA-01-MQ-1234"},
             token=tokens.get("officer"), expected=201)

    # ---- STEP 6: Upload evidence -------------------------------------------
    print_step(6, "Upload Evidence Document")
    api_call(client, "POST", f"/api/v1/fir/{CASE_ID}/evidence",
             "Upload forensic report",
             json_body={"description": "Forensic analysis report -- fingerprints matched"},
             token=tokens.get("officer"), expected=201)

    # ---- STEP 7: Update case status ----------------------------------------
    print_step(7, "Update Case Status")
    status_data = {
        "CaseStatusID": 2,
        "Reason": "Preliminary investigation complete. "
                  "Evidence collected and witness statements recorded.",
    }
    api_call(client, "PUT", f"/api/v1/fir/{CASE_ID}/status",
             "Update status to charge-sheeted",
             json_body=status_data, token=tokens.get("officer"))

    # ---- STEP 8: Generate related cases ------------------------------------
    print_step(8, "Generate Related Case Suggestions")
    related = api_call(client, "POST", f"/api/v1/fir/{CASE_ID}/related-cases/generate",
                       "Generate related cases", token=tokens.get("officer"))

    # ---- STEP 9: Review and accept suggestion ------------------------------
    print_step(9, "Review and Accept Related Case Suggestion")
    suggestion_id = None
    if related and isinstance(related, list) and len(related) > 0:
        suggestion_id = related[0].get("SuggestionID")
    if suggestion_id:
        api_call(client, "PUT", f"/api/v1/fir/related-cases/{suggestion_id}/review",
                 "Accept suggestion",
                 json_body={"ReviewStatus": "accepted",
                            "ReviewReason": "Same vehicle plate: KA-01-MQ-1234"},
                 token=tokens.get("officer"))
    else:
        print_skip("Accept suggestion", "no suggestions returned")

    # ---- STEP 10: View case timeline ---------------------------------------
    print_step(10, "View Case Timeline")
    api_call(client, "GET", f"/api/v1/fir/{CASE_ID}/timeline", "Get timeline",
             token=tokens.get("officer"))

    # ---- STEP 11: Authenticate as supervisor -------------------------------
    print_step(11, "Authenticate as Supervisor")
    supervisor_login = api_call(
        client, "POST", "/api/v1/auth/login",
        "Login supervisor",
        json_body={"email": DEMO_SUPERVISOR_EMAIL, "password": DEMO_SUPERVISOR_PASSWORD},
    )
    if supervisor_login and isinstance(supervisor_login, dict):
        supervisor_token = supervisor_login["token"]
        sup_user = supervisor_login.get("user", {})
        print_ok("Supervisor session", f"userId={sup_user.get('userId')} role={sup_user.get('role')}")
        tokens["supervisor"] = supervisor_token
    else:
        print("  [WARN] Supervisor login failed -- trying register fallback...")
        api_call(client, "POST", "/api/v1/auth/register", "Register supervisor",
                 json_body={"email": DEMO_SUPERVISOR_EMAIL, "password": DEMO_SUPERVISOR_PASSWORD,
                            "role": "supervisor", "district_id": 5},
                 expected=range(200, 410))
        supervisor_login = api_call(
            client, "POST", "/api/v1/auth/login",
            "Login supervisor (retry)",
            json_body={"email": DEMO_SUPERVISOR_EMAIL, "password": DEMO_SUPERVISOR_PASSWORD},
        )
        if supervisor_login and isinstance(supervisor_login, dict):
            supervisor_token = supervisor_login["token"]
            tokens["supervisor"] = supervisor_token
        else:
            supervisor_token = ""

    # ---- STEP 12: View supervisor dashboard --------------------------------
    print_step(12, "View Supervisor Dashboard")
    api_call(client, "GET", "/api/v1/dashboard/supervisor",
             "Supervisor dashboard", token=tokens.get("supervisor"))
    api_call(client, "GET", "/api/v1/dashboard/activity",
             "Recent activity", token=tokens.get("supervisor"))

    # ---- STEP 13: Review case progress -------------------------------------
    print_step(13, "Review Case Progress")
    api_call(client, "GET", f"/api/v1/fir/{CASE_ID}/notes",
             "List notes", token=tokens.get("supervisor"))
    api_call(client, "GET", f"/api/v1/fir/{CASE_ID}/evidence",
             "List evidence", token=tokens.get("supervisor"))
    review_data = {
        "ReviewType": "progress_review",
        "Status": "approved",
        "Comments": "Investigation thorough. Evidence chain preserved. "
                     "Witness statements properly documented. Approving progress.",
        "ActionRequested": "File charge sheet by end of week.",
    }
    api_call(client, "POST", f"/api/v1/fir/{CASE_ID}/reviews",
             "Submit supervisor review",
             json_body=review_data, token=tokens.get("supervisor"), expected=201)

    # ---- STEP 14: Request a report -----------------------------------------
    print_step(14, "Request Investigation Progress Report")
    report_req = api_call(client, "POST", "/api/v1/reports",
                          "Request report",
                          json_body={
                              "ReportType": "investigation_progress",
                              "Parameters": json.dumps({"case_master_id": CASE_ID, "include_evidence": True}),
                              "FileFormat": "pdf",
                          },
                          token=tokens.get("supervisor"), expected=201)

    # ---- STEP 15: Generate the report --------------------------------------
    print_step(15, "Generate the Report")
    report_id = None
    if report_req and isinstance(report_req, dict):
        report_id = report_req.get("ReportID")
    if report_id:
        api_call(client, "POST", f"/api/v1/reports/{report_id}/generate",
                 f"Generate report {report_id}",
                 token=tokens.get("supervisor"))
        api_call(client, "GET", f"/api/v1/reports/{report_id}",
                 "Get report status", token=tokens.get("supervisor"))
    else:
        print_skip("Generate report", "no report_id returned")

    # ---- STEP 16: View audit trail -----------------------------------------
    print_step(16, "View Audit Trail")
    api_call(client, "GET",
             f"/api/v1/audit?entity_type=src_CaseMaster&entity_id={CASE_ID}",
             "View audit trail for case",
             token=tokens.get("supervisor"))

    # -- complete ------------------------------------------------------------
    print(f"\n\n{'=' * 62}")
    print(f"  PHASE 4 DEMO COMPLETE")
    print(f"  Roles: officer -> supervisor")
    print(f"  Case: CM-{CASE_ID}")
    print(f"  16 workflow steps executed (live)")
    print(f"{'=' * 62}")


def _run_offline_demo() -> None:
    """Simulate all 16 steps without a running server."""
    print("  [OFFLINE MODE -- responses are simulated]\n")

    # STEP 1
    print_step(1, "Authenticate as Investigating Officer")
    print_ok("Login officer", "200 userId=2 role=officer")

    # STEP 2
    print_step(2, "List Assigned FIRs")
    print_ok("List FIRs",
             '200 {"total":5,"items":["KA-01-001","KA-01-002","KA-01-003","KA-01-005","KA-01-HS-001"]}')

    # STEP 3
    print_step(3, "Open FIR Detail")
    print_ok("Get FIR #1",
             '200 {"CaseMasterID":1,"CrimeNo":"KA-01-001","BriefFacts":"Theft of mobile phone","CaseStatusID":1}')

    # STEP 4
    print_step(4, "Add Investigation Note")
    print_ok("Create note", "201 NoteID=101 -- field_visit note stored")

    # STEP 5
    print_step(5, "Link Vehicle to Case")
    print_ok("Upload vehicle evidence", "201 KA-01-MQ-1234 linked to case")

    # STEP 6
    print_step(6, "Upload Evidence Document")
    print_ok("Upload forensic report", "201 EvidenceID=202 -- report stored")

    # STEP 7
    print_step(7, "Update Case Status")
    print_ok("Update status to charge-sheeted",
             "200 CaseStatusID=2 (Under Investigation -> Charge Sheeted)")

    # STEP 8
    print_step(8, "Generate Related Case Suggestions")
    print_ok("Generate related cases",
             '200 [{"SuggestionID":1,"CandidateFIRID":6,"ConfidenceScore":0.92,"ReviewStatus":"pending"}]')

    # STEP 9
    print_step(9, "Review and Accept Related Case Suggestion")
    print_ok("Accept suggestion", '200 {"ReviewStatus":"accepted"}')

    # STEP 10
    print_step(10, "View Case Timeline")
    print_ok("Get timeline",
             '200 [{"type":"FIR_REGISTERED"},{"type":"NOTE_ADDED"},{"type":"EVIDENCE_UPLOADED"},{"type":"STATUS_CHANGED"}]')

    # STEP 11
    print_step(11, "Authenticate as Supervisor")
    print_ok("Login supervisor", "200 userId=3 role=supervisor")

    # STEP 12
    print_step(12, "View Supervisor Dashboard")
    print_ok("Supervisor dashboard",
             '200 {"total_firs":25,"pending_review_count":3,"active_officer_count":4}')
    print_ok("Recent activity", '200 [{"CaseMasterID":1,"ActivityType":"FIR_REGISTERED"}]')

    # STEP 13
    print_step(13, "Review Case Progress")
    print_ok("List notes", "200 [2 notes found]")
    print_ok("List evidence", "200 [2 evidence items found]")
    print_ok("Submit supervisor review", '201 ReviewID=1 Status=approved')

    # STEP 14
    print_step(14, "Request Investigation Progress Report")
    print_ok("Request report", '201 {"ReportID":"RPT-001","Status":"pending"}')

    # STEP 15
    print_step(15, "Generate the Report")
    print_ok("Generate report",
             '200 {"report_type":"investigation_progress","generated_at":"2026-07-26T21:30:00"}')
    print_ok("Get report status", '200 {"Status":"completed"}')

    # STEP 16
    print_step(16, "View Audit Trail")
    print_ok("View audit trail",
             '200 [{"Action":"FIR_CREATED"},{"Action":"NOTE_ADDED"},{"Action":"EVIDENCE_UPLOADED"},{"Action":"STATUS_CHANGED"}]')

    # -- complete ------------------------------------------------------------
    print(f"\n\n{'=' * 62}")
    print(f"  PHASE 4 DEMO COMPLETE (OFFLINE)")
    print(f"  Roles: officer -> supervisor")
    print(f"  Case: CM-1 (KA-01-001)")
    print(f"  16 workflow steps simulated")
    print(f"  Start the server and re-run for live API calls")
    print(f"{'=' * 62}")


# -- entrypoint --------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Phase 4 Hackathon Demo Flow -- Berunda",
        epilog="Example: python scripts/demo/phase4_demo_flow.py --base-url http://localhost:9000",
    )
    parser.add_argument("--base-url", default=os.environ.get("BERUNDA_API", "http://localhost:9000"))
    parser.add_argument("--wait", action="store_true", help="Wait for server to be ready")
    args = parser.parse_args()

    demo_flow(args.base_url, args.wait)


if __name__ == "__main__":
    main()