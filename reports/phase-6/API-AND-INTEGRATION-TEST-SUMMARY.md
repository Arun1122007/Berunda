# Project Berunda — API & Integration Test Summary

## Test Execution Metrics
```
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-8.4.1, pluggy-1.6.0
sensitiveurl: .*
rootdir: D:\Hack2Skill\Berunda\tests
configfile: pytest.ini
plugins: anyio-4.13.0, Faker-40.31.0, asyncio-1.4.0, base-url-2.1.0, cov-7.1.0, html-4.1.1, metadata-3.1.1, mock-3.15.1, selenium-4.1.0, variables-3.1.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 28 items

tests\phase6\test_phase6_full_workflow.py::TestHealth::test_health 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:00 [INFO] httpx: HTTP Request: GET http://test/health "HTTP/1.1 200 OK"
PASSED                                                                   [  3%]
tests\phase6\test_phase6_full_workflow.py::TestHealth::test_readiness 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:00 [INFO] httpx: HTTP Request: GET http://test/ready "HTTP/1.1 200 OK"
PASSED                                                                   [  7%]
tests\phase6\test_phase6_full_workflow.py::TestHealth::test_root 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:01 [INFO] httpx: HTTP Request: GET http://test/ "HTTP/1.1 200 OK"
PASSED                                                                   [ 10%]
tests\phase6\test_phase6_full_workflow.py::TestAuth::test_register_and_login 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:01 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:02 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
PASSED                                                                   [ 14%]
tests\phase6\test_phase6_full_workflow.py::TestAuth::test_login_wrong_credentials 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:02 [WARNING] src.main: Exception: Invalid credentials
2026-07-26 23:12:02 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 401 Unauthorized"
PASSED                                                                   [ 17%]
tests\phase6\test_phase6_full_workflow.py::TestAuth::test_login_disabled_user 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:03 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:03 [WARNING] src.main: Exception: Invalid credentials
2026-07-26 23:12:03 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 401 Unauthorized"
PASSED                                                                   [ 21%]
tests\phase6\test_phase6_full_workflow.py::TestFIR::test_create_fir 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:04 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:04 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:04 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
PASSED                                                                   [ 25%]
tests\phase6\test_phase6_full_workflow.py::TestFIR::test_list_firs 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:05 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:06 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:06 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:06 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir "HTTP/1.1 200 OK"
PASSED                                                                   [ 28%]
tests\phase6\test_phase6_full_workflow.py::TestFIR::test_get_fir 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:07 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:08 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:08 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:08 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1 "HTTP/1.1 200 OK"
PASSED                                                                   [ 32%]
tests\phase6\test_phase6_full_workflow.py::TestFIR::test_update_fir 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:09 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:09 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:09 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:09 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/1 "HTTP/1.1 200 OK"
PASSED                                                                   [ 35%]
tests\phase6\test_phase6_full_workflow.py::TestFIR::test_status_transition 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:10 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:11 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:11 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:11 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/1/status "HTTP/1.1 200 OK"
PASSED                                                                   [ 39%]
tests\phase6\test_phase6_full_workflow.py::TestFIR::test_invalid_status_transition 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:12 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:12 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:12 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:12 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/1/status "HTTP/1.1 400 Bad Request"
PASSED                                                                   [ 42%]
tests\phase6\test_phase6_full_workflow.py::TestInvestigation::test_create_note 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:14 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:14 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:15 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:15 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/notes "HTTP/1.1 201 Created"
PASSED                                                                   [ 46%]
tests\phase6\test_phase6_full_workflow.py::TestInvestigation::test_list_notes 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:15 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:18 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:18 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:18 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/notes "HTTP/1.1 201 Created"
2026-07-26 23:12:18 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/notes "HTTP/1.1 200 OK"
PASSED                                                                   [ 50%]
tests\phase6\test_phase6_full_workflow.py::TestInvestigation::test_get_timeline 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:20 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:22 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:23 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:23 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/timeline "HTTP/1.1 200 OK"
PASSED                                                                   [ 53%]
tests\phase6\test_phase6_full_workflow.py::TestInvestigation::test_assign_officer 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:25 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:26 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:26 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:26 [INFO] berunda.event_bus: Connected CatalystWebhookService to EventBusService
2026-07-26 23:12:26 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1000 to topic 'case.assigned'
2026-07-26 23:12:26 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/assignments "HTTP/1.1 201 Created"
PASSED                                                                   [ 57%]
tests\phase6\test_phase6_full_workflow.py::TestInvestigation::test_supervisor_review 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:27 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:27 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:27 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:28 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1001 to topic 'supervisor.review.created'
2026-07-26 23:12:28 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/reviews "HTTP/1.1 201 Created"
PASSED                                                                   [ 60%]
tests\phase6\test_phase6_full_workflow.py::TestSearchAndDashboard::test_search 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:29 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:29 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:29 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:29 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 64%]
tests\phase6\test_phase6_full_workflow.py::TestSearchAndDashboard::test_dashboard 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:30 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:31 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:31 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/officer "HTTP/1.1 200 OK"
PASSED                                                                   [ 67%]
tests\phase6\test_phase6_full_workflow.py::TestSearchAndDashboard::test_reports 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:31 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:32 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:32 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:32 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 201 Created"
PASSED                                                                   [ 71%]
tests\phase6\test_phase6_full_workflow.py::TestSearchAndDashboard::test_audit 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:33 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:33 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:33 [INFO] httpx: HTTP Request: GET http://test/api/v1/audit "HTTP/1.1 200 OK"
PASSED                                                                   [ 75%]
tests\phase6\test_phase6_full_workflow.py::TestSearchAndDashboard::test_police_stations 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:34 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:35 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:35 [INFO] httpx: HTTP Request: GET http://test/api/v1/police-stations "HTTP/1.1 200 OK"
PASSED                                                                   [ 78%]
tests\phase6\test_phase6_full_workflow.py::TestSearchAndDashboard::test_districts 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:35 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:37 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:37 [INFO] httpx: HTTP Request: GET http://test/api/v1/police-stations/districts "HTTP/1.1 200 OK"
PASSED                                                                   [ 82%]
tests\phase6\test_phase6_full_workflow.py::TestSearchAndDashboard::test_lifecycle_info 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:37 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/statuses/lifecycle "HTTP/1.1 200 OK"
PASSED                                                                   [ 85%]
tests\phase6\test_phase6_full_workflow.py::TestSearchAndDashboard::test_allowed_transitions 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:38 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/statuses/transitions?current_status_id=1 "HTTP/1.1 200 OK"
PASSED                                                                   [ 89%]
tests\phase6\test_phase6_full_workflow.py::TestSearchAndDashboard::test_evidence_upload 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:41 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:42 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:42 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:42 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1002 to topic 'evidence.uploaded'
2026-07-26 23:12:42 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/evidence "HTTP/1.1 201 Created"
PASSED                                                                   [ 92%]
tests\phase6\test_phase6_full_workflow.py::TestSearchAndDashboard::test_related_cases 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:44 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:45 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:45 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:45 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:45 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/related-cases/generate "HTTP/1.1 200 OK"
PASSED                                                                   [ 96%]
tests\phase6\test_phase6_full_workflow.py::TestSearchAndDashboard::test_ai_endpoint 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:46 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:47 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:12:47 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:12:47 [INFO] src.services.ai_provider: Mock Provider received prompt: Summarize the following incident report objectivel...
2026-07-26 23:12:47 [INFO] httpx: HTTP Request: POST http://test/api/v1/ai/firs/1/summarize "HTTP/1.1 200 OK"
PASSED                                                                   [100%]

============================= 28 passed in 52.61s =============================
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-8.4.1, pluggy-1.6.0
sensitiveurl: .*
rootdir: D:\Hack2Skill\Berunda\tests
configfile: pytest.ini
plugins: anyio-4.13.0, Faker-40.31.0, asyncio-1.4.0, base-url-2.1.0, cov-7.1.0, html-4.1.1, metadata-3.1.1, mock-3.15.1, selenium-4.1.0, variables-3.1.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 123 items

tests\api\test_auth_api.py::TestAuthAPI::test_register_returns_201 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:57 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
PASSED                                                                   [  0%]
tests\api\test_auth_api.py::TestAuthAPI::test_register_duplicate_returns_409 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:58 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:58 [WARNING] src.main: Exception: Email already registered
2026-07-26 23:12:58 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 409 Conflict"
PASSED                                                                   [  1%]
tests\api\test_auth_api.py::TestAuthAPI::test_login_valid_returns_token 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:58 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:12:59 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
PASSED                                                                   [  2%]
tests\api\test_auth_api.py::TestAuthAPI::test_login_invalid_returns_401 
-------------------------------- live log call --------------------------------
2026-07-26 23:12:59 [WARNING] src.main: Exception: Invalid credentials
2026-07-26 23:12:59 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 401 Unauthorized"
PASSED                                                                   [  3%]
tests\api\test_auth_api.py::TestAuthAPI::test_get_me_returns_user 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:00 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:13:00 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:13:00 [INFO] httpx: HTTP Request: GET http://test/api/v1/auth/me "HTTP/1.1 200 OK"
PASSED                                                                   [  4%]
tests\api\test_auth_api.py::TestAuthAPI::test_me_without_auth_returns_ok 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:00 [INFO] httpx: HTTP Request: GET http://test/api/v1/auth/me "HTTP/1.1 200 OK"
PASSED                                                                   [  4%]
tests\api\test_auth_api.py::TestAuthAPI::test_logout_revokes_session 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:02 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/register "HTTP/1.1 201 Created"
2026-07-26 23:13:02 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/login "HTTP/1.1 200 OK"
2026-07-26 23:13:02 [INFO] httpx: HTTP Request: POST http://test/api/v1/auth/logout "HTTP/1.1 200 OK"
PASSED                                                                   [  5%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_officer_dashboard_empty 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:03 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/officer "HTTP/1.1 200 OK"
PASSED                                                                   [  6%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_officer_dashboard_with_data 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:03 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/officer "HTTP/1.1 200 OK"
PASSED                                                                   [  7%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_officer_dashboard_shows_fields 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:04 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/officer "HTTP/1.1 200 OK"
PASSED                                                                   [  8%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_officer_dashboard_without_auth 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:04 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/officer "HTTP/1.1 200 OK"
PASSED                                                                   [  8%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_supervisor_dashboard_empty 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:04 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/supervisor "HTTP/1.1 200 OK"
PASSED                                                                   [  9%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_supervisor_dashboard_with_data 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:05 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/supervisor "HTTP/1.1 200 OK"
PASSED                                                                   [ 10%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_supervisor_dashboard_admin_allowed 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:05 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/supervisor "HTTP/1.1 200 OK"
PASSED                                                                   [ 11%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_supervisor_dashboard_officer_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:05 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/supervisor "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 12%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_supervisor_dashboard_viewer_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:05 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/supervisor "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 13%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_supervisor_dashboard_analyst_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:06 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/supervisor "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 13%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_supervisor_dashboard_no_auth_returns_401 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:06 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/supervisor "HTTP/1.1 401 Unauthorized"
PASSED                                                                   [ 14%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_activity_empty 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:06 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/activity "HTTP/1.1 200 OK"
PASSED                                                                   [ 15%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_activity_with_data 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:06 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/activity "HTTP/1.1 200 OK"
PASSED                                                                   [ 16%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_activity_without_auth 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:07 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/activity "HTTP/1.1 200 OK"
PASSED                                                                   [ 17%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_activity_not_exceeds_10_items 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:07 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/activity "HTTP/1.1 200 OK"
PASSED                                                                   [ 17%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_officer_dashboard_empty_ps 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:07 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/officer "HTTP/1.1 200 OK"
PASSED                                                                   [ 18%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_supervisor_dashboard_empty_ps 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:08 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/supervisor "HTTP/1.1 200 OK"
PASSED                                                                   [ 19%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_admin_dashboard_officer 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:08 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/officer "HTTP/1.1 200 OK"
PASSED                                                                   [ 20%]
tests\api\test_dashboard_api.py::TestDashboardAPI::test_activity_returns_list 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:08 [INFO] httpx: HTTP Request: GET http://test/api/v1/dashboard/activity "HTTP/1.1 200 OK"
PASSED                                                                   [ 21%]
tests\api\test_fir_api.py::TestFIRAPI::test_list_firs_empty 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:10 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir "HTTP/1.1 200 OK"
PASSED                                                                   [ 21%]
tests\api\test_fir_api.py::TestFIRAPI::test_create_fir 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:11 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
PASSED                                                                   [ 22%]
tests\api\test_fir_api.py::TestFIRAPI::test_create_and_retrieve 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:12 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:13:12 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1 "HTTP/1.1 200 OK"
PASSED                                                                   [ 23%]
tests\api\test_fir_api.py::TestFIRAPI::test_list_after_create 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:13 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
2026-07-26 23:13:13 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir "HTTP/1.1 200 OK"
PASSED                                                                   [ 24%]
tests\api\test_fir_api.py::TestFIRAPI::test_create_without_auth_returns_401 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:14 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 401 Unauthorized"
PASSED                                                                   [ 25%]
tests\api\test_fir_api.py::TestFIRAPI::test_list_without_auth_returns_200 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:14 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir "HTTP/1.1 200 OK"
PASSED                                                                   [ 26%]
tests\api\test_fir_api.py::TestFIRAPI::test_get_nonexistent_returns_404 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:15 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/99999 "HTTP/1.1 404 Not Found"
PASSED                                                                   [ 26%]
tests\api\test_fir_api.py::TestFIRAPI::test_create_fir_all_fields 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:16 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir "HTTP/1.1 201 Created"
PASSED                                                                   [ 27%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_create_note_success 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:17 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/notes "HTTP/1.1 201 Created"
PASSED                                                                   [ 28%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_create_note_no_auth_returns_401 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:17 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/notes "HTTP/1.1 401 Unauthorized"
PASSED                                                                   [ 29%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_create_note_viewer_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:17 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/notes "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 30%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_create_note_analyst_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:17 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/notes "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 30%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_create_note_invalid_fir_404 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:18 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/99999/notes "HTTP/1.1 404 Not Found"
PASSED                                                                   [ 31%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_create_note_invalid_returns_422 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:18 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/notes "HTTP/1.1 422 Unprocessable Entity"
PASSED                                                                   [ 32%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_list_notes_empty 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:18 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/notes "HTTP/1.1 200 OK"
PASSED                                                                   [ 33%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_list_notes_after_create 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:18 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/notes "HTTP/1.1 201 Created"
2026-07-26 23:13:18 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/notes "HTTP/1.1 201 Created"
2026-07-26 23:13:18 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/notes "HTTP/1.1 200 OK"
PASSED                                                                   [ 34%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_assign_officer_success 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:19 [INFO] berunda.event_bus: Connected CatalystWebhookService to EventBusService
2026-07-26 23:13:19 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1000 to topic 'case.assigned'
2026-07-26 23:13:19 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/assignments "HTTP/1.1 201 Created"
PASSED                                                                   [ 34%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_assign_officer_analyst_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:19 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/assignments "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 35%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_assign_officer_viewer_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:19 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/assignments "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 36%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_assign_officer_no_auth_returns_401 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:20 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/assignments "HTTP/1.1 401 Unauthorized"
PASSED                                                                   [ 37%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_list_assignments_after_create 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:20 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1001 to topic 'case.assigned'
2026-07-26 23:13:20 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/assignments "HTTP/1.1 201 Created"
2026-07-26 23:13:20 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1002 to topic 'case.assigned'
2026-07-26 23:13:20 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/assignments "HTTP/1.1 201 Created"
2026-07-26 23:13:20 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/assignments "HTTP/1.1 200 OK"
PASSED                                                                   [ 38%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_list_assignments_empty 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:20 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/assignments "HTTP/1.1 200 OK"
PASSED                                                                   [ 39%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_get_active_assignment_after_assign 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:21 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1003 to topic 'case.assigned'
2026-07-26 23:13:21 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/assignments "HTTP/1.1 201 Created"
2026-07-26 23:13:21 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/assignment/active "HTTP/1.1 200 OK"
PASSED                                                                   [ 39%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_get_active_assignment_not_found 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:21 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/assignment/active "HTTP/1.1 200 OK"
PASSED                                                                   [ 40%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_update_status_success 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:21 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/1/status "HTTP/1.1 200 OK"
PASSED                                                                   [ 41%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_update_status_viewer_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:21 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/1/status "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 42%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_update_status_no_auth_returns_401 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:22 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/1/status "HTTP/1.1 401 Unauthorized"
PASSED                                                                   [ 43%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_update_status_same_status_no_change 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:22 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/1/status "HTTP/1.1 200 OK"
2026-07-26 23:13:22 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/1/status "HTTP/1.1 200 OK"
PASSED                                                                   [ 43%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_update_status_invalid_case_status_id_422 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:22 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/1/status "HTTP/1.1 422 Unprocessable Entity"
PASSED                                                                   [ 44%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_timeline_has_fir_registered_event 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:22 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/timeline "HTTP/1.1 200 OK"
PASSED                                                                   [ 45%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_timeline_returns_200 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:23 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/timeline "HTTP/1.1 200 OK"
PASSED                                                                   [ 46%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_create_review_success 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:23 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1004 to topic 'supervisor.review.created'
2026-07-26 23:13:23 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/reviews "HTTP/1.1 201 Created"
PASSED                                                                   [ 47%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_create_review_officer_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:23 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/reviews "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 47%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_create_review_no_auth_returns_401 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:24 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/reviews "HTTP/1.1 401 Unauthorized"
PASSED                                                                   [ 48%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_list_reviews_empty 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:24 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/reviews "HTTP/1.1 200 OK"
PASSED                                                                   [ 49%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_list_reviews_after_create 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:24 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1005 to topic 'supervisor.review.created'
2026-07-26 23:13:24 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/reviews "HTTP/1.1 201 Created"
2026-07-26 23:13:24 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/reviews "HTTP/1.1 200 OK"
PASSED                                                                   [ 50%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_admin_can_assign 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:24 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1006 to topic 'case.assigned'
2026-07-26 23:13:24 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/assignments "HTTP/1.1 201 Created"
PASSED                                                                   [ 51%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_admin_can_review 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:25 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1007 to topic 'supervisor.review.created'
2026-07-26 23:13:25 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/reviews "HTTP/1.1 201 Created"
PASSED                                                                   [ 52%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_admin_can_update_status 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:25 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/1/status "HTTP/1.1 200 OK"
PASSED                                                                   [ 52%]
tests\api\test_investigation_api.py::TestInvestigationAPI::test_update_status_analyst_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:25 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/1/status "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 53%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_generate_related_cases 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:25 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/related-cases/generate "HTTP/1.1 200 OK"
PASSED                                                                   [ 54%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_generate_related_cases_second_call_returns_cached 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:26 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/related-cases/generate "HTTP/1.1 200 OK"
2026-07-26 23:13:26 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/related-cases/generate "HTTP/1.1 200 OK"
PASSED                                                                   [ 55%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_generate_related_cases_nonexistent_fir 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:26 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/99999/related-cases/generate "HTTP/1.1 404 Not Found"
PASSED                                                                   [ 56%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_generate_related_cases_viewer_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:26 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/related-cases/generate "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 56%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_generate_related_cases_no_auth_returns_401 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:27 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/related-cases/generate "HTTP/1.1 401 Unauthorized"
PASSED                                                                   [ 57%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_generate_with_analyst_role 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:27 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/related-cases/generate "HTTP/1.1 200 OK"
PASSED                                                                   [ 58%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_list_related_cases_empty 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:27 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/related-cases "HTTP/1.1 200 OK"
PASSED                                                                   [ 59%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_list_related_cases_after_generate 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:28 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/related-cases/generate "HTTP/1.1 200 OK"
2026-07-26 23:13:28 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/related-cases "HTTP/1.1 200 OK"
PASSED                                                                   [ 60%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_list_related_cases_without_auth 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:28 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/related-cases "HTTP/1.1 200 OK"
PASSED                                                                   [ 60%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_review_accept_suggestion 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:28 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/related-cases/generate "HTTP/1.1 200 OK"
2026-07-26 23:13:28 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1008 to topic 'supervisor.review.created'
2026-07-26 23:13:28 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/related-cases/1/review "HTTP/1.1 200 OK"
PASSED                                                                   [ 61%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_review_reject_suggestion 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:28 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/related-cases/generate "HTTP/1.1 200 OK"
2026-07-26 23:13:28 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1009 to topic 'supervisor.review.created'
2026-07-26 23:13:28 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/related-cases/1/review "HTTP/1.1 200 OK"
PASSED                                                                   [ 62%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_review_invalid_suggestion_id 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:29 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/related-cases/99999/review "HTTP/1.1 404 Not Found"
PASSED                                                                   [ 63%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_review_analyst_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:29 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/related-cases/generate "HTTP/1.1 200 OK"
2026-07-26 23:13:29 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/related-cases/1/review "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 64%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_review_viewer_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:29 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/related-cases/generate "HTTP/1.1 200 OK"
2026-07-26 23:13:29 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/related-cases/1/review "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 65%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_review_invalid_status_returns_422 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:30 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/related-cases/generate "HTTP/1.1 200 OK"
2026-07-26 23:13:30 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/related-cases/1/review "HTTP/1.1 422 Unprocessable Entity"
PASSED                                                                   [ 65%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_generate_with_no_matching_signals 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:30 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/4/related-cases/generate "HTTP/1.1 200 OK"
PASSED                                                                   [ 66%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_list_after_review_shows_status 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:31 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/1/related-cases/generate "HTTP/1.1 200 OK"
2026-07-26 23:13:31 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1010 to topic 'supervisor.review.created'
2026-07-26 23:13:31 [INFO] httpx: HTTP Request: PUT http://test/api/v1/fir/related-cases/1/review "HTTP/1.1 200 OK"
2026-07-26 23:13:31 [INFO] httpx: HTTP Request: GET http://test/api/v1/fir/1/related-cases "HTTP/1.1 200 OK"
PASSED                                                                   [ 67%]
tests\api\test_related_cases_api.py::TestRelatedCasesAPI::test_generate_only_matches_crime_category 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:31 [INFO] httpx: HTTP Request: POST http://test/api/v1/fir/3/related-cases/generate "HTTP/1.1 200 OK"
PASSED                                                                   [ 68%]
tests\api\test_report_api.py::TestReportAPI::test_request_report_success 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:31 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 201 Created"
PASSED                                                                   [ 69%]
tests\api\test_report_api.py::TestReportAPI::test_request_report_investigation_progress 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:32 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 201 Created"
PASSED                                                                   [ 69%]
tests\api\test_report_api.py::TestReportAPI::test_request_report_evidence_inventory 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:32 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 201 Created"
PASSED                                                                   [ 70%]
tests\api\test_report_api.py::TestReportAPI::test_request_report_case_timeline 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:32 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 201 Created"
PASSED                                                                   [ 71%]
tests\api\test_report_api.py::TestReportAPI::test_request_report_supervisor_allowed 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:33 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 201 Created"
PASSED                                                                   [ 72%]
tests\api\test_report_api.py::TestReportAPI::test_request_report_viewer_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:33 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 73%]
tests\api\test_report_api.py::TestReportAPI::test_request_report_no_auth_returns_401 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:33 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 401 Unauthorized"
PASSED                                                                   [ 73%]
tests\api\test_report_api.py::TestReportAPI::test_request_report_invalid_returns_422 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:33 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 422 Unprocessable Entity"
PASSED                                                                   [ 74%]
tests\api\test_report_api.py::TestReportAPI::test_list_reports_empty 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:34 [INFO] httpx: HTTP Request: GET http://test/api/v1/reports "HTTP/1.1 200 OK"
PASSED                                                                   [ 75%]
tests\api\test_report_api.py::TestReportAPI::test_list_reports_after_create 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:34 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 201 Created"
2026-07-26 23:13:34 [INFO] httpx: HTTP Request: GET http://test/api/v1/reports "HTTP/1.1 200 OK"
PASSED                                                                   [ 76%]
tests\api\test_report_api.py::TestReportAPI::test_list_reports_without_auth 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:34 [INFO] httpx: HTTP Request: GET http://test/api/v1/reports "HTTP/1.1 200 OK"
PASSED                                                                   [ 77%]
tests\api\test_report_api.py::TestReportAPI::test_get_report_by_id 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:34 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 201 Created"
2026-07-26 23:13:35 [INFO] httpx: HTTP Request: GET http://test/api/v1/reports/RPT-730AA9AF0A11 "HTTP/1.1 200 OK"
PASSED                                                                   [ 78%]
tests\api\test_report_api.py::TestReportAPI::test_get_report_not_found 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:35 [INFO] httpx: HTTP Request: GET http://test/api/v1/reports/RPT-NONEXISTENT "HTTP/1.1 404 Not Found"
PASSED                                                                   [ 78%]
tests\api\test_report_api.py::TestReportAPI::test_get_report_without_auth_returns_200 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:35 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 201 Created"
2026-07-26 23:13:35 [INFO] httpx: HTTP Request: GET http://test/api/v1/reports/RPT-B3649F440DAC "HTTP/1.1 200 OK"
PASSED                                                                   [ 79%]
tests\api\test_report_api.py::TestReportAPI::test_generate_report 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:35 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 201 Created"
2026-07-26 23:13:35 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports/RPT-6D0627027D08/generate "HTTP/1.1 200 OK"
PASSED                                                                   [ 80%]
tests\api\test_report_api.py::TestReportAPI::test_generate_report_not_found 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:36 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports/RPT-NONEXISTENT/generate "HTTP/1.1 404 Not Found"
PASSED                                                                   [ 81%]
tests\api\test_report_api.py::TestReportAPI::test_generate_report_analyst 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:36 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 201 Created"
2026-07-26 23:13:36 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports/RPT-B32D8E4EB18B/generate "HTTP/1.1 200 OK"
PASSED                                                                   [ 82%]
tests\api\test_report_api.py::TestReportAPI::test_generate_report_viewer_forbidden 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:36 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports/RPT-FAKE/generate "HTTP/1.1 403 Forbidden"
PASSED                                                                   [ 82%]
tests\api\test_report_api.py::TestReportAPI::test_admin_all_report_ops 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:37 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 201 Created"
PASSED                                                                   [ 83%]
tests\api\test_report_api.py::TestReportAPI::test_list_reports_shows_all_for_user 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:37 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 201 Created"
2026-07-26 23:13:37 [INFO] httpx: HTTP Request: POST http://test/api/v1/reports "HTTP/1.1 201 Created"
2026-07-26 23:13:37 [INFO] httpx: HTTP Request: GET http://test/api/v1/reports "HTTP/1.1 200 OK"
PASSED                                                                   [ 84%]
tests\api\test_search_api.py::TestSearchAPI::test_search_empty 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:37 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 85%]
tests\api\test_search_api.py::TestSearchAPI::test_search_all 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:37 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 86%]
tests\api\test_search_api.py::TestSearchAPI::test_search_by_crime_no 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:37 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 86%]
tests\api\test_search_api.py::TestSearchAPI::test_search_by_crime_no_partial 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:37 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 87%]
tests\api\test_search_api.py::TestSearchAPI::test_search_by_vehicle_number 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 88%]
tests\api\test_search_api.py::TestSearchAPI::test_search_with_status_filter 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 89%]
tests\api\test_search_api.py::TestSearchAPI::test_search_with_police_station_filter 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 90%]
tests\api\test_search_api.py::TestSearchAPI::test_search_pagination_page_size 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 91%]
tests\api\test_search_api.py::TestSearchAPI::test_search_pagination_second_page 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 91%]
tests\api\test_search_api.py::TestSearchAPI::test_search_without_auth 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 92%]
tests\api\test_search_api.py::TestSearchAPI::test_search_non_admin_sees_filtered 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 93%]
tests\api\test_search_api.py::TestSearchAPI::test_search_invalid_page_returns_422 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 422 Unprocessable Entity"
PASSED                                                                   [ 94%]
tests\api\test_search_api.py::TestSearchAPI::test_search_invalid_page_size_returns_422 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 422 Unprocessable Entity"
PASSED                                                                   [ 95%]
tests\api\test_search_api.py::TestSearchAPI::test_search_semantic_flag 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 95%]
tests\api\test_search_api.py::TestSearchAPI::test_search_with_date_range 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 96%]
tests\api\test_search_api.py::TestSearchAPI::test_search_no_match_returns_empty 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/search "HTTP/1.1 200 OK"
PASSED                                                                   [ 97%]
tests\api\test_webhook_api.py::TestWebhookAPI::test_register_and_list_webhooks 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:38 [INFO] src.services.webhook_service: Registered Catalyst Webhook whk_437fef2c targeting https://catalyst.zoho.com/test-endpoint for events: ['case.assigned', 'evidence.uploaded']
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/webhooks "HTTP/1.1 201 Created"
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: GET http://test/api/v1/webhooks "HTTP/1.1 200 OK"
PASSED                                                                   [ 98%]
tests\api\test_webhook_api.py::TestWebhookAPI::test_test_dispatch_webhook 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:38 [INFO] src.services.webhook_service: Registered Catalyst Webhook whk_7ee6752c targeting catalyst://simulated-target for events: ['case.assigned']
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/webhooks "HTTP/1.1 201 Created"
2026-07-26 23:13:38 [INFO] berunda.event_bus: [EVENT BUS] Published event evt_1011 to topic 'case.assigned'
2026-07-26 23:13:38 [INFO] src.services.webhook_service: [CATALYST WEBHOOK] Delivery del_bd6416ef (success) to catalyst://simulated-target for event 'case.assigned' (HTTP 200, 1 attempt(s))
2026-07-26 23:13:38 [INFO] httpx: HTTP Request: POST http://test/api/v1/webhooks/test-dispatch "HTTP/1.1 200 OK"
PASSED                                                                   [ 99%]
tests\api\test_webhook_api.py::TestWebhookAPI::test_unregister_webhook 
-------------------------------- live log call --------------------------------
2026-07-26 23:13:39 [INFO] src.services.webhook_service: Registered Catalyst Webhook whk_5041984b targeting https://catalyst.zoho.com/to-delete for events: ['supervisor.review.created']
2026-07-26 23:13:39 [INFO] httpx: HTTP Request: POST http://test/api/v1/webhooks "HTTP/1.1 201 Created"
2026-07-26 23:13:39 [INFO] src.services.webhook_service: Unregistered Catalyst Webhook whk_5041984b
2026-07-26 23:13:39 [INFO] httpx: HTTP Request: DELETE http://test/api/v1/webhooks/whk_5041984b "HTTP/1.1 204 No Content"
2026-07-26 23:13:39 [INFO] httpx: HTTP Request: DELETE http://test/api/v1/webhooks/whk_5041984b "HTTP/1.1 404 Not Found"
PASSED                                                                   [100%]

============================ 123 passed in 47.24s =============================
```
