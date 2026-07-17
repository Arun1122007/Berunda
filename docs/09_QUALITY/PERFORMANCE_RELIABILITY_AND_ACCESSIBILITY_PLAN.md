# Performance, Reliability, and Accessibility Plan

[//]: # (Document ID: BERUNDA-QA-003 | Status: DRAFT | Classification: INTERNAL)

---

## 1. Performance Targets

### 1.1 API Response Times

| Endpoint Category | Target (p95) | Maximum (p99) | Measurement |
|-------------------|-------------|---------------|-------------|
| Simple reads (GET /cases/{id}, GET /persons/{id}) | < 200ms | < 500ms | API Gateway metrics |
| List queries with filters | < 500ms | < 1s | API Gateway metrics |
| Data import (POST /cases/import, 100 records) | < 5s | < 10s | Function timing |
| RAG query (POST /rag/query) | < 5s | < 10s | Function timing (includes LLM inference) |
| Graph traversal (GET /relationships/network/{id}) | < 2s | < 5s | AppSail timing |
| Map tile generation (GET /hotspots) | < 2s | < 5s | Function timing |
| Dashboard load (all tiles) | < 3s | < 5s | Browser DevTools |

### 1.2 Throughput

| Scenario | Target | Notes |
|----------|--------|-------|
| Concurrent API users | 10 | Hackathon demo scale |
| FIRs imported per minute | 1,000 | Batch import, not real-time |
| RAG queries per minute | 20 | Limited by LLM inference |
| Concurrent graph traversals | 5 | Single AppSail instance |

### 1.3 Data Volume

| Metric | Target | Scaling Strategy |
|--------|--------|------------------|
| Maximum FIRs | 5,000 | Static synthetic dataset |
| Maximum PersonEntities | 8,000 | Static |
| Maximum RelationshipEdges | 15,000 | Static |
| Maximum AuditLog entries | 50,000 | Static |
| Database size (estimated) | < 1 GB | Well within Catalyst Data Store limits |

## 2. Reliability Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| System uptime (demo hours) | 100% | Manual verification during demo |
| API availability | 99.9% | API Gateway health check |
| Data integrity | 100% | Referential integrity checks pass |
| Cron job success rate | 95% | Job execution logs |
| RAG answer success rate | 95% | Non-error responses |

## 3. Scalability Plan

| Component | Phase 1 Scaling | Phase 3+ Scaling |
|-----------|----------------|-------------------|
| Catalyst Functions | Auto-scaling by Catalyst (0-10 instances) | Auto-scaling with higher limits |
| AppSail (NetworkX) | Single instance | Multiple instances with load balancer |
| Data Store | Single instance | Read replicas + sharding |
| Cache | Single instance | Cluster mode |
| QuickML | Managed by Catalyst | Higher service tier |

## 4. Caching Strategy

| Cache | Key | TTL | Invalidation |
|-------|-----|-----|--------------|
| Hotspot layers | `hotspot:{districtId}:{weekStart}` | 24 hours | Cron job overwrites |
| Crime distribution | `analytics:crime-distribution:{districtId}` | 1 hour | Cache-bust on new import |
| PersonEntity search results | `search:{query}:{page}` | 5 minutes | Manual cache clear |
| RAG chunk embeddings | `rag:embedding:{chunkId}` | Permanent | Rebuilt on re-import |
| Audit log recent entries | `audit:recent:{userId}` | 1 minute | Direct DB read bypasses cache for audits |

## 5. Resilience Patterns

| Pattern | Implementation |
|---------|---------------|
| Retry with backoff | All function-to-function calls: 3 retries, exponential backoff (1s, 2s, 4s) |
| Timeout | All function calls: max 30s timeout |
| Circuit breaker | Phase 3+ (event-driven) — not implemented in Phase 1 |
| Bulkhead | Separate function instances for different workloads |
| Idempotency | Import uses X-Request-ID for deduplication |
| Graceful degradation | If QuickML is down, RAG returns "AI service unavailable" instead of error |

## 6. Accessibility Targets

| Standard | Target | Verification |
|----------|--------|-------------|
| WCAG 2.1 Level AA | Minimum for all public-facing views | Lighthouse audit |
| Color contrast | 4.5:1 for normal text, 3:1 for large text | Automated check |
| Keyboard navigation | All interactive elements accessible via keyboard | Manual check |
| Screen reader support | ARIA labels on all interactive elements | Manual check |
| Font scaling | UI works at 200% zoom | Manual check |
| Color-blind safe | Hotspot map uses patterns + colors, not color-only | Manual check |

**Note:** Full WCAG compliance is STRETCH. Minimum accessibility (color contrast, keyboard nav, ARIA labels) is MUST for MVP.
