const { createProxyHandler, authenticate, proxyRequest } = require('../../src/middleware/proxy');
const catalyst = require('zcatalyst-sdk-node');

const SENSITIVE_FIELDS = (process.env.FAIRNESS_SENSITIVE_FIELDS || 'religion,caste,community,ethnicity').split(',');

function scanSensitiveFields(features) {
  if (!Array.isArray(features)) return [];
  return features.filter(f =>
    SENSITIVE_FIELDS.some(sensitive => f.toLowerCase().includes(sensitive.toLowerCase()))
  );
}

module.exports = async (req, res) => {
  const handler = createProxyHandler({ name: 'fairness-check' });

  const correlationId = req.headers?.['x-correlation-id']
    || req.headers?.['X-Correlation-ID']
    || `berunda-${Date.now()}`;
  res.setHeader('x-correlation-id', correlationId);

  try {
    if (req.method === 'POST' && req.path === '/fairness/check') {
      const { features = [] } = req.body || {};

      const app = catalyst.initialize(req);
      await authenticate(app);

      const violations = scanSensitiveFields(features);

      req.body = {
        ...req.body,
        _prechecked: true,
        _sensitiveViolations: violations,
        _checkedAt: new Date().toISOString(),
      };

      const response = await proxyRequest(req);

      if (violations.length > 0) {
        return res.status(response.status).json({
          ...response.data,
          _warnings: [`Sensitive fields detected: ${violations.join(', ')}`],
        });
      }

      return res.status(response.status).json(response.data);
    }

    return handler(req, res);
  } catch (err) {
    if (err.status === 401) {
      return res.status(401).json({
        success: false,
        error: { code: 'AUTH_ERROR', message: err.message },
        correlationId,
      });
    }
    return res.status(500).json({
      success: false,
      error: { code: 'FAIRNESS_FAILED', message: err.message },
      correlationId,
    });
  }
};
