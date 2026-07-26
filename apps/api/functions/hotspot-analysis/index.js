const { createProxyHandler } = require('../../src/middleware/proxy');

module.exports = createProxyHandler({ name: 'hotspot-analysis' });
