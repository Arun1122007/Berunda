const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  const ctx = catalyst.initialize(context);
  const { personEntityId } = event?.data || {};

  if (!personEntityId) {
    return context.closeWithFailure({ error: "personEntityId is required" });
  }

  const linksTable = ctx.datastore().table("int_PersonEntityLink");
  const links = await linksTable.getAllRows({ PersonEntityID: personEntityId });

  const caseIds = [...new Set(links.map((l) => l.CaseMasterID).filter(Boolean))];
  const caseTable = ctx.datastore().table("src_CaseMaster");
  const cases = await Promise.all(caseIds.map((id) => caseTable.getRow(id)));

  const priorCount = cases.length;
  const accusationCount = links.filter((l) => l.SourceTable === "Accused").length;
  const victimCount = links.filter((l) => l.SourceTable === "Victim").length;

  let score = 0.3;
  score += Math.min(priorCount * 0.1, 0.3);
  score += Math.min(accusationCount * 0.05, 0.2);
  if (victimCount === 0) score += 0.1;

  const scoresTable = ctx.datastore().table("int_RiskScore");
  const row = await scoresTable.insertRow({
    PersonEntityID: personEntityId,
    Score: Math.round(score * 100000) / 100000,
    ModelVersion: "rule-based-v1",
    FeaturesJSON: JSON.stringify({ priorCount, accusationCount, victimCount }),
  });

  context.closeWithSuccess({ riskScoreId: row.RiskScoreID, score, priorCount, accusationCount, victimCount });
};
