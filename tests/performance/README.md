# Performance Tests

Load and stress tests to validate system performance under realistic and peak loads.

## Tool

[k6](https://k6.io) — a modern open-source load testing tool.

### Install k6

**Windows (Choco):**
```powershell
choco install k6
```

**macOS (Homebrew):**
```bash
brew install k6
```

**Linux (APT):**
```bash
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

**Docker:**
```bash
docker pull grafana/k6
```

**Manual:** Download from https://k6.io

## Running the Tests

### Default (localhost:9000)

```bash
k6 run tests/performance/k6-load-test.js
```

### Custom Base URL

```bash
k6 run -e BASE_URL=https://api.example.com tests/performance/k6-load-test.js
```

### Docker

```bash
docker run --rm -i grafana/k6 run -e BASE_URL=http://host.docker.internal:9000 - <tests/performance/k6-load-test.js
```

## Test Scenarios

| Stage | Duration | Target Users |
|-------|----------|--------------|
| Ramp up | 30s | 0 → 10 |
| Steady (low) | 1m | 10 |
| Ramp up | 30s | 10 → 50 |
| Steady (high) | 2m | 50 |
| Ramp down | 30s | 50 → 0 |

## Endpoints Tested

- `GET /health`
- `GET /ready`
- `GET /api/v1/status`
- `GET /api/v1/fir`
- `GET /api/v1/entities`
- `GET /api/v1/graph`
- `POST /api/v1/auth/login`

## Thresholds

- **p95 latency** < 500ms
- **Error rate** < 1% (non-5xx responses considered success)

## Metrics

- p50 / p95 / p99 latency
- Throughput (RPS)
- Error rate
- Request duration trend