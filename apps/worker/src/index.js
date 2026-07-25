import Catalyst from 'catalyst-sdk-node';
import { writeFileSync } from 'fs';

const logger = {
  info: (...args) => console.log(JSON.stringify({ level: 'info', timestamp: new Date().toISOString(), message: args.join(' ') })),
  warn: (...args) => console.warn(JSON.stringify({ level: 'warn', timestamp: new Date().toISOString(), message: args.join(' ') })),
  error: (...args) => console.error(JSON.stringify({ level: 'error', timestamp: new Date().toISOString(), message: args.join(' ') })),
};

const JOB_REGISTRY = {
  'nightly-hotspot-recompute': { description: 'Recompute hotspot KDE/hexbin data', timeout: 600000 },
  'data-freshness-check': { description: 'Verify data store sync and freshness', timeout: 120000 },
  'report-generation': { description: 'Generate scheduled PDF/CSV reports', timeout: 300000 },
  'anomaly-scan': { description: 'Run anomaly detection pipeline', timeout: 300000 },
  'risk-batch-update': { description: 'Batch recompute risk scores', timeout: 600000 },
  'audit-log-archive': { description: 'Archive and compress old audit logs', timeout: 600000 },
};

const jobHandlers = {
  'nightly-hotspot-recompute': async (payload) => {
    logger.info('Executing nightly-hotspot-recompute', { districts: payload?.districts ?? 'all' });
  },
  'data-freshness-check': async () => {
    logger.info('Executing data-freshness-check');
  },
  'report-generation': async (payload) => {
    logger.info('Executing report-generation', { type: payload?.type ?? 'default' });
  },
  'anomaly-scan': async () => {
    logger.info('Executing anomaly-scan');
  },
  'risk-batch-update': async () => {
    logger.info('Executing risk-batch-update');
  },
  'audit-log-archive': async () => {
    logger.info('Executing audit-log-archive');
  },
};

async function start() {
  logger.info('Worker starting...');

  try {
    Catalyst.initialize();
    logger.info('Catalyst SDK initialized');
  } catch (err) {
    logger.warn('Catalyst SDK not available, running standalone', err.message);
  }

  try {
    writeFileSync('/tmp/worker-health', 'ok');
  } catch {
    // tmpfs may not be available outside container
  }

  const shutdown = (signal) => {
    logger.info(`Received ${signal}, shutting down gracefully`);
    process.exit(0);
  };

  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('SIGINT', () => shutdown('SIGINT'));

  const maxConcurrency = parseInt(process.env.WORKER_MAX_CONCURRENCY || '5', 10);
  const retryMax = parseInt(process.env.WORKER_RETRY_MAX || '3', 10);

  logger.info('Worker ready', {
    jobs: Object.keys(JOB_REGISTRY),
    maxConcurrency,
    retryMax,
    node: process.version,
  });
}

export { JOB_REGISTRY, jobHandlers, start };

start().catch((err) => {
  logger.error('Worker failed to start', err);
  process.exit(1);
});
