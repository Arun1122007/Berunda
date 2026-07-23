const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  const ctx = catalyst.initialize(context);
  const { userId, action, entityType, entityId, oldValue, newValue, ipAddress } = event?.data || {};

  if (!action) {
    return context.closeWithFailure({ error: "action is required" });
  }

  const table = ctx.datastore().table("gov_AuditLog");
  const entry = await table.insertRow({
    UserID: userId || null,
    Action: action,
    EntityType: entityType || null,
    EntityID: entityId || null,
    OldValue: oldValue ? JSON.stringify(oldValue) : null,
    NewValue: newValue ? JSON.stringify(newValue) : null,
    Timestamp: new Date().toISOString(),
    IPAddress: ipAddress || null,
  });

  context.closeWithSuccess({ auditLogId: entry.AuditLogID, action, timestamp: entry.Timestamp });
};
