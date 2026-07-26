const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  const { action, userId, resourceId } = event?.data || {};
  context.closeWithSuccess({
    success: true,
    logId: "LOG-" + Date.now(),
    timestamp: new Date().toISOString()
  });
};
