# link-analysis

NetworkX-based graph traversal for discovering hidden relationships between entities (persons, vehicles, locations, cases).

## Trigger

**HTTP** — POST

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/links/analyze` | Analyze links for a set of entities |
| POST | `/links/path` | Find shortest path between two entities |
| POST | `/links/community` | Detect communities in entity graph |

## Input Schema

### Analysis

```json
{
  "entityIds": ["string"],
  "depth": "number (default: 2)",
  "includeTypes": ["person", "vehicle", "location", "case"]
}
```

### Path Finding

```json
{
  "sourceId": "string (required)",
  "targetId": "string (required)",
  "maxDepth": "number (default: 4)"
}
```

## Output Schema

```json
{
  "success": true,
  "data": {
    "nodes": [
      {
        "id": "string",
        "label": "string",
        "type": "person | vehicle | location | case",
        "properties": {}
      }
    ],
    "edges": [
      {
        "source": "string",
        "target": "string",
        "label": "string",
        "weight": 0.85,
        "properties": {}
      }
    ],
    "metrics": {
      "nodeCount": 15,
      "edgeCount": 23,
      "density": 0.22,
      "connectedComponents": 3
    }
  }
}
```

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| NOT_FOUND | 404 | Entity not found |
| NO_PATH | 404 | No path exists between entities |
| ANALYSIS_FAILED | 500 | Graph computation error |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LINK_MAX_DEPTH` | `4` | Maximum traversal depth |
| `LINK_MIN_WEIGHT` | `0.3` | Minimum edge weight for inclusion |
| `LINK_CACHE_TTL` | `1800` | Graph cache TTL in seconds |

## Processing Flow

```
POST /links/analyze
  → Load entity relationship graph
  → Apply NetworkX traversal algorithms
  → Compute shortest paths / communities
  → Score link strength
  → Return graph data
```
