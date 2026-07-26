const { createProxyHandler, authenticate, proxyRequest } = require('../../src/middleware/proxy');
const catalyst = require('zcatalyst-sdk-node');
const crypto = require('crypto');

function computeChainHash(previousHash, payload) {
  const hash = crypto.createHash('sha256');
  hash.update(previousHash || '');
  hash.update(JSON.stringify(payload));
  return hash.digest('hex');
}

module.exports = async (req, res) => {
  const handler = createProxyHandler({ name: 'audit-logging' });

  const correlationId = req.headers?.['x-correlation-id']
    || req.headers?.['X-Correlation-ID']
    || `berunda-${Date.now()}`;
  res.setHeader('x-correlation-id', correlationId);

  try {
    if (req.method === 'POST' && req.path === '/audit/log') {
      const { action, userId, resource, resourceId } = req.body || {};
      if (!action || !userId || !resource || !resourceId) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'Missing required fields: action, userId, resource, resourceId' },
          correlationId,
        });
      }

      const app = catalyst.initialize(req);
      await authenticate(app);

      const previousHash = req.body.previousHash || '';
      const currentHash = computeChainHash(previousHash, req.body);
      const auditEntry = {
        auditId: `AUDIT-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
        action,
        userId,
        resource,
        resourceId,
        previousHash,
        currentHash,
        timestamp: new Date().toISOString(),
      };

      req.body = auditEntry;
      req.path = '/audit/log';

      const response = await proxyRequest(req);
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
      error: { code: 'INTEGRITY_ERROR', message: err.message },
      correlationId,
    });
  }
};
