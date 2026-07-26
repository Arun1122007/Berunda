const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  const req = event?.data || {};
  context.closeWithSuccess({
    success: true,
    data: [
      {
        alertId: "ANOM-" + Date.now(),
        district: req.district || "Koramangala",
        crimeType: req.crimeType || "theft",
        observedCount: 28,
        expectedCount: 12.5,
        zScore: 3.45,
        severity: "high",
        detectedAt: new Date().toISOString(),
        period: new Date().toISOString().split("T")[0],
        acknowledged: false
      }
    ]
  });
};
