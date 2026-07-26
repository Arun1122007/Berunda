const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  context.closeWithSuccess({
    success: true,
    answer: "Based on the case files, the suspect was last seen in Indiranagar.",
    citations: ["FIR-2026-001"]
  });
};
