# Performance Tests

Load and stress tests to validate system performance under realistic and peak loads.

- **Tool**: k6
- **Run**: `k6 run tests/performance/k6-script.js`
- **Metrics**: p50/p95/p99 latency, throughput (RPS), error rate, resource utilization
- **Targets**: API p95 < 500ms, p99 < 2s, throughput > 100 RPS
