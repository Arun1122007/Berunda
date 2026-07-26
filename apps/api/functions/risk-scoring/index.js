const { createProxyHandler, authenticate, proxyRequest } = require('../../src/middleware/proxy');
const catalyst = require('zcatalyst-sdk-node');

module.exports = async (req, res) => {
  const handler = createProxyHandler({ name: 'risk-scoring' });

  const correlationId = req.headers?.['x-correlation-id']
    || req.headers?.['X-Correlation-ID']
    || `berunda-${Date.now()}`;
  res.setHeader('x-correlation-id', correlationId);

  try {
    if (req.method === 'POST' && (req.path === '/risk/score' || req.path === '/risk/score-batch')) {
      const app = catalyst.initialize(req);
      await authenticate(app);

      const personId = req.body?.personId;
      if (req.path === '/risk/score' && !personId) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'personId is required for risk scoring' },
          correlationId,
        });
      }
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
      error: { code: 'SCORE_FAILED', message: err.message },
      correlationId,
    });
  }
};
