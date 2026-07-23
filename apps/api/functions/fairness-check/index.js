const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  const ctx = catalyst.initialize(context);
  const { modelVersion } = event?.data || {};

  const riskTable = ctx.datastore().table("int_RiskScore");
  const scores = await riskTable.getAllRows({ ModelVersion: modelVersion || "rule-based-v1" });

  const groupScores = {};
  for (const s of scores) {
    const entity = await ctx.datastore().table("int_PersonEntity").getRow(s.PersonEntityID);
    const district = entity?.PrimaryDistrictID || "unknown";
    if (!groupScores[district]) groupScores[district] = [];
    groupScores[district].push(s.Score);
  }

  let passed = true;
  const details = [];
  for (const [district, districtScores] of Object.entries(groupScores)) {
    const mean = districtScores.reduce((a, b) => a + b, 0) / districtScores.length;
    const globalMean = scores.reduce((a, b) => a + b.Score, 0) / scores.length;
    const diff = Math.abs(mean - globalMean);
    if (diff > 0.2) passed = false;
    details.push({ district, meanScore: mean, globalMean, deviation: diff });
  }

  const checkTable = ctx.datastore().table("gov_FairnessCheckResult");
  await checkTable.insertRow({
    CheckType: "model_exclusion",
    Timestamp: new Date().toISOString(),
    Passed: passed ? 1 : 0,
    Details: JSON.stringify(details),
    CheckedBy: "system",
  });

  context.closeWithSuccess({ passed, details });
};
