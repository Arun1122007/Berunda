const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  const ctx = catalyst.initialize(context);
  const { districtId, weekStart, weekEnd } = event?.data || {};

  const tables = ctx.datastore().table("int_HotspotLayer");
  const filters = { DistrictID: districtId };
  if (weekStart) filters.WeekStart = { $gte: weekStart };
  if (weekEnd) filters.WeekEnd = { $lte: weekEnd };

  const layers = await tables.getAllRows(filters);
  context.closeWithSuccess({ hotspots: layers });
};
