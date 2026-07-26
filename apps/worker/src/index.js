const catalyst = require("zcatalyst-sdk-node");

module.exports = async (cronDetails, context) => {
  const app = catalyst.initialize(context);
  const jobName = cronDetails?.cron_name;
  
  console.log(`Worker picked up job: ${jobName}`);

  try {
    switch (jobName) {
      case "nightly-hotspot-recompute":
        console.log("Recomputing hotspot data...");
        break;
      case "data-freshness-check":
        console.log("Checking data freshness...");
        break;
      case "report-generation":
        console.log("Generating scheduled reports...");
        break;
      case "anomaly-scan":
        console.log("Running anomaly scan...");
        break;
      case "risk-batch-update":
        console.log("Updating risk scores in batch...");
        break;
      case "audit-log-archive":
        console.log("Archiving audit logs...");
        break;
      default:
        console.log(`Unknown job: ${jobName}`);
    }
    context.closeWithSuccess();
  } catch (err) {
    console.error(`Job ${jobName} failed:`, err);
    context.closeWithFailure();
  }
};
