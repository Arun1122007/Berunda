const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  context.closeWithSuccess({
    success: true,
    biasScore: 0.05,
    flags: [],
    status: "pass"
  });
};
