# Database, Stratus, and File Integration

## File Upload Workflow
- Client initiates upload.
- Backend registers protected upload.
- Object stored in Catalyst Stratus.
- Verified that filenames cannot perform path traversal.
- Verified that Stratus objects default to private.
