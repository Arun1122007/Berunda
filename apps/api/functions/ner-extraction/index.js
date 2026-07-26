const { createProxyHandler, authenticate, proxyRequest } = require('../../src/middleware/proxy');
const catalyst = require('zcatalyst-sdk-node');

module.exports = async (req, res) => {
  const handler = createProxyHandler({ name: 'ner-extraction' });

  const correlationId = req.headers?.['x-correlation-id']
    || req.headers?.['X-Correlation-ID']
    || `berunda-${Date.now()}`;
  res.setHeader('x-correlation-id', correlationId);

  try {
    if (req.method === 'POST' && req.path === '/ner/extract') {
      const { narrative } = req.body || {};
      if (!narrative || typeof narrative !== 'string' || narrative.trim().length === 0) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'Narrative text is required for entity extraction' },
          correlationId,
        });
      }
      if (narrative.length > 50000) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'Narrative exceeds maximum length of 50000 characters' },
          correlationId,
        });
      }
    }

    if (req.method === 'POST' && req.path === '/ner/extract-batch') {
      const { firs } = req.body || {};
      if (!Array.isArray(firs) || firs.length === 0) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'firs array is required for batch extraction' },
          correlationId,
        });
      }
      const maxBatch = parseInt(process.env.NER_BATCH_MAX || '50', 10);
      if (firs.length > maxBatch) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: `Batch size exceeds maximum of ${maxBatch}` },
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
      error: { code: 'NER_FAILED', message: err.message },
      correlationId,
    });
  }
};
