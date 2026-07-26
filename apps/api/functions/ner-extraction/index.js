const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  context.closeWithSuccess({
    success: true,
    entities: [
      { text: "Bengaluru", type: "LOCATION", confidence: 0.99 }
    ]
  });
};
