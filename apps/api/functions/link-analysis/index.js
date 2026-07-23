const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  const ctx = catalyst.initialize(context);
  const { personEntityId, maxDepth = 2 } = event?.data || {};

  if (!personEntityId) {
    return context.closeWithFailure({ error: "personEntityId is required" });
  }

  const edgesTable = ctx.datastore().table("int_RelationshipEdge");
  const personsTable = ctx.datastore().table("int_PersonEntity");

  const visited = new Set();
  const nodes = {};
  const edges = [];
  let queue = [{ id: personEntityId, depth: 0 }];

  while (queue.length > 0) {
    const { id, depth } = queue.shift();
    if (visited.has(id) || depth > maxDepth) continue;
    visited.add(id);

    const person = await personsTable.getRow(id);
    if (person) nodes[id] = { id: String(id), label: person.CanonicalName, type: "person" };

    const relEdges = await edgesTable.getAllRows({
      $or: [{ PersonEntityA: id }, { PersonEntityB: id }],
    });

    for (const edge of relEdges) {
      const neighbor = edge.PersonEntityA === id ? edge.PersonEntityB : edge.PersonEntityA;
      if (neighbor) {
        queue.push({ id: neighbor, depth: depth + 1 });
        edges.push({
          source: String(edge.PersonEntityA),
          target: String(edge.PersonEntityB),
          label: edge.RelationshipType || "related",
          weight: edge.Confidence || 0.5,
        });
      }
    }
  }

  context.closeWithSuccess({ nodes: Object.values(nodes), edges });
};
