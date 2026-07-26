const { createProxyHandler, authenticate, proxyRequest } = require('../../src/middleware/proxy');
const catalyst = require('zcatalyst-sdk-node');

module.exports = async (req, res) => {
  const handler = createProxyHandler({ name: 'rag-query' });

  const correlationId = req.headers?.['x-correlation-id']
    || req.headers?.['X-Correlation-ID']
    || `berunda-${Date.now()}`;
  res.setHeader('x-correlation-id', correlationId);

  try {
    if (req.method === 'POST' && req.path === '/rag/query') {
      const { query } = req.body || {};
      if (!query || typeof query !== 'string' || query.trim().length === 0) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'Query text is required' },
          correlationId,
        });
      }
      if (query.length > 2000) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'Query exceeds maximum length of 2000 characters' },
          correlationId,
        });
      }

      const app = catalyst.initialize(req);
      await authenticate(app);
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
      error: { code: 'RAG_FAILED', message: err.message },
      correlationId,
    });
  }
};
