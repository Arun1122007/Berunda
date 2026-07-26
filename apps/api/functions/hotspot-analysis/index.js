const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  context.closeWithSuccess({
    success: true,
    hotspots: [
      { location: [12.9716, 77.5946], intensity: 0.85, radius: 500 }
    ]
  });
};
