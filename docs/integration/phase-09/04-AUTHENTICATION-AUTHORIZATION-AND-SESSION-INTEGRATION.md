# Authentication, Authorization, and Session Integration

## Flow Verified
`Frontend Login -> Catalyst Auth -> Backend Profile Lookup -> Frontend Protected Routes`

## Cross-Station Isolation
- Confirmed that officers from Station A cannot retrieve FIRs from Station B.
- Unauthorized access properly returns `403 Forbidden` rather than `404 Not Found` for existent records, or `404` where record existence must be obscured.
