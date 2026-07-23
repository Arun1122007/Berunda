const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  const ctx = catalyst.initialize(context);
  const { districtId, weekStart } = event?.data || {};

  const table = ctx.datastore().table("int_AnomalyAlert");
  const filters = { AlertLevel: 1 };
  if (districtId) filters.DistrictID = districtId;
  if (weekStart) filters.WeekStart = { $gte: weekStart };

  const alerts = await table.getAllRows(filters);
  alerts.sort((a, b) => b.ZScore - a.ZScore);

  context.closeWithSuccess({ alerts, total: alerts.length });
};
