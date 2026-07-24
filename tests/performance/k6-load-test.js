import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:9000';

const errorRate = new Rate('errors');
const requestTrend = new Trend('request_duration');

export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 10 },
    { duration: '30s', target: 50 },
    { duration: '2m', target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    errors: ['rate<0.01'],
  },
};

function checkStatus(name, res) {
  const result = check(res, {
    [`${name} status is not 5xx`]: (r) => r.status < 500,
  });
  errorRate.add(!result);
  requestTrend.add(res.timings.duration);
}

export default function () {
  checkStatus('GET /health', http.get(`${BASE_URL}/health`));
  sleep(0.5);

  checkStatus('GET /ready', http.get(`${BASE_URL}/ready`));
  sleep(0.5);

  checkStatus('GET /api/v1/status', http.get(`${BASE_URL}/api/v1/status`));
  sleep(0.5);

  checkStatus('GET /api/v1/fir', http.get(`${BASE_URL}/api/v1/fir`));
  sleep(1);

  checkStatus('GET /api/v1/entities', http.get(`${BASE_URL}/api/v1/entities`));
  sleep(1);

  checkStatus('GET /api/v1/graph', http.get(`${BASE_URL}/api/v1/graph`));
  sleep(1);

  const loginPayload = JSON.stringify({
    email: 'admin@berunda.gov',
    password: 'admin',
  });
  const loginHeaders = { 'Content-Type': 'application/json' };
  const loginRes = http.post(`${BASE_URL}/api/v1/auth/login`, loginPayload, {
    headers: loginHeaders,
  });
  checkStatus('POST /api/v1/auth/login', loginRes);
  sleep(1);
}