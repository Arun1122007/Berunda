const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  context.closeWithSuccess({
    success: true,
    nodes: [{ id: "PER-1", label: "Person" }],
    edges: []
  });
};
