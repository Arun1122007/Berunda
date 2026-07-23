const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  const ctx = catalyst.initialize(context);
  const req = event?.data || {};
  const body = typeof req === "string" ? JSON.parse(req) : req;

  try {
    const table = ctx.datastore().table("src_CaseMaster");
    const row = await table.insertRow(body);
    context.closeWithSuccess({ success: true, caseMasterId: row.CaseMasterID });
  } catch (err) {
    context.closeWithFailure({ error: err.message });
  }
};
