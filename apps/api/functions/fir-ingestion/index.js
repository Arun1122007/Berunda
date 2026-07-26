const { createProxyHandler, proxyRequest, buildTargetUrl } = require('../../src/middleware/proxy');

async function validateFirData(body) {
  const errors = [];
  if (!body || !Array.isArray(body.firs)) {
    errors.push({ field: 'firs', message: 'firs array is required' });
    return errors;
  }
  body.firs.forEach((fir, i) => {
    if (!fir.caseNumber) errors.push({ index: i, field: 'caseNumber', message: 'Case number is required' });
    if (!fir.district) errors.push({ index: i, field: 'district', message: 'District is required' });
    if (!fir.policeStation) errors.push({ index: i, field: 'policeStation', message: 'Police station is required' });
    if (!fir.dateFiled) errors.push({ index: i, field: 'dateFiled', message: 'Date filed is required' });
    if (!fir.narrative) errors.push({ index: i, field: 'narrative', message: 'Narrative is required' });
  });
  return errors;
}

module.exports = async (req, res) => {
  const handler = createProxyHandler({ name: 'fir-ingestion' });

  const correlationId = req.headers?.['x-correlation-id'] || `berunda-${Date.now()}`;
  res.setHeader('x-correlation-id', correlationId);

  try {
    if (req.method === 'POST' && req.path === '/fir/validate') {
      const errors = await validateFirData(req.body);
      if (errors.length > 0) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'Validation failed', details: { errors } },
          correlationId,
        });
      }
      return res.status(200).json({
        success: true,
        data: { valid: true, count: req.body.firs.length, errors: [] },
        correlationId,
      });
    }

    return handler(req, res);
  } catch (err) {
    return res.status(500).json({
      success: false,
      error: { code: 'IMPORT_ERROR', message: err.message },
      correlationId,
    });
  }
};
