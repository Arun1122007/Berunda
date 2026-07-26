const catalyst = require('zcatalyst-sdk-node');

const logger = {
  info: (msg, data) => console.log(JSON.stringify({ level: 'info', message: msg, ...data })),
  warn: (msg, data) => console.warn(JSON.stringify({ level: 'warn', message: msg, ...data })),
  error: (msg, err, data) => console.error(JSON.stringify({ level: 'error', message: msg, error: err?.message, stack: err?.stack, ...data })),
};

async function authenticate(app) {
  try {
    const auth = app.userManagement();
    const user = await auth.getCurrentUser();
    return user;
  } catch (err) {
    const authErr = new Error('Authentication failed. Valid Catalyst session required.');
    authErr.status = 401;
    authErr.code = 'AUTH_ERROR';
    throw authErr;
  }
}

function buildTargetUrl(path) {
  const apiBase = process.env.API_BASE_URL || 'http://localhost:8000';
  const base = apiBase.replace(/\/+$/, '');
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${base}${cleanPath}`;
}

function sanitizeHeaders(headers) {
  const safe = { ...headers };
  delete safe.host;
  delete safe.connection;
  delete safe['content-length'];
  delete safe['transfer-encoding'];
  return safe;
}

async function proxyRequest(req) {
  const targetUrl = buildTargetUrl(req.path || '/');
  const fetchOptions = {
    method: req.method || 'GET',
    headers: sanitizeHeaders(req.headers),
  };

  const hasBody = req.method !== 'GET' && req.method !== 'HEAD'
    && req.body && typeof req.body === 'object';

  if (hasBody) {
    fetchOptions.body = JSON.stringify(req.body);
  }

  const timeout = parseInt(process.env.PROXY_TIMEOUT_MS || '30000', 10);
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  fetchOptions.signal = controller.signal;

  let response;
  try {
    response = await fetch(targetUrl, fetchOptions);
  } finally {
    clearTimeout(timeoutId);
  }

  const contentType = response.headers.get('content-type') || '';
  let data;
  if (contentType.includes('application/json')) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  return { status: response.status, data, ok: response.ok };
}

function createProxyHandler(config) {
  return async (req, res) => {
    const correlationId = req.headers?.['x-correlation-id']
      || req.headers?.['X-Correlation-ID']
      || `berunda-${Date.now()}`;
    const startTime = Date.now();

    res.setHeader('x-correlation-id', correlationId);
    res.setHeader('x-powered-by', 'Berunda-Catalyst');

    try {
      logger.info(`${config.name} invoked`, {
        method: req.method,
        path: req.path,
        functionName: config.name,
        correlationId,
      });

      const app = catalyst.initialize(req);
      let user;
      try {
        user = await authenticate(app);
      } catch (authErr) {
        logger.warn(`${config.name} authentication failed`, {
          functionName: config.name,
          correlationId,
        });
        return res.status(401).json({
          success: false,
          error: { code: 'AUTH_ERROR', message: authErr.message },
          correlationId,
        });
      }

      const userId = user?.user_id || user?.sub || 'anonymous';
      const userRole = user?.role || 'viewer';

      logger.info(`${config.name} authenticated`, {
        functionName: config.name,
        userId,
        role: userRole,
        correlationId,
      });

      req.headers['x-user-id'] = userId;
      req.headers['x-user-role'] = userRole;

      const response = await proxyRequest(req);

      const elapsed = Date.now() - startTime;
      logger.info(`${config.name} completed`, {
        functionName: config.name,
        status: response.status,
        elapsed: `${elapsed}ms`,
        correlationId,
      });

      return res.status(response.status).json(response.data);
    } catch (err) {
      const elapsed = Date.now() - startTime;

      if (err.name === 'AbortError') {
        logger.error(`${config.name} timeout`, err, {
          functionName: config.name,
          correlationId,
        });
        return res.status(504).json({
          success: false,
          error: { code: 'TIMEOUT_ERROR', message: 'Backend request timed out. Please try again.' },
          correlationId,
        });
      }

      if (err.code === 'ECONNREFUSED' || err.code === 'ECONNRESET' || err.code === 'ENOTFOUND' || err.type === 'system') {
        logger.error(`${config.name} backend unavailable`, err, {
          functionName: config.name,
          correlationId,
        });
        return res.status(502).json({
          success: false,
          error: { code: 'BACKEND_UNAVAILABLE', message: 'Backend service is currently unavailable.' },
          correlationId,
        });
      }

      if (err instanceof SyntaxError && err.message.includes('JSON')) {
        logger.error(`${config.name} invalid response`, err, {
          functionName: config.name,
          correlationId,
        });
        return res.status(502).json({
          success: false,
          error: { code: 'INVALID_RESPONSE', message: 'Backend returned an invalid response.' },
          correlationId,
        });
      }

      logger.error(`${config.name} unexpected error`, err, {
        functionName: config.name,
        correlationId,
      });
      return res.status(500).json({
        success: false,
        error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred.' },
        correlationId,
      });
    }
  };
}

module.exports = { createProxyHandler, authenticate, proxyRequest, buildTargetUrl };
