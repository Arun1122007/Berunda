# Stratus Storage Design and Implementation

> **Document ID:** BERUNDA-PH5-STRATUS-001 | **Version:** 1.0

## Storage Categories
1. **Original FIR Documents**: Raw uploaded PDFs/Images. Private, strict access control.
2. **Evidence Files**: Audio/Video/Images associated with a case.
3. **Generated Reports**: Output PDF/CSV analytics.
4. **Temporary Processing**: Fleeting storage for AI chunking.
5. **Demo Data**: Synthetic files for Datathon demo.

## Access Policy
- Stratus containers must be marked as **Private**.
- Temporary files must have an aggressive cleanup job.
- User filenames must not be used directly as object keys to prevent path traversal.
