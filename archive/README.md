# Archive Directory

> **Last Updated:** 2026-07-18
> **Classification:** Internal

---

## Purpose

The `archive/` directory contains files and directories that are preserved for historical reference but are no longer active in the main project structure. These items have been superseded, deprecated, or moved during restructuring, and are kept here to maintain auditability and traceability.

Examples of what belongs here:
- Superseded configuration files
- Previous versions of documents that have been reorganized
- Deprecated scripts or data pipelines
- Pre-restructuring directory snapshots
- Historical manifests superseded by newer versions

---

## Archive Manifest Format

Every archived item SHOULD be accompanied by a manifest note. Manifests can be stored as a single `ARCHIVE_MANIFEST.md` at the archive root or as individual `.manifest.md` files alongside archived items.

Recommended manifest entry format:

```markdown
## [item-name]

- **Original location:** `path/to/original/location`
- **Archived at:** 2026-07-18T10:00:00Z
- **Archived by:** user / agent-name
- **Reason:** e.g., "Superseded by new directory structure"
- **Restorable:** Yes/No — whether the item can be cleanly restored
- **Depends on:** [list any dependencies still in active use]
- **Replaced by:** `path/to/replacement` (if applicable)
```

### Example

```markdown
## config/old-pipeline-config.yml

- **Original location:** `config/old-pipeline-config.yml`
- **Archived at:** 2026-07-18T10:00:00Z
- **Archived by:** restructuring-agent
- **Reason:** Pipeline v1 config superseded by `config/pipeline-config-v2.yml`
- **Restorable:** Yes
- **Depends on:** None
- **Replaced by:** `config/pipeline-config-v2.yml`
```

---

## Retention Policy

- Archive contents are retained indefinitely for audit purposes.
- Items in `archive/` are NOT backed up separately (they are part of the repository).
- Items may be permanently deleted only after explicit team approval and a 90-day notice period posted in the project communication channel.

---

## Safe Deletion

Once the main project restructuring is verified and stable, the entire `archive/` directory (or individual items within it) may be deleted. Verify that no active references point to any archived item before deleting.
