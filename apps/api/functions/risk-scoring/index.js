const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  context.closeWithSuccess({
    success: true,
    score: 75,
    factors: ["Repeat offense", "Weapon involved"],
    riskLevel: "High"
  });
};
