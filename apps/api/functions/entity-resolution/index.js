const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  const { name, phone } = event?.data || {};
  context.closeWithSuccess({
    success: true,
    matches: [
      { entityId: "PER-" + Date.now(), confidence: 0.95, matchedOn: ["phone"] }
    ]
  });
};
